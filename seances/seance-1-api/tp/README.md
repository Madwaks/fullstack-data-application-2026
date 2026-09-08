# TP — Séance 1 : votre première API FastAPI (2h)

## Objectifs du TP

À la fin de ce TP, vous devez savoir :

- créer une application FastAPI et la lancer dans un conteneur Docker ;
- écrire des routes avec path parameters, query parameters et corps de requête validé ;
- utiliser Pydantic pour valider les entrées et filtrer les sorties ;
- renvoyer les bons codes de statut et gérer les erreurs proprement ;
- découper une API en routers ;
- faire générer une ressource complète par Copilot, puis la reviewer.

Le thème est celui du projet : **GearShare**, une plateforme de prêt de matériel entre étudiants
(voir [le sujet](../../../projet/sujet.md)). On travaille ici sur la ressource `items` (le matériel).

## Prérequis

- Docker Desktop lancé (`docker run hello-world` fonctionne).
- Python 3.11+ installé localement (pour l'autocomplétion de l'éditeur ; l'exécution se fait dans
  le conteneur).
- VS Code avec GitHub Copilot configuré (voir [INTRO.md](../../../OUTILS.md)).

**Aucune base de données dans ce TP** : on stocke tout dans un dictionnaire en mémoire. C'est
volontaire, et c'est ce qu'on corrigera à partir de la séance 3.

---

## Étape 0 — Prendre en main le projet de départ (15 min)

Ouvrez le projet fourni : [`projet-demo/`](./projet-demo/). Copiez-le dans le dépôt de votre
groupe avant de le modifier : c'est le point de départ de votre API pour ce TP.

Son arborescence est la suivante :

```text
projet-demo/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routers/
│   │   └── __init__.py
│   └── schemas/
│       └── __init__.py
├── Dockerfile
└── docker-compose.yml
```

Depuis ce dossier, lancez l'API :

```bash
docker compose up --build
```

**Vérifiez :**

1. `curl http://localhost:8000/health` renvoie `{"status":"ok"}` ;
2. `http://localhost:8000/docs` s'ouvre dans votre navigateur ;
3. modifiez le message de `/health`, sauvegardez, et rappelez la route **sans reconstruire
   l'image** : le changement est pris en compte.

Le point 3 est important. Prenez 2 minutes pour comprendre pourquoi :

- le `volumes:` monte votre dossier `app/` local dans le conteneur, donc le code du conteneur est
  votre code ;
- le `--reload` d'uvicorn détecte la modification et redémarre le serveur.

Sans ces deux lignes, vous devriez faire `docker compose up --build` à chaque modification.

> ⚠️ Le montage de volume et `--reload` sont des outils de **développement**. En production, on
> construit une image figée contenant le code. Vous ferez cette distinction en séance 7.

---

## Étape 1 — Path parameters (10 min)

Ajoutez dans `main.py` :

```python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}
```

**Testez et notez ce que vous observez :**

| Requête | Code attendu | Corps |
|---|---|---|
| `GET /items/42` | ? | ? |
| `GET /items/abc` | ? | ? |
| `GET /items/-1` | ? | ? |

La dernière ligne vous pose une question : rien dans le code n'interdit un identifiant négatif.
Corrigez avec `Path` :

```python
from fastapi import Path


@app.get("/items/{item_id}")
def get_item(item_id: int = Path(ge=1)):
    return {"item_id": item_id}
```

Appelez à nouveau `GET /items/-1`. Regardez aussi `/docs` : la contrainte y apparaît.

---

## Étape 2 — Query parameters (15 min)

Écrivez une route `GET /items` qui accepte :

- `skip` : entier, défaut `0`, minimum `0` ;
- `limit` : entier, défaut `20`, maximum `100` ;
- `q` : chaîne optionnelle (recherche dans le titre) ;
- `disponible` : booléen optionnel.

Pour l'instant, renvoyez simplement les paramètres reçus. Le but est de valider votre
compréhension de la signature.

```python
from fastapi import Query


@app.get("/items")
def list_items(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    q: str | None = None,
    disponible: bool | None = None,
):
    return {"skip": skip, "limit": limit, "q": q, "disponible": disponible}
```

**Testez :**

```bash
curl "http://localhost:8000/items"
curl "http://localhost:8000/items?limit=5&q=velo"
curl "http://localhost:8000/items?limit=500"      # attendu : 422
curl "http://localhost:8000/items?disponible=oui" # que se passe-t-il ?
```

La dernière : FastAPI accepte `true`, `false`, `1`, `0`, `yes`, `no`, `on`, `off` pour un booléen.
Testez `disponible=peut-etre` pour voir l'erreur.

---

## Étape 3 — Modèles Pydantic et création (20 min)

Créez `app/schemas/item.py` :

```python
from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    titre: str = Field(min_length=3, max_length=120)
    description: str | None = Field(default=None, max_length=1000)
    tarif_jour: float = Field(gt=0)
    disponible: bool = True


class ItemRead(BaseModel):
    id: int
    titre: str
    description: str | None
    tarif_jour: float
    disponible: bool
```

Dans `main.py`, ajoutez un stockage en mémoire et la route de création :

```python
from app.schemas.item import ItemCreate, ItemRead

FAKE_DB: dict[int, dict] = {}
_next_id = 1


@app.post("/items", response_model=ItemRead, status_code=201)
def create_item(payload: ItemCreate):
    global _next_id
    item = {"id": _next_id, **payload.model_dump()}
    FAKE_DB[_next_id] = item
    _next_id += 1
    return item
```

**Testez depuis `/docs`** (plus rapide que curl pour un POST) :

1. créez un item valide → vérifiez le code `201` et le corps renvoyé ;
2. créez un item avec `"titre": "ab"` → lisez attentivement le `422` ;
3. créez un item avec `"tarif_jour": 0` → même chose ;
4. créez un item avec un champ en trop, `"couleur": "rouge"` → que se passe-t-il ?

Le point 4 mérite une réponse : par défaut, Pydantic **ignore silencieusement** les champs
inconnus. Si vous voulez les refuser explicitement :

```python
from pydantic import BaseModel, ConfigDict


class ItemCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ...
```

Essayez ce comportement et gardez `extra="forbid"` : c'est le comportement que je préfère pour une API — un
client qui envoie un champ mal orthographié doit être averti, pas ignoré.

---

## Étape 4 — Lecture, mise à jour, suppression (25 min)

Complétez le CRUD. Contraintes précises :

| Route | Code succès | Comportement |
|---|---|---|
| `GET /items` | `200` | Renvoie la liste filtrée par `q`/`disponible`, tronquée par `skip`/`limit` |
| `GET /items/{item_id}` | `200` | `404` si l'item n'existe pas |
| `PUT /items/{item_id}` | `200` | Remplace tous les champs modifiables ; `404` si absent |
| `PATCH /items/{item_id}` | `200` | Modifie seulement les champs fournis ; `404` si absent |
| `DELETE /items/{item_id}` | `204` | Aucun corps de réponse ; `404` si absent |

Quelques indices :

```python
from fastapi import HTTPException


@app.get("/items/{item_id}", response_model=ItemRead)
def get_item(item_id: int = Path(ge=1)):
    item = FAKE_DB.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} introuvable")
    return item
```

Pour le `PATCH`, il vous faut un schéma dédié où **tout est optionnel** :

```python
class ItemUpdate(BaseModel):
    titre: str | None = Field(default=None, min_length=3, max_length=120)
    description: str | None = Field(default=None, max_length=1000)
    tarif_jour: float | None = Field(default=None, gt=0)
    disponible: bool | None = None
```

et la mise à jour n'applique que ce qui a été réellement transmis :

```python
data = payload.model_dump(exclude_unset=True)
item.update(data)
```

Comprenez bien `exclude_unset=True` : sans lui, un `PATCH {"titre": "X"}` écraserait
`description` avec `None`, parce que le champ existe dans le modèle avec la valeur par défaut
`None`. C'est un bug classique — et un bug que les agents produisent régulièrement.

Pour le `DELETE`, précisez le code et l'absence de corps :

```python
from fastapi import Response


@app.delete("/items/{item_id}", status_code=204, response_class=Response)
def delete_item(item_id: int = Path(ge=1)):
    if item_id not in FAKE_DB:
        raise HTTPException(status_code=404, detail=f"Item {item_id} introuvable")
    del FAKE_DB[item_id]
```

**Vérifiez chacun des cas d'erreur**, pas seulement les cas nominaux. Vous automatiserez ensuite
ces vérifications dans la séance suivante.

---

## Étape 5 — Découpage en routers (15 min)

Votre `main.py` commence à grossir. Déplacez tout ce qui concerne `items` dans
`app/routers/items.py` :

```python
# app/routers/items.py
from fastapi import APIRouter, HTTPException, Path, Query

from app.schemas.item import ItemCreate, ItemRead, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])

FAKE_DB: dict[int, dict] = {}


@router.get("", response_model=list[ItemRead])
def list_items(...):
    ...
```

Attention : avec `prefix="/items"`, le chemin de la route de liste devient `""` et non `"/items"`.

`main.py` se réduit à :

```python
from fastapi import FastAPI

from app.routers import items

app = FastAPI(title="GearShare API", version="0.1.0")
app.include_router(items.router)


@app.get("/health", tags=["monitoring"])
def health():
    return {"status": "ok"}
```

**Vérifiez** que toutes vos routes fonctionnent encore et que `/docs` les regroupe désormais sous
le tag `items`.

---

## Étape 6 — Faire produire une ressource par Copilot (20 min)

C'est le cœur agentic de ce TP. Vous allez demander à Copilot la ressource `reservations`, **sans
l'écrire vous-même**, puis la reviewer.

### 6.1. Écrivez la spécification d'abord

Dans un fichier `SPEC-reservations.md` à la racine du TP, rédigez le contrat. Modèle attendu :

```markdown
# Ressource : reservations

Fichiers : `app/schemas/reservation.py`, `app/routers/reservations.py`
Stockage : dictionnaire en mémoire dans le router (comme `items`)

## Schémas
- `ReservationCreate` : item_id (int, >= 1), date_debut (date), date_fin (date)
- `ReservationRead` : id, item_id, date_debut, date_fin, statut ("active" | "annulee")

## Routes (préfixe /reservations, tag "reservations")
- POST ""              → 201, ReservationRead. 422 si date_fin <= date_debut.
- GET  ""              → 200, list[ReservationRead]. Query : item_id optionnel, limit (défaut 20, max 100).
- GET  "/{reservation_id}" → 200, ReservationRead. 404 si absente.
- POST "/{reservation_id}/annuler" → 200, ReservationRead avec statut "annulee".
                                     404 si absente, 409 si déjà annulée.

## Contraintes
- Aucun accès à FAKE_DB de items.
- response_model sur toutes les routes.
- Pas de logique de validation en `if` dans le router : tout ce qui peut l'être dans Pydantic.
```

Notez la validation croisée « `date_fin > date_debut` » : elle ne s'exprime pas avec un simple
`Field`. C'est un point intéressant à confier à l'agent — regardez comment il s'en sort.

### 6.2. Demandez la génération

Ouvrez le **chat Copilot en mode Plan**, joignez `SPEC-reservations.md` au contexte ainsi que
`app/routers/items.py` (pour qu'il calque le style), et demandez le plan. **Lisez le plan avant
d'accepter.** Puis faites générer le code.

### 6.3. Reviewez

Remplissez ce tableau dans un fichier `REVIEW.md` :

| Point de contrôle | OK / KO | Ce que j'ai corrigé |
|---|---|---|
| Les codes de statut correspondent à la spec (201, 404, 409) | | |
| `response_model` présent sur les 4 routes | | |
| La validation `date_fin > date_debut` est bien dans le schéma Pydantic | | |
| Le router n'accède pas au stockage de `items` | | |
| Pas d'`async def` sans `await` | | |
| Aucune dépendance ajoutée dans `requirements.txt` (ou justifiée) | | |
| Les routes littérales sont déclarées avant les routes paramétrées | | |
| Le code renvoie une réponse cohérente pour `POST /reservations/999/annuler` | | |

Pour la validation croisée, la bonne réponse ressemble à ceci — comparez avec ce que l'agent a
produit :

```python
from pydantic import BaseModel, model_validator


class ReservationCreate(BaseModel):
    item_id: int = Field(ge=1)
    date_debut: date
    date_fin: date

    @model_validator(mode="after")
    def check_dates(self):
        if self.date_fin <= self.date_debut:
            raise ValueError("date_fin doit être postérieure à date_debut")
        return self
```

Une `ValueError` levée dans un validateur Pydantic est transformée par FastAPI en réponse `422`.
Si votre agent a écrit un `if` dans le router avec un `HTTPException(400)`, ce n'est pas faux
fonctionnellement, mais ce n'est pas la spec — et la contrainte n'apparaît pas dans la
documentation OpenAPI. **Corrigez-le.**

---

## Ce que vous devez me rendre à la fin de la séance 1

Poussez votre projet issu de `projet-demo/` sur un dépôt Git (un par groupe) contenant :

1. **Une API fonctionnelle** : `docker compose up` démarre, `/docs` liste les deux ressources
   `items` et `reservations`.
2. **Le CRUD complet sur `items`**, avec les bons codes de statut et les cas d'erreur gérés.
3. **`SPEC-reservations.md`** : la spécification que vous avez donnée à l'agent.
4. **`REVIEW.md`** : le tableau de review rempli, avec vos corrections. C'est le livrable que je
   regarderai le plus attentivement — une review qui dit « tout OK » sur les huit lignes me dira
   surtout que vous ne l'avez pas faite.

## Pour aller plus loin (si vous avez fini en avance)

- Ajoutez une route `GET /items/search?q=...` et vérifiez qu'elle n'est pas capturée par
  `GET /items/{item_id}`. Inversez volontairement l'ordre de déclaration pour observer le bug.
- Ajoutez un gestionnaire d'exception global pour une exception métier `ReservationConflict`
  renvoyant `409`, et faites-le utiliser par la route d'annulation à la place de l'`HTTPException`.
- Ajoutez `summary`, `description` et `responses` sur vos routes, et comparez le rendu de `/docs`
  avant/après.
