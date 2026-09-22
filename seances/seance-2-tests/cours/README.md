# Cours — Séance 2 : tester une API (2h)

Après la séance API, vous avez vérifié votre travail à la main
Cela fonctionne tant que le projet tient dans votre tête et que vous êtes seuls dessus.

Les tests automatisés existent pour le moment où ce n'est plus vrai : quand vous serez cinq à
modifier le même code, quand vous reviendrez dessus dans trois semaines, et quand vous devrez
changer une route sans casser les autres. Une vérification manuelle ne se rejoue pas ; un test,
si.

Cette séance s'appuie exclusivement sur ce que vous avez construit en séance 1 : une API FastAPI
avec deux ressources, `items` et `reservations`, et un stockage en mémoire. Pas de base de données,
pas d'authentification. Vous verrez comment tester ces deux briques quand elles arriveront, en
séance 4 puis en séance 5, avec les mêmes outils qu'aujourd'hui.

- [Cours — Séance 2 : tester une API (2h)](#cours--séance-2--tester-une-api-2h)
  - [Objectifs pédagogiques](#objectifs-pédagogiques)
  - [1. Pourquoi tester, et quoi tester](#1-pourquoi-tester-et-quoi-tester)
    - [1.1. La pyramide des tests](#11-la-pyramide-des-tests)
    - [1.2. Écrire le test avant le code](#12-écrire-le-test-avant-le-code)
  - [2. pytest : les bases](#2-pytest--les-bases)
    - [2.1. Un premier test](#21-un-premier-test)
    - [2.2. Lancer pytest](#22-lancer-pytest)
  - [3. TestClient, fixtures et stockage](#3-testclient-fixtures-et-stockage)
    - [3.1. TestClient](#31-testclient)
    - [3.2. Une fixture, c'est de l'injection de dépendances](#32-une-fixture-cest-de-linjection-de-dépendances)
    - [3.3. `yield` : préparer, puis nettoyer](#33-yield--préparer-puis-nettoyer)
    - [3.4. Isoler l'état en mémoire : la fixture `storage`](#34-isoler-létat-en-mémoire--la-fixture-storage)
    - [3.5. Composer : un item prêt à l'emploi](#35-composer--un-item-prêt-à-lemploi)
    - [3.6. Le scope](#36-le-scope)
    - [3.7. `autouse` : l'alternative implicite](#37-autouse--lalternative-implicite)
  - [4. Écrire un bon test](#4-écrire-un-bon-test)
    - [4.1. Le motif Given/When/Then](#41-le-motif-givenwhenthen)
    - [4.2. Tester une exception](#42-tester-une-exception)
    - [4.3. La paramétrisation](#43-la-paramétrisation)
    - [4.4. Tester un schéma Pydantic sans HTTP](#44-tester-un-schéma-pydantic-sans-http)
    - [4.5. Et quand la base et l'authentification arriveront ?](#45-et-quand-la-base-et-lauthentification-arriveront-)
  - [5. Que faut-il tester ?](#5-que-faut-il-tester-)
  - [6. Mocker, et quand ne pas le faire](#6-mocker-et-quand-ne-pas-le-faire)
    - [6.1. Décider entre réel et mock](#61-décider-entre-réel-et-mock)
    - [6.2. `monkeypatch` et `Mock`](#62-monkeypatch-et-mock)
    - [6.3. Les mocks qui trompent](#63-les-mocks-qui-trompent)
  - [7. La couverture](#7-la-couverture)
  - [8. Les tests qui ne testent rien](#8-les-tests-qui-ne-testent-rien)
  - [9. Synthèse](#9-synthèse)

## Objectifs pédagogiques

À la fin de ce cours, vous devez être capables de :

- expliquer ce qu'apporte un test automatisé et distinguer test unitaire, d'intégration et
  fonctionnel ;
- tester une API FastAPI avec `TestClient` et isoler son état en mémoire entre deux tests ;
- écrire des fixtures pytest : un client, un stockage remis à zéro, des données prêtes à l'emploi ;
- écrire des tests lisibles (motif Given/When/Then) et paramétrés ;
- tester un schéma Pydantic directement, sans passer par HTTP ;
- tester les cas d'erreur, pas seulement le cas nominal ;
- remplacer une dépendance non maîtrisée par un mock, et reconnaître un mock qui ne teste rien ;
- mesurer et interpréter une couverture de code, sans en faire un objectif aveugle ;
- reconnaître un test qui ne teste rien, et prouver qu'un test protège bien une règle.

## 1. Pourquoi tester, et quoi tester

Un test automatisé est un bout de code qui exécute votre application et vérifie qu'elle fait ce
qu'on attend. Ce qu'il vous apporte réellement :

| Bénéfice | Concrètement |
|---|---|
| **Non-régression** | Vous modifiez le `PATCH` d'un item, la suite vous dit ce que vous avez cassé |
| **Documentation exécutable** | `test_annuler_deux_fois_renvoie_409` décrit une règle métier, et prouve qu'elle est appliquée |
| **Confiance pour refactorer** | Sans tests, on n'ose pas toucher au code qui marche — et la dette s'accumule |
| **Feedback rapide** | Trois secondes de suite de tests contre dix minutes de clics dans Swagger |

### 1.1. La pyramide des tests

```text
          ╱╲          E2E / fonctionnels
         ╱  ╲         lents, fragiles, mais proches du réel
        ╱────╲
       ╱      ╲       Intégration
      ╱        ╲      plusieurs composants ensemble (routes + stockage)
     ╱──────────╲
    ╱            ╲    Unitaires
   ╱______________╲   rapides, nombreux, isolés
```

- **Unitaire** : une fonction, une classe, isolée. Rapide (millisecondes). Exemple aujourd'hui :
  le validateur `date_fin > date_debut` de `ReservationCreate`, testé sans lancer l'API.
- **Intégration** : plusieurs composants ensemble. Exemple : `POST /reservations` traverse le
  router, le schéma Pydantic et le stockage. C'est le niveau où vous passerez le plus de temps
  sur ce projet. Aujourd'hui le stockage est un dictionnaire ; en séance 4, ce sera PostgreSQL,
  et vos tests garderont la même forme.
- **E2E** : l'application complète, du frontend à la base. Lent et fragile ; on en garde très peu.

La forme pyramidale exprime une règle de proportion : beaucoup de tests rapides, peu de tests
lents. L'anti-pattern inverse — le « cornet de glace », plein de tests E2E — donne une suite qui
met vingt minutes et échoue au hasard, donc que plus personne ne regarde.

Pour votre projet, une répartition raisonnable : quelques tests unitaires sur les règles non
triviales (validation croisée, calculs, et plus tard les règles métier des services), et
l'essentiel en tests d'intégration sur les routes.

### 1.2. Écrire le test avant le code

Quand vous écrivez le code d'abord, vos tests confirment ce que vous savez déjà : vous testez ce
que vous avez fait, pas ce qu'il fallait faire. L'ordre inverse change trois choses :

1. Formuler un test vous force à définir précisément le comportement attendu : quel code de
   statut, quel corps, dans quel cas. Les tableaux de codes que vous avez remplis à la main en
   séance 1 sont déjà des plans de tests.
2. La suite de tests devient un critère d'acceptation objectif : « c'est fini quand tout est vert »
   au lieu de « ça a l'air de marcher ». C'est ce qui permet à cinq personnes de travailler sur le
   même dépôt sans se marcher dessus.
3. La boucle de correction se raccourcit : vous lancez la suite, un test est rouge, vous savez
   exactement quelle règle est cassée et où.

C'est le principe du **TDD** (*Test-Driven Development*). Vous n'êtes pas obligés de l'appliquer à
la lettre ; en revanche, sur ce projet, aucune route ne sera considérée comme terminée sans ses
tests, nominaux et d'erreur.

## 2. pytest : les bases

### 2.1. Un premier test

```text
projet/
├── app/
│   ├── main.py
│   ├── routers/
│   └── schemas/
└── tests/
    ├── conftest.py
    ├── test_health.py
    ├── test_items.py
    └── test_reservations.py
```

```python
# tests/test_health.py
from fastapi.testclient import TestClient

from app.main import app


def test_health_retourne_ok() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

Les conventions pytest : fichiers `test_*.py`, fonctions `test_*`, classes `Test*`. Pas de classe
obligatoire, pas d'héritage, un `assert` Python standard. Quand un `assert` échoue, pytest affiche
les deux valeurs comparées : c'est tout ce dont vous avez besoin pour comprendre l'échec.

### 2.2. Lancer pytest

```bash
pytest                      # tout
pytest -v                   # une ligne par test
pytest tests/test_items.py  # un fichier
pytest -k "patch"           # les tests dont le nom contient "patch"
pytest -x                   # s'arrête au premier échec
pytest --lf                 # relance seulement les derniers échecs
```

`pytest -x --lf` est la combinaison que vous utiliserez le plus en développement. Dans votre
projet, tout cela s'exécute dans le conteneur : `docker compose run --rm api pytest`.

## 3. TestClient, fixtures et stockage

Avant d'écrire de bons tests, il faut résoudre un problème de plomberie : comment appeler l'API, et
comment garantir que chaque test part d'un état connu. C'est le rôle de cette section — tout ce qui
suit dans le cours s'appuie sur les trois fixtures qu'elle construit : `client`, `storage` et
`item_velo`.

### 3.1. TestClient

```python
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
response = client.get("/items", params={"limit": 5})
response = client.post("/items", json={"titre": "Vélo de ville", "tarif_jour": 8.5})
response = client.patch("/items/1", json={"titre": "Vélo pliant"})
response = client.delete("/items/1")
```

`TestClient` appelle l'application **en mémoire**, sans serveur ni réseau : pas d'uvicorn, pas de
port, pas de conteneur à démarrer. C'est rapide et reproductible. Il expose la même interface que
`httpx` (`params`, `json`, `headers`), et la réponse a un `status_code` et un `json()`.

Ce que vous testez avec lui, c'est le **contrat HTTP** : ce qu'un client peut observer. Une
requête, un code de statut, un corps. Pas l'intérieur du dictionnaire de stockage.

### 3.2. Une fixture, c'est de l'injection de dépendances

Le test de la section 2.1 construit son propre `TestClient`. Dix tests plus tard, vous aurez écrit
dix fois la même ligne. Une **fixture** est une fonction qui prépare quelque chose dont plusieurs
tests ont besoin :

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
```

```python
# tests/test_health.py
from fastapi.testclient import TestClient


def test_health_retourne_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
```

Un test qui déclare `client` en paramètre le reçoit automatiquement : pytest voit le nom, trouve la
fixture, l'appelle, et passe le résultat. C'est de l'**injection de dépendances** — le même
principe que le `Depends` de FastAPI que vous verrez en séance 4.

`conftest.py` est le fichier de fixtures partagées : tout ce qu'il contient est visible par les
tests du même dossier et des sous-dossiers, sans import.

Cette version de `client` est encore incomplète : elle ne garantit pas que l'API soit vide au début
du test. On la termine en section 3.4, après un détour par `yield`.

### 3.3. `yield` : préparer, puis nettoyer

```python
from collections.abc import Iterator
from pathlib import Path


@pytest.fixture
def fichier_temporaire(tmp_path: Path) -> Iterator[Path]:
    chemin = tmp_path / "export.csv"
    chemin.write_text("id;titre\n")
    yield chemin              # le test s'exécute ici
    chemin.unlink()           # nettoyage, même si le test a échoué
```

Tout ce qui précède le `yield` est la préparation ; tout ce qui suit est le nettoyage, exécuté quoi
qu'il arrive. `tmp_path` est une fixture fournie par pytest : un dossier temporaire propre pour
chaque test. Vous en verrez d'autres du même genre, comme `monkeypatch` en section 6.

### 3.4. Isoler l'état en mémoire : la fixture `storage`

Votre API de la séance 1 stocke ses données dans des dictionnaires de module :

```python
# app/routers/items.py
from typing import Any

FAKE_DB: dict[int, dict[str, Any]] = {}
_next_id: int = 1
```

Ces variables vivent aussi longtemps que le processus Python — donc aussi longtemps que la suite de
tests. Sans précaution, le premier test qui crée un item laisse un item derrière lui, et le
deuxième test ne trouve plus une liste vide. Il passe si on le lance seul, il échoue si on lance
la suite : c'est le symptôme classique d'une suite qui **dépend de l'ordre d'exécution**.

**Première chose à faire, côté application** : supprimer le compteur global. Un identifiant se
déduit du dictionnaire lui-même :

```python
# app/routers/items.py
from typing import Any

FAKE_DB: dict[int, dict[str, Any]] = {}


def _next_id() -> int:
    return max(FAKE_DB, default=0) + 1
```

Il ne reste plus qu'**un seul** état par ressource : le dictionnaire. Le vider suffit à repartir de
zéro. Faites la même chose dans `reservations`. Ce n'est pas qu'une commodité de test : un
`global` modifié depuis une route est un état difficile à suivre et à réinitialiser.

**Deuxième chose, côté tests** : une classe `Storage` qui tient tous les dictionnaires de l'API et
sait les remettre à zéro, et une fixture qui l'expose.

```python
# tests/conftest.py
from collections.abc import Iterator
from dataclasses import dataclass, fields
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import items, reservations


@dataclass
class Storage:
    """Poignée sur l'état en mémoire de l'API, réservée aux tests."""

    items: dict[int, dict[str, Any]]
    reservations: dict[int, dict[str, Any]]

    def reset_all(self) -> None:
        for field in fields(self):
            getattr(self, field.name).clear()


@pytest.fixture
def storage() -> Iterator[Storage]:
    storage = Storage(items=items.FAKE_DB, reservations=reservations.FAKE_DB)
    storage.reset_all()
    yield storage
    storage.reset_all()


@pytest.fixture
def client(storage: Storage) -> TestClient:
    return TestClient(app)
```

Lisez ce fichier de haut en bas, il contient toute l'idée :

- `Storage` référence les **vrais** dictionnaires des routers, pas des copies. `clear()` vide donc
  l'état que l'API utilise. `reset_all()` parcourt les attributs de la dataclass : quand vous
  ajouterez une ressource `avis` en séance 7, un attribut de plus suffira, sans toucher à la
  méthode ni à la fixture.
- La fixture `storage` remet à zéro **avant** le test (un test précédent a pu planter avant son
  nettoyage), rend la poignée, puis remet à zéro **après**.
- `client` **dépend de** `storage`. Tout test qui passe par HTTP reçoit donc un état vide sans
  avoir à le demander. Rien dans le code de l'application ne sait que les tests existent : pas de
  route de reset, pas de fonction réservée aux tests dans les routers.

Les tests qui ont **besoin du stockage lui-même** le déclarent en paramètre. Ils sont rares, et ce
sont toujours des tests où le contrat HTTP ne suffit pas à décrire le `Given` ou le `Then` :

```python
def test_lister_avec_skip_saute_les_premiers(client: TestClient, storage: Storage) -> None:
    # Given : cinquante items, insérés sans passer par cinquante requêtes HTTP.
    for i in range(1, 51):
        storage.items[i] = {"id": i, "titre": f"Item {i}", "description": None,
                            "tarif_jour": 5.0, "disponible": True}

    response = client.get("/items", params={"skip": 40, "limit": 20})

    assert [item["id"] for item in response.json()] == list(range(41, 51))
```

C'est le cas légitime : préparer un volume de données en une boucle plutôt qu'en cinquante `POST`.
Gardez la règle de la section 3.1 en tête : **`storage` sert à préparer et à constater, pas à
contourner l'API**. Un test qui fait tout son `When` dans `storage.items` ne teste plus une API ;
un test qui vérifie `item_id not in storage.items` après un `DELETE` vérifie moins bien que
`GET /items/{id}` → `404`, qui teste ce que le client verra.

Ce que vous faites là a un nom : vous rendez l'état du système **contrôlable depuis les tests**.
En séance 4, la base PostgreSQL remplacera les dictionnaires ; la fixture s'appellera `db`, rendra
une session SQLAlchemy dans une transaction annulée, et `client` en dépendra de la même façon. La
forme ne change pas.

### 3.5. Composer : un item prêt à l'emploi

Une fixture peut en demander une autre. Beaucoup de tests commencent par « étant donné un item
existant » ; factorisez ce `Given` :

```python
@pytest.fixture
def item_velo(client: TestClient) -> dict[str, Any]:
    """Un item déjà créé, renvoyé tel que l'API l'expose."""
    response = client.post("/items", json={
        "titre": "Vélo de ville", "description": "Trois vitesses", "tarif_jour": 8.5,
    })
    assert response.status_code == 201
    return response.json()
```

`item_velo` demande `client`, qui demande `storage` : la chaîne est résolue par pytest, dans le
bon ordre. Un test qui déclare `item_velo` reçoit un item existant dans une API par ailleurs vide,
et ne contient plus que son `When` et son `Then`.

L'`assert` dans une fixture n'est pas un test : c'est une garde. Si la création échoue, vous voulez
que la fixture le dise, pas que vingt tests échouent avec un message obscur.

### 3.6. Le scope

Le **scope** contrôle la fréquence de création d'une fixture :

| Scope | Créée |
|---|---|
| `function` (défaut) | À chaque test |
| `class` | Une fois par classe |
| `module` | Une fois par fichier |
| `session` | Une fois pour toute la suite |

Le défaut, `function`, est le bon choix tant que la préparation est rapide — et pour un
`TestClient` sur une API en mémoire, elle l'est. Vous élargirez le scope en séance 4 pour ce qui
coûte cher, comme la création du schéma de la base de test, et pas avant. Surtout, ne mettez jamais
`storage` en scope `module` ou `session` : vous réintroduiriez exactement la dépendance à l'ordre
que la section 3.4 vient de supprimer.

### 3.7. `autouse` : l'alternative implicite

```python
@pytest.fixture(autouse=True)
def reset_storage() -> Iterator[None]:
    storage = Storage(items=items.FAKE_DB, reservations=reservations.FAKE_DB)
    storage.reset_all()
    yield
    storage.reset_all()
```

Une fixture `autouse=True` s'applique à tous les tests de sa portée sans qu'ils la déclarent.
C'est simple et impossible à oublier. Son défaut est le revers de sa qualité : rien dans la
signature d'un test ne dit qu'il dépend de cet état, et les tests qui n'en ont pas besoin (ceux
d'un schéma Pydantic, section 4.4) paient quand même la remise à zéro. Le montage de la section
3.4 — `client` dépend de `storage` — dit la même chose explicitement ; c'est celui que je vous
recommande, et celui du TP.

Règle d'or, quelle que soit l'approche : **chaque test doit être indépendant**. Si `test_b` ne
passe que parce que `test_a` a créé un item avant lui, votre suite cassera dès qu'on lancera les
tests dans un autre ordre, en parallèle, ou avec `-k` sur un seul d'entre eux.

## 4. Écrire un bon test

Vous avez maintenant `client`, `storage` et `item_velo`. Voyons ce qu'on écrit avec.

### 4.1. Le motif Given/When/Then

Un test répond à une histoire courte et vérifiable :

- **Given** : dans quel état connu se trouve le système ?
- **When** : quelle action exerce-t-on ?
- **Then** : quel résultat observable doit-on obtenir ?

Ce motif résout deux problèmes fréquents : un lecteur comprend immédiatement la règle couverte, et
un test n'échoue que pour une raison identifiable. Il ne s'agit pas d'ajouter trois commentaires à
chaque test : utilisez-les lorsque les trois étapes ne sont pas évidentes dans le code.

```python
def test_annuler_une_reservation_deja_annulee_renvoie_409(client: TestClient, item_velo: dict[str, Any]) -> None:
    # Given : une réservation existe et a déjà été annulée.
    creation = client.post("/reservations", json={
        "item_id": item_velo["id"], "date_debut": "2026-09-01", "date_fin": "2026-09-05",
    })
    reservation_id = creation.json()["id"]
    client.post(f"/reservations/{reservation_id}/annuler")

    # When : on demande une seconde annulation.
    response = client.post(f"/reservations/{reservation_id}/annuler")

    # Then : l'API refuse avec un conflit, et la réservation reste annulée.
    assert response.status_code == 409
    assert client.get(f"/reservations/{reservation_id}").json()["statut"] == "annulee"
```

Le `Given` est ici assez long pour mériter sa propre fixture : dès qu'un second test commence
par « une réservation existe », créez `reservation_active` sur le modèle de `item_velo`.

Pour une route HTTP, le `Then` vérifie le code, puis la partie utile du corps de réponse. Pas tout
le corps : vérifier vingt champs, c'est vingt raisons de casser le test pour une raison qui n'a
rien à voir avec ce qu'il teste.

Sur le nommage : `test_annuler_une_reservation_deja_annulee_renvoie_409` vous dit ce qui a cassé
sans ouvrir le fichier. `test_reservation_2` ne vous dit rien. Vos noms de tests seront lus le jour
où la suite est rouge et où vous cherchez pourquoi — écrivez-les pour ce jour-là.

### 4.2. Tester une exception

Un test d'exception regroupe naturellement `When` et `Then` dans `pytest.raises` : l'appel est
l'action, l'exception attendue est le résultat.

```python
from datetime import date

import pytest
from pydantic import ValidationError

from app.schemas.reservation import ReservationCreate


def test_dates_inversees_sont_refusees_par_le_schema() -> None:
    with pytest.raises(ValidationError, match="date_fin"):
        ReservationCreate(item_id=1, date_debut=date(2026, 9, 5), date_fin=date(2026, 9, 1))
```

Ce test ne passe pas par HTTP : il instancie directement le schéma Pydantic écrit en séance 1. C'est un test **unitaire**, et c'est exactement ce que vous voulez pour une règle de
validation : rapide, précis, sans bruit. Il ne déclare ni `client` ni `storage` — il n'en a pas
besoin, et il ne paie donc aucune préparation.

`match` vérifie le message par expression régulière. Utile, mais ne le rendez pas trop strict :
un test qui casse parce que vous avez corrigé une faute de frappe dans un message est un test qui
coûte plus qu'il ne rapporte.

### 4.3. La paramétrisation

Un même test, plusieurs jeux de données :

```python
@pytest.mark.parametrize(
    ("payload", "champ_en_erreur"),
    [
        ({"titre": "ab", "tarif_jour": 8.5}, "titre"),                   # trop court
        ({"titre": "Vélo de ville", "tarif_jour": 0}, "tarif_jour"),      # nul
        ({"titre": "Vélo de ville", "tarif_jour": -3}, "tarif_jour"),     # négatif
        ({"titre": "Vélo de ville"}, "tarif_jour"),                       # manquant
        ({"titre": "Vélo de ville", "tarif_jour": 8.5, "couleur": "rouge"}, "couleur"),  # inconnu
    ],
)
def test_creation_item_invalide_renvoie_422(
    client: TestClient, payload: dict[str, Any], champ_en_erreur: str
) -> None:
    response = client.post("/items", json=payload)

    assert response.status_code == 422
    champs = [erreur["loc"][-1] for erreur in response.json()["detail"]]
    assert champ_en_erreur in champs
```

Cinq cas, un seul test, cinq lignes de résultat dans la sortie pytest. Ce sont exactement les
essais que vous avez faits à la main dans `/docs` en séance 1 — les voilà automatisés, et ils
resteront là quand vous aurez oublié de les refaire.

La seconde assertion mérite un mot : elle ne vérifie pas le message d'erreur de Pydantic (qui peut
changer d'une version à l'autre), mais **quel champ** est en cause. C'est l'information utile, et
elle est stable.

Le dernier cas (champ inconnu) traduit une **décision** que vous avez prise en séance 1 avec
`extra="forbid"`. Votre test la rend explicite et la protège : quiconque retire cette ligne en
« nettoyant » le schéma fera passer ce test au rouge.

### 4.4. Tester un schéma Pydantic sans HTTP

Une bonne partie de votre logique de séance 1 vit dans les schémas : bornes de `Field`,
`extra="forbid"`, le `model_validator` sur les dates. Tout cela se teste directement, comme en
section 4.2 :

```python
def test_reservation_valide_est_acceptee() -> None:
    reservation = ReservationCreate(item_id=1, date_debut=date(2026, 9, 1), date_fin=date(2026, 9, 5))

    assert reservation.date_fin > reservation.date_debut


def test_item_update_sans_champ_est_vide() -> None:
    assert ItemUpdate().model_dump(exclude_unset=True) == {}
```

Le second test protège le comportement du `PATCH` : c'est `exclude_unset=True` qui évite d'écraser
`description` avec `None`. Un test d'intégration sur `PATCH /items/1` le vérifie aussi, de plus
loin ; les deux se complètent.

Quand testez-vous par HTTP, quand testez-vous le schéma directement ? Le contrat (codes, corps,
routes) par HTTP ; les règles de validation fines, avec leurs nombreux cas, directement sur le
schéma — c'est plus rapide à écrire, à lire et à exécuter.

### 4.5. Et quand la base et l'authentification arriveront ?

Deux briques manquent encore à votre API, et elles changent la manière de préparer un test :

- **En séance 4**, PostgreSQL remplace les dictionnaires. `storage` devient `db` : une session de
  base de test dans une transaction annulée, injectée dans l'application par
  `app.dependency_overrides`. Vous apprendrez aussi à tester une règle métier dans un service,
  sans passer par HTTP. Tout cela est dans le cours de la séance 4, section « Tester l'application
  en couches ».
- **En séance 5**, les routes sensibles exigent un jeton. Vous ajouterez des fixtures
  `client_alice` et `client_bob` qui portent chacune un jeton valide, et chaque ligne de votre
  matrice d'autorisation deviendra un test.

Retenez le point commun : **la forme des tests ne change pas**. `TestClient`, Given/When/Then,
paramétrisation, fixtures dans `conftest.py`. Seule la préparation de l'état évolue.

## 5. Que faut-il tester ?

Cette grille résout le problème du « cela marche dans la démo » : elle vous oblige à transformer
chaque comportement observable et chaque erreur prévue en un test explicite.

Pour chaque route, au minimum :

| Catégorie | Exemple sur votre API de la séance 1 |
|---|---|
| **Cas nominal** | `POST /reservations` valide → `201`, la réservation est relisible par `GET` |
| **Validation** | `date_fin <= date_debut` → `422` ; `limit=500` → `422` ; `/items/abc` → `422` |
| **Ressource absente** | `GET /items/999` → `404` ; `POST /reservations/999/annuler` → `404` |
| **Conflit métier** | Annuler une réservation déjà annulée → `409` |
| **Effet de bord** | `DELETE /items/1` → `204`, puis `GET /items/1` → `404` |
| **Cas limites** | `PATCH` avec un seul champ : les autres sont inchangés ; `GET /items?skip=0&limit=1` |

Les catégories « non authentifié » (`401`) et « non autorisé » (`403`) s'ajouteront à cette grille
en séance 5. Gardez-lui une ligne libre.

Une règle simple pour vous cadrer : **pour chaque `raise HTTPException` de vos routers, il y a un
test.** Si votre router d'annulation lève un `404` et un `409`, il vous faut deux tests d'erreur.

Et ce qu'il ne faut **pas** tester :

- le framework (FastAPI convertit correctement `"42"` en `int`, ce n'est pas votre travail) ;
- des détails d'implémentation (« la route appelle bien `FAKE_DB.get()` ») : ces tests cassent à
  chaque refactoring sans jamais attraper de vrai bug ;
- le même comportement dix fois sous des angles à peine différents.

**Testez le comportement observable, pas la mécanique interne.** En séance 4, cette règle vous
permettra de remplacer les dictionnaires par PostgreSQL sans réécrire un seul test de contrat.

## 6. Mocker, et quand ne pas le faire

Un **mock** remplace une dépendance par un objet contrôlé. Il sert à isoler le comportement que
vous voulez tester d'un effet de bord non déterministe, lent, payant ou extérieur à votre projet.
Il ne sert pas à faire disparaître les composants que vous devriez réellement vérifier.

### 6.1. Décider entre réel et mock

| Élément | Choix | Pourquoi |
|---|---|---|
| Vos routes FastAPI et vos schémas Pydantic | Réel | Le contrat HTTP est le sujet du test |
| Votre stockage (dictionnaires aujourd'hui, PostgreSQL de test en séance 4) | Réel | C'est là que sont les bugs |
| Horloge, aléa, identifiants générés | Valeur contrôlée | Le résultat doit être reproductible |
| API d'e-mail, de paiement, service tiers | Mock | Appel externe, coûteux, lent ou indisponible en test |

Regardez votre API de la séance 1 avec cette grille : elle n'a **aucune dépendance externe**. Vous
n'avez donc rien à mocker aujourd'hui pour tester son contrat, et c'est le bon diagnostic — un
mock qu'on ajoute « par habitude » est un mock de trop.

Le TP vous fera néanmoins ajouter un effet de bord minuscule (une notification à l'annulation)
pour manipuler l'outil une fois, sur un cas où il est légitime.

### 6.2. `monkeypatch` et `Mock`

Deux outils, fournis en standard.

**`monkeypatch`** est une fixture pytest qui remplace un attribut, une variable d'environnement ou
un élément de dictionnaire pour la durée d'un test, et restaure l'original ensuite :

```python
from datetime import date
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.routers import reservations


def test_reservation_dans_le_passe_est_refusee(
    client: TestClient, item_velo: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    # Given : "aujourd'hui" est fixé, quel que soit le jour où la suite tourne.
    monkeypatch.setattr(reservations, "aujourd_hui", lambda: date(2026, 9, 10))

    response = client.post("/reservations", json={
        "item_id": item_velo["id"], "date_debut": "2026-09-01", "date_fin": "2026-09-05",
    })

    assert response.status_code == 422
```

Sans `monkeypatch`, ce test passerait aujourd'hui et échouerait dans un an : l'horloge est la
dépendance non déterministe la plus courante. Notez la condition : il faut que le code lise la date
via une fonction remplaçable (`aujourd_hui()`), et non `date.today()` en dur au milieu d'une
expression. Un code testable est un code dont les dépendances sont nommées.

**`Mock`** (module `unittest.mock`) crée un faux objet dont vous contrôlez le comportement et
dont vous pouvez inspecter les appels :

```python
from typing import Any
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.routers import reservations


def test_annulation_envoie_une_notification(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, reservation_active: dict[str, Any]
) -> None:
    notifier = Mock()
    monkeypatch.setattr(reservations, "envoyer_notification_annulation", notifier)

    response = client.post(f"/reservations/{reservation_active['id']}/annuler")

    assert response.status_code == 200
    notifier.assert_called_once_with(reservation_id=reservation_active["id"])
```

- `return_value` définit ce qu'une méthode renvoie ;
- `side_effect` permet de lever une exception ou de renvoyer plusieurs résultats successifs ;
- `assert_called_once_with(...)` vérifie que l'effet de bord a été demandé, avec les bons
  arguments, une seule fois.

Utilisez `MagicMock` seulement si votre dépendance doit supporter des méthodes spéciales Python,
par exemple un gestionnaire de contexte (`with`) ; dans la plupart des cas, `Mock` est plus
lisible.

`side_effect` sert à poser une question que le cas nominal ne pose jamais : **que fait votre API si
la dépendance échoue ?**

```python
def test_annulation_reussit_meme_si_la_notification_echoue(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, reservation_active: dict[str, Any]
) -> None:
    notifier = Mock(side_effect=ConnectionError("serveur mail injoignable"))
    monkeypatch.setattr(reservations, "envoyer_notification_annulation", notifier)

    response = client.post(f"/reservations/{reservation_active['id']}/annuler")

    assert response.status_code == 200
```

Ce test encode une décision : l'annulation est acquise même si la notification ne part pas.
L'inverse (renvoyer une erreur, ne pas annuler) est défendable aussi. Ce qui ne l'est pas, c'est de
ne pas avoir décidé — et de découvrir le comportement en production.

### 6.3. Les mocks qui trompent

Ne mockez **pas** votre propre stockage quand vous pouvez utiliser le vrai. Aujourd'hui, le vrai
est un dictionnaire remis à zéro par `storage` : il n'y a aucune raison de le simuler. En séance 4,
le vrai sera une base PostgreSQL de test, et la même règle s'appliquera : un test qui simule
l'accès aux données ne vérifie pas que la requête est correcte — or c'est précisément là que sont
les bugs.

Le piège absolu, que je retrouve chaque année dans des suites de tests :

```python
# ☠️ Ce test ne teste rien
def test_creer_item() -> None:
    client = Mock()
    client.post.return_value.status_code = 201

    response = client.post("/items", json={"titre": "Vélo", "tarif_jour": 8.5})

    assert response.status_code == 201
```

On a simulé la chose qu'on prétend tester, puis vérifié que la simulation renvoie ce qu'on lui a
dit de renvoyer. Ce test sera vert quoi qu'il arrive au code réel. Apprenez à le reconnaître : dès
que le sujet du test est lui-même un `Mock`, il y a un problème.

## 7. La couverture

```bash
pytest --cov=app --cov-report=term-missing
```

```text
Name                              Stmts   Miss  Cover   Missing
---------------------------------------------------------------
app/main.py                           8      0   100%
app/routers/items.py                 46      4    91%   58-61
app/routers/reservations.py          39      6    85%   44-49
app/schemas/reservation.py           14      0   100%
---------------------------------------------------------------
TOTAL                               107     10    91%
```

La colonne `Missing` est la seule qui vous intéresse vraiment : elle vous dit **quelles lignes** ne
sont jamais exécutées. Regardez-les une par une — souvent, c'est un `raise HTTPException` ou une
branche de filtre, c'est-à-dire précisément ce qu'on oublie de tester.

Mais gardez la mesure à sa place. **La couverture mesure l'exécution, pas la vérification.** Ce
test atteint 100 % de couverture sur la route et ne vérifie rien :

```python
def test_creer_item(client: TestClient) -> None:
    client.post("/items", json={"titre": "Vélo", "tarif_jour": 8.5})
    # aucun assert
```

À l'inverse, 75 % de couverture avec des tests qui vérifient réellement les règles vaut mieux que
95 % obtenus en exécutant du code sans rien affirmer. Un seuil de **70–80 %** est un objectif sain
pour votre projet ; au-delà, l'effort se déplace vers du code sans valeur.

Un seuil bloquant est utile :

```bash
pytest --cov=app --cov-fail-under=70
```

## 8. Les tests qui ne testent rien

Un test qui échoue attire l'attention. Un test inutile qui passe ne l'attire pas, et donne une
fausse assurance jusqu'au jour où la régression qu'il aurait dû détecter passe.

Les défauts que je vois le plus souvent :

| Défaut | À quoi ça ressemble |
|---|---|
| Test sans `assert` | Appelle la route, ne vérifie rien |
| Assertion tautologique | `assert response.json() == response.json()`, `assert True` |
| Mock du sujet testé | Le client ou la route testée est lui-même un `Mock` |
| Seulement le cas nominal | Aucun test de `404`, `409`, `422` |
| Tests dépendants | `test_02` suppose que `test_01` a créé l'item |
| Assertion trop faible | `assert response.status_code != 500` |
| Assertion trop rigide | Vérifie le message d'erreur exact, casse à la première reformulation |
| Fixture recréée partout | La même création d'item copiée dans dix tests, jamais factorisée |
| Test de l'implémentation | Vérifie que `storage.items` contient une clé, pas que `GET` renvoie l'item |

**Comment vérifier qu'un test teste vraiment** — c'est la technique la plus utile de cette séance,
et elle prend trente secondes :

> **Cassez volontairement le code, et vérifiez que le test devient rouge.**

Concrètement : votre route d'annulation renvoie `409` quand la réservation est déjà annulée ?
Commentez cette vérification et relancez les tests. Si tout reste vert, votre suite ne protège pas
cette règle — quel que soit son taux de couverture.

C'est le principe du **test de mutation** : on introduit un défaut et on regarde si la suite le
détecte. Faites-le à la main sur vos trois ou quatre règles les plus importantes. C'est un exercice
imposé du TP.

**La méthode pour écrire une suite qui tient**, en pratique :

1. Listez les cas à couvrir (nominal, erreurs, limites) **avant** d'écrire le premier test. C'est
   un travail de conception : chaque `raise` de vos routers et chaque contrainte de vos schémas
   est un cas.
2. Écrivez un test par cas, avec les fixtures existantes. Un seul `assert` principal par test, un
   nom qui dit ce qui est cassé quand il est rouge.
3. Relisez chaque `assert` comme si un autre l'avait écrit : que vérifie-t-il exactement ? Que
   se passe-t-il s'il est supprimé ?
4. Cassez le code pour vérifier que la suite le détecte.

## 9. Synthèse

- Les tests servent la non-régression, la documentation et le refactoring. Un test écrit avant le
  code fixe le comportement attendu avant l'implémentation.
- Beaucoup de tests rapides, peu de tests lents. Pour ce projet : l'essentiel en intégration sur
  les routes, quelques tests unitaires sur les schémas et les règles.
- `TestClient` appelle l'application en mémoire ; une classe `Storage` référence les dictionnaires
  de l'API et `reset_all()` les vide ; la fixture `storage` l'expose, `client` en dépend, et seuls
  les tests qui préparent un volume de données la déclarent.
- Les fixtures se composent (`item_velo` → `client` → `storage`), se nettoient avec `yield`, et
  restent en scope `function` tant que la préparation est rapide.
- pytest : motif Given/When/Then, noms explicites, `parametrize` pour les jeux de données, schémas
  Pydantic testés directement.
- Testez les cas d'erreur : **pour chaque `raise`, un test.**
- Mockez ce que vous ne contrôlez pas (horloge, service tiers) avec `monkeypatch` et `Mock` ; ne
  mockez jamais le sujet du test ni votre propre stockage.
- La couverture indique où regarder, elle ne mesure pas la qualité. 70–80 % est un bon objectif.
- Pour valider une suite : **cassez le code et vérifiez que ça devient rouge**.

Passez au [TP](../tp/README.md) : vous automatisez toutes les vérifications que vous avez faites
à la main en séance 1.

En séance 4, vous brancherez cette suite sur PostgreSQL et apprendrez à tester vos services. Vous
la ferez évoluer à chaque séance jusqu'au rendu final.
