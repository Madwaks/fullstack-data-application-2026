# Cours — Séance 1 : Les API et FastAPI (2h)

Vous savez faire tourner un conteneur (séance 0). Il est temps d'avoir quelque chose à faire
tourner dedans.

Cette séance pose les fondations techniques de tout le reste du module. Le backend que vous
construirez pour le projet est une API FastAPI ; la persistance, l'authentification et le frontend
viendront ensuite s'y greffer.

- [Cours — Séance 1 : Les API et FastAPI (2h)](#cours--séance-1--les-api-et-fastapi-2h)
  - [Objectifs pédagogiques](#objectifs-pédagogiques)
  - [1. Qu'est-ce qu'une API ?](#1-quest-ce-quune-api-)
    - [1.1. Le contrat](#11-le-contrat)
    - [1.2. Pourquoi c'est devenu incontournable](#12-pourquoi-cest-devenu-incontournable)
  - [2. HTTP, le protocole de base](#2-http-le-protocole-de-base)
    - [2.1. Anatomie d'une requête](#21-anatomie-dune-requête)
    - [2.2. Les méthodes](#22-les-méthodes)
    - [2.3. Les codes de statut](#23-les-codes-de-statut)
  - [3. REST](#3-rest)
    - [3.1. Le principe : des ressources, pas des actions](#31-le-principe--des-ressources-pas-des-actions)
    - [3.2. Les autres styles](#32-les-autres-styles)
  - [4. Les frameworks Python](#4-les-frameworks-python)
  - [5. Premiers pas avec FastAPI](#5-premiers-pas-avec-fastapi)
    - [5.1. Une application minimale](#51-une-application-minimale)
    - [5.2. ASGI : comment votre code est servi](#52-asgi--comment-votre-code-est-servi)
    - [5.3. Path parameters](#53-path-parameters)
    - [5.4. Query parameters](#54-query-parameters)
  - [6. Pydantic : la validation au cœur de FastAPI](#6-pydantic--la-validation-au-cœur-de-fastapi)
    - [6.1. Un modèle d'entrée](#61-un-modèle-dentrée)
    - [6.2. Un modèle de sortie](#62-un-modèle-de-sortie)
  - [7. Gérer les erreurs](#7-gérer-les-erreurs)
  - [8. Documentation automatique : OpenAPI](#8-documentation-automatique--openapi)
  - [9. Structurer : les routers](#9-structurer--les-routers)
  - [10. Faire produire une API par un agent](#10-faire-produire-une-api-par-un-agent)
  - [11. Synthèse](#11-synthèse)

## Objectifs pédagogiques

À la fin de ce cours, vous devez être capables de :

- expliquer ce qu'est une API REST et à quoi sert le contrat qu'elle définit ;
- choisir la bonne méthode HTTP et le bon code de statut pour une opération donnée ;
- écrire une application FastAPI avec des routes, des path/query parameters et des modèles Pydantic ;
- expliquer ce qu'est une application ASGI et comment un serveur (uvicorn, hypercorn…) l'exécute ;
- faire valider automatiquement les entrées et sérialiser proprement les sorties ;
- renvoyer des erreurs HTTP explicites plutôt que des 500 silencieuses ;
- découper une API en routers ;
- spécifier un contrat d'API à un agent, puis relire ce qu'il produit avec un œil critique.

## 1. Qu'est-ce qu'une API ?

Une **API** (= *Application Programming Interface*) est une interface qu'un logiciel expose pour que
d'autres logiciels puissent l'utiliser sans savoir comment il est fait à l'intérieur.

Une application deployée à grande échelle ne permet pas seule de faire fonctionner un système complexe. Il faut la plupart du temps plusieurs applications qui tournent simultanément et qui s'interrogent en permanence. Ces systèmes peuvent être écrits dans des langages différents et déployés sur des environnements différents.

Il faut donc un moyen à toutes ces applications de communiquer entre elles de manière efficace et standardisée.

### 1.1. Le contrat

Une API, c'est avant tout un **contrat** entre celui qui l'expose et ceux qui la consomment :

- quelles ressources sont disponibles, à quels endroits ;
- quelles opérations sont possibles sur chacune ;
- quelle forme ont les données envoyées et reçues ;
- que se passe-t-il quand ça se passe mal.

Tant que le contrat est respecté, l'implémentation interne peut changer complètement (changement
de base de données, refonte du code) sans casser les clients. C'est tout l'intérêt.

Le format d'échange standard aujourd'hui est le format **JSON** :

```json
{
  "id": 12,
  "titre": "Vélo de ville",
  "disponible": true,
  "tarif_jour": 8.5,
  "tags": ["velo", "mobilite"]
}
```

JSON est textuel, lisible, supporté partout, et se mappe naturellement sur les types Python
(`dict`, `list`, `str`, `int`, `float`, `bool`, `None`).

### 1.2. Pourquoi c'est devenu incontournable

- **Découplage** : le frontend et le backend évoluent séparément, avec des équipes différentes.
- **Réutilisation** : la même API sert un site web, une app mobile, un script d'import.
- **Intégration** : c'est le moyen standard de brancher deux systèmes entre eux.

Points de vigilance, en revanche : une API expose une surface d'attaque, impose de gérer la compatibilité dans le temps, ajoute de la latence réseau...

## 2. HTTP, le protocole de base

### 2.1. Anatomie d'une requête

Tout échange HTTP suit le même schéma : le client envoie une **requête**, le serveur renvoie une
**réponse**. Les deux ont la même structure : une ligne d'ouverture, des en-têtes, un corps
optionnel.

#### La requête

```http
POST http://api.google.com/items 
Content-Type: application/json
Authorization: Bearer eyJhbGciOi...

{"titre": "Perceuse", "tarif_jour": 5.0}
```

Quatre éléments à retenir :

| Élément | Dans l'exemple | Rôle |
|---|---|---|
| **Méthode** | `POST` | L'intention : lire, créer, modifier, supprimer (voir 2.2) |
| **URL** | `/items` | Quelle ressource on cible |
| **En-têtes** | `Content-Type`, `Authorization` | Les métadonnées de la requête |
| **Corps** | `{"titre": ...}` | Les données envoyées, en JSON la plupart du temps |

Les **en-têtes** portent tout ce qui décrit la requête sans faire partie des données : le format du
corps (`Content-Type: application/json`), les formats acceptés en réponse (`Accept`), le jeton
d'authentification (`Authorization: Bearer ...`, séance 4). Le **corps** n'existe que pour les
méthodes qui envoient des données (`POST`, `PUT`, `PATCH`) — un `GET` n'en a pas.

#### Les parties d'une URL

L'URL est la partie que vous concevez vous-mêmes quand vous écrivez une API : c'est elle qui
matérialise le contrat. Elle se décompose ainsi :

```text
https://api.gearshare.local:8000/items/42/reservations?statut=active&page=2#resume
└─┬─┘   └────────┬────────┘└─┬─┘└──────────┬─────────┘ └────────┬─────────┘└──┬──┘
scheme        domaine        port        path            query params   fragment
```

| Partie | Exemple | À quoi ça sert |
|---|---|---|
| **Scheme** | `https` | Le protocole utilisé (`http`, `https`) |
| **Domaine** | `api.gearshare.local` | La machine à contacter. Ici `api` est un sous-domaine de `gearshare.local` |
| **Port** | `8000` | Le port d'écoute du serveur. Implicite si standard : `80` en HTTP, `443` en HTTPS. En dev, vos conteneurs exposent souvent `8000` |
| **Path** | `/items/42/reservations` | Le chemin qui **identifie la ressource** ciblée |
| **Query params** | `?statut=active&page=2` | Les paramètres optionnels : filtres, tri, pagination |
| **Fragment** | `#resume` | Ancre interne à la page, traitée par le navigateur — **jamais envoyée au serveur**, donc inutilisable dans une API |

Deux points essentiels pour la suite :

- Le **path** identifie *quoi* : `/items/42` désigne le matériel 42, et rien d'autre. Les segments
  variables (ici `42`) sont les **path parameters** — vous les récupérerez en FastAPI avec
  `/items/{item_id}` (section 5.3).
- Les **query params** décrivent *comment* on veut la réponse : `?disponible=true&tag=velo&page=2`.
  Ils sont facultatifs par nature, et se déclarent en FastAPI comme des arguments de fonction avec
  une valeur par défaut (section 5.4).

La faute classique est de mettre dans le path ce qui relève du filtrage
(`/items/disponibles/velo`) : le path doit désigner une ressource, pas encoder une recherche.

#### La réponse

Le serveur répond avec la même structure — mais la ligne d'ouverture change : au lieu d'une méthode
et d'une URL, elle porte un **code de statut** qui résume le résultat de l'appel.

```http
HTTP/1.1 201 Created
Content-Type: application/json

{"id": 42, "titre": "Perceuse", "tarif_jour": 5.0}
```

Même structure, avec un **code de statut** (`201`) à la place de la méthode et de l'URL : des
en-têtes, puis un corps. Le code de statut est ce que le client regarde en premier pour savoir si
l'appel a réussi — d'où la section 2.3.

### 2.2. Les méthodes

| Méthode | Usage | Idempotente ? | Corps de requête |
|---|---|---|---|
| `GET` | Lire une ressource ou une collection | oui | non |
| `POST` | Créer une ressource | non | oui |
| `PUT` | Remplacer entièrement une ressource | oui | oui |
| `PATCH` | Modifier partiellement une ressource | non (en général) | oui |
| `DELETE` | Supprimer une ressource | oui | non |

**Idempotente** signifie : rejouer la même requête N fois donne le même état final qu'une seule
fois. `DELETE /items/42` deux fois de suite laisse la ressource supprimée dans les deux cas.
`POST /items` deux fois crée deux ressources. C'est ce qui permet à un client de réessayer sans
danger une requête `GET`, `PUT` ou `DELETE` qui a échoué sur un timeout.

Règle simple : **un `GET` ne modifie jamais rien**. Une route `GET /items/42/delete` est une faute.

### 2.3. Les codes de statut

Vous devez connaître ceux-ci par cœur — ils font partie de la grille d'évaluation :

| Code | Nom | Quand l'utiliser |
|---|---|---|
| `200` | OK | Lecture ou mise à jour réussie |
| `201` | Created | Création réussie (renvoyez la ressource créée) |
| `204` | No Content | Suppression réussie, rien à renvoyer |
| `400` | Bad Request | Requête mal formée, règle métier violée |
| `401` | Unauthorized | Pas authentifié (ou token invalide/expiré) |
| `403` | Forbidden | Authentifié, mais pas le droit de faire ça |
| `404` | Not Found | La ressource n'existe pas |
| `409` | Conflict | Conflit d'état (email déjà pris, créneau déjà réservé) |
| `422` | Unprocessable Entity | Validation des données échouée (FastAPI le renvoie tout seul) |
| `500` | Internal Server Error | Bug côté serveur — ne doit jamais être volontaire |

La distinction `401` / `403` tombe souvent : **401 = je ne sais pas qui vous êtes**, **403 = je sais
qui vous êtes et ce n'est pas à vous**.

## 3. REST

### 3.1. Le principe : des ressources, pas des actions

REST (*REpresentational State Transfer*) est un **style d'architecture**, pas une norme. L'idée
centrale : on modélise le domaine en **ressources** identifiées par des URL, et on agit dessus
avec les méthodes HTTP.

```text
GET    /items            → lister le matériel
POST   /items            → publier du matériel
GET    /items/42         → détail du matériel 42
PUT    /items/42         → remplacer le matériel 42
DELETE /items/42         → supprimer le matériel 42
GET    /items/42/reservations → les réservations du matériel 42
```

Conventions à respecter :

- **noms au pluriel**, pas de verbe dans l'URL (`/items`, pas `/getItems` ni `/createItem`) ;
- l'identifiant dans le chemin (`/items/42`), les filtres en query string
  (`/items?disponible=true&tag=velo`) ;
- des URL **stables** dans le temps ;
- **sans état** : chaque requête porte tout ce qu'il faut pour être traitée (d'où le token
  d'authentification renvoyé à chaque appel — séance 4).

Une contre-conception fréquente : `POST /reserverUnVelo`. La version REST : `POST /reservations`
avec l'identifiant du matériel dans le corps.

### 3.2. Les autres styles d'API

Pour votre culture, et parce que vous les croiserez :

- **GraphQL** : le client décrit précisément les champs qu'il veut, une seule URL. Évite le
  sur-chargement/sous-chargement de données, au prix d'une complexité serveur bien supérieure.
- **WebSocket** : connexion bidirectionnelle persistante, pour le temps réel (chat, notifications).
  HTTP est requête/réponse, WebSocket est un tuyau ouvert.
- **gRPC** : binaire, contractuel (Protobuf), très rapide — surtout utilisé entre services internes.

Pour ce module, c'est **REST**, et c'est le bon choix : c'est le standard du web, c'est simple, et
c'est ce que vous rencontrerez en entreprise dans l'immense majorité des cas.

## 4. Les frameworks Python

| Framework | Philosophie | Pour quoi |
|---|---|---|
| **Django** | « Batteries included » : ORM, admin, auth, templates fournis | Grosse application web classique, équipe qui veut des conventions fortes |
| **Flask** | Micro-framework minimaliste, tout est extension | Petits services, prototypage, contrôle total |
| **FastAPI** | Moderne, asynchrone, validation et doc automatiques via les annotations de types | API REST, la référence actuelle en Python |

**Nous utiliserons FastAPI**, et ce n'est pas négociable pour le projet. Les raisons :

- il s'appuie sur les **annotations de types** Python — la validation, la sérialisation et la
  documentation découlent du code que vous écrivez déjà ;
- il génère automatiquement une documentation OpenAPI interactive ;
- il est asynchrone (ASGI) et rapide ;
- son système d'**injection de dépendances** rend l'authentification et la gestion de session
  base de données propres (vous le verrez en séances 3 et 4).

Son inconvénient : il ne fournit ni ORM ni système d'authentification. Vous devez les assembler
vous-mêmes — ce que nous ferons.

## 5. Premiers pas avec FastAPI

### 5.1. Une application minimale

Une application FastAPI tient en trois éléments : on instancie un objet `FastAPI`, on lui attache
des routes avec des décorateurs (`@app.get(...)`), et chaque route est une simple fonction Python
qui renvoie la réponse. Voici la plus petite API complète possible :

```python
# app/main.py
from fastapi import FastAPI

app = FastAPI(title="GearShare API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}
```

On lance avec **uvicorn**, le serveur ASGI :

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

`app.main:app` = « dans le module `app.main`, prends l'objet nommé `app` ». `--reload` recharge à
chaque sauvegarde de fichier (développement uniquement). `--host 0.0.0.0` est **indispensable dans
un conteneur** : avec le défaut `127.0.0.1`, le serveur n'écoute que depuis l'intérieur du
conteneur et vous n'y accéderez pas depuis votre machine.

Le retour de la fonction (un `dict`) est automatiquement sérialisé en JSON, avec le bon
`Content-Type`.

### 5.2. ASGI : comment votre code est servi

Vous venez de lancer une commande sans savoir ce qu'elle fait. Prenons deux minutes, parce que ce
modèle explique ensuite beaucoup de choses : pourquoi `async def`, pourquoi un pool de connexions
par process, pourquoi une variable globale n'est pas un cache.

#### Deux rôles séparés : le serveur et l'application

Servir une API demande deux métiers très différents :

- **le serveur** ouvre un socket sur un port, accepte les connexions TCP, parse le texte HTTP
  (méthode, URL, en-têtes, corps — cf. 2.1), gère les timeouts et le HTTPS ;
- **l'application** — votre code — décide *quoi répondre* à `POST /items`.

Python a standardisé le contrat entre les deux. C'est **ASGI** (*Asynchronous Server Gateway
Interface*) : une spécification, pas une bibliothèque. Elle dit qu'une application est un appelable
asynchrone à trois arguments :

```python
async def app(scope, receive, send):
    ...
```

C'est tout. Une API ASGI complète, sans aucun framework :

```python
async def app(scope, receive, send):
    assert scope["type"] == "http"          # ce que le client demande
    await receive()                          # lire la requête entrante
    await send({                             # émettre le début de la réponse
        "type": "http.response.start",
        "status": 200,
        "headers": [(b"content-type", b"application/json")],
    })
    await send({                             # puis le corps
        "type": "http.response.body",
        "body": b'{"status": "ok"}',
    })
```

Les trois arguments :

| Argument | Nature | Contenu |
|---|---|---|
| `scope` | `dict` | Le contexte de la connexion : `type` (`http`, `websocket`, `lifespan`), `method`, `path`, `query_string`, `headers`, IP du client |
| `receive` | coroutine | À appeler pour recevoir les événements entrants (le corps de la requête, arrivant éventuellement par morceaux) |
| `send` | coroutine | À appeler pour émettre les événements sortants (statut + en-têtes, puis corps) |

Retenez ceci : **`FastAPI()` est exactement cet appelable-là**, en beaucoup plus riche. Quand vous
écrivez `app = FastAPI(...)`, vous construisez un objet ASGI qui, à partir du `scope`, retrouve la
route qui correspond au `path` et à la `method`, valide les paramètres, appelle votre fonction, puis
sérialise son retour en événements `send`. Tout le cours qui suit décrit ce que FastAPI fait *entre*
`scope` et `send`.

#### Le serveur, lui, est interchangeable

Puisque le contrat est standard, **le serveur ASGI est un composant remplaçable** :

| Serveur ASGI | Particularité |
|---|---|
| **uvicorn** | Le plus répandu, celui que nous utilisons. S'appuie sur `uvloop` et `httptools` |
| **hypercorn** | Supporte HTTP/2 et HTTP/3 |
| **granian** | Écrit en Rust, orienté performance |
| **daphne** | Historiquement lié à Django Channels |

Votre code ne les mentionne jamais : `uvicorn app.main:app` et `hypercorn app.main:app` servent la
même application sans changer une ligne. uvicorn n'est donc **pas** « le serveur de FastAPI », c'est
une implémentation du standard parmi d'autres — exactement comme PostgreSQL est une implémentation
de SQL.

L'ancêtre d'ASGI est **WSGI** (Flask, Django historique) : un appelable *synchrone*, une requête
occupant un thread du début à la fin, et aucune notion de connexion longue. ASGI existe pour lever
ces deux limites — d'où le support des WebSocket par la même interface (`scope["type"] ==
"websocket"`).

#### Le modèle d'exécution : une boucle, puis N process

Reste à comprendre *comment* uvicorn exécute votre application. Le schéma ci-dessous montre les
deux mécanismes en jeu : à l'intérieur d'un process, une **boucle d'événements** entrelace les
requêtes ; et le serveur peut démarrer **plusieurs process workers** qui se partagent le même port.

```text
                 ┌──────────── process worker 1 ────────────┐
                 │  event loop                              │
  socket :8000 ──┤    ├─ requête A ─┐                       │
  (partagé)      │    ├─ requête B ─┼─► votre app ASGI      │
                 │    └─ requête C ─┘   (FastAPI)           │
                 └──────────────────────────────────────────┘
                 ┌──────────── process worker 2 ────────────┐
                 │  event loop  (mémoire séparée)           │
                 └──────────────────────────────────────────┘
```

Deux niveaux à ne pas confondre :

1. **Dans un process** : une seule **boucle d'événements** (`asyncio`) traite plusieurs requêtes en
   les *entrelaçant*. Dès qu'une requête attend (réseau, base de données), la boucle passe à une
   autre. Ce n'est pas du parallélisme : un seul cœur, un seul thread d'exécution Python.
2. **Entre process** : `--workers 4` démarre 4 process qui **partagent le même socket d'écoute**, et
   le noyau répartit les connexions entrantes entre eux. Là, il y a du vrai parallélisme.

Les conséquences sont concrètes et vous mordront si vous les ignorez :

- **Les workers ne partagent pas leur mémoire.** Un compteur ou un cache dans une variable globale
  devient incohérent dès le deuxième worker. Tout état partagé doit vivre dans PostgreSQL (ou un
  Redis).
- **Chaque worker ouvre son propre pool de connexions** à la base. 4 workers × 10 connexions = 40
  connexions PostgreSQL — à garder en tête en séance 3.
- **Une opération bloquante gèle toute la boucle** du worker. Un `time.sleep(5)` ou un appel réseau
  synchrone dans une route `async def` met en attente *toutes* les requêtes de ce worker. C'est
  pour cette raison que FastAPI exécute les routes déclarées en `def` (synchrones) dans un pool de
  threads séparé, et seules les `async def` directement sur la boucle. En cas de doute, `def` est
  le choix sûr.

#### En développement et en production

- **Dev** : un seul process, `--reload` pour recharger à chaque sauvegarde. `--reload` est
  incompatible avec `--workers`.
- **Prod** : plusieurs workers (ordre de grandeur : `2 × nombre de cœurs`, à mesurer), jamais de
  `--reload`, et un reverse proxy devant. Dans votre projet, la montée en charge se fera plutôt en
  multipliant les **conteneurs** backend derrière ce proxy — un worker par conteneur, l'orchestrateur
  fait la répartition.

### 5.3. Path parameters

Vous avez vu en 2.1 que le path identifie la ressource ciblée, avec des segments variables comme
`/items/42`. Côté FastAPI, on déclare ce segment entre accolades dans le chemin, et on le récupère
comme paramètre de la fonction — l'annotation de type pilotant la conversion :

```python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}
```

L'annotation `: int` n'est pas décorative. FastAPI **convertit et valide** :

- `GET /items/42` → `item_id` vaut l'entier `42` ;
- `GET /items/abc` → réponse `422` automatique, avec un message expliquant l'erreur.

Vous n'écrivez aucun code de validation. C'est le point central de FastAPI : le type *est* la
spécification.

Attention à l'ordre de déclaration des routes : elles sont évaluées de haut en bas.

```python
@app.get("/items/search")   # doit être déclarée AVANT /items/{item_id}
def search_items(...): ...

@app.get("/items/{item_id}")
def get_item(item_id: int): ...
```

Dans l'ordre inverse, `/items/search` serait capturée par `/items/{item_id}` et échouerait en 422.

### 5.4. Query parameters

Tout paramètre de fonction qui n'apparaît pas dans le chemin devient un query parameter :

```python
from fastapi import Query


@app.get("/items")
def list_items(
    skip: int = 0,
    limit: int = Query(default=20, le=100, description="Nombre max de résultats"),
    disponible: bool | None = None,
):
    return {"skip": skip, "limit": limit, "disponible": disponible}
```

- `skip: int = 0` → optionnel, défaut `0` ;
- `Query(..., le=100)` → contrainte : `limit` ne peut pas dépasser 100, sinon `422` ;
- `bool | None = None` → optionnel, absent par défaut.

`GET /items?limit=50&disponible=true` fonctionne ; `GET /items?limit=5000` renvoie `422`.

Toujours **plafonner les paramètres de pagination** : sans `le=100`, un client peut demander un
million de lignes et faire tomber votre service.

## 6. Pydantic : la validation au cœur de FastAPI

Pydantic est la bibliothèque de validation sur laquelle repose FastAPI. Un modèle Pydantic est une
classe qui décrit la forme d'une donnée.

### 6.1. Un modèle d'entrée

Un modèle d'entrée décrit le **corps de requête** attendu : on hérite de `BaseModel`, on déclare un
champ typé par attribut, et `Field(...)` porte les contraintes de validation (longueur, bornes…) :

```python
from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    titre: str = Field(min_length=3, max_length=120)
    description: str | None = None
    tarif_jour: float = Field(gt=0, description="Tarif journalier en euros, strictement positif")


@app.post("/items", status_code=201)
def create_item(payload: ItemCreate):
    return {"id": 1, **payload.model_dump()}
```

FastAPI comprend que `payload` est un modèle Pydantic, donc que la donnée vient du **corps** de la
requête. Il désérialise le JSON, valide chaque champ, et vous livre un objet typé. Si le titre fait
deux caractères ou si `tarif_jour` vaut `-3`, le client reçoit un `422` détaillé — votre fonction
n'est jamais appelée.

```json
{
  "detail": [
    {
      "type": "greater_than",
      "loc": ["body", "tarif_jour"],
      "msg": "Input should be greater than 0"
    }
  ]
}
```

**Conséquence pratique** : dans le corps de vos fonctions de route, vous n'avez plus besoin
d'écrire `if not titre: raise ...`. Les contraintes vivent dans le modèle.

### 6.2. Un modèle de sortie

Le modèle d'entrée et le modèle de sortie ne sont **pas les mêmes**. C'est une erreur très
fréquente, y compris chez les agents.

```python
class ItemRead(BaseModel):
    id: int
    titre: str
    description: str | None
    tarif_jour: float


@app.post("/items", response_model=ItemRead, status_code=201)
def create_item(payload: ItemCreate):
    ...
```

`response_model` **filtre** la réponse : tout champ absent de `ItemRead` est retiré, même s'il est
présent dans l'objet renvoyé. C'est votre garde-fou principal contre les fuites de données : si
vous renvoyez un objet utilisateur contenant `hashed_password`, un `response_model` sans ce champ
l'élimine.

Retenez le triptyque, vous le réutiliserez pour chaque ressource du projet :

| Modèle | Rôle | Contient |
|---|---|---|
| `XxxCreate` | Ce que le client envoie pour créer | Champs modifiables, pas d'`id` |
| `XxxUpdate` | Ce que le client envoie pour modifier | Mêmes champs, tous optionnels |
| `XxxRead` | Ce que l'API renvoie | `id` + champs publics, **jamais** de secret |

## 7. Gérer les erreurs

Les erreurs d'API ne sont pas un défaut de conception : elles sont au cœur du contrat entre le client et le serveur. Quand une ressource n'existe pas, qu'une donnée est invalide ou qu'un conflit apparaît, l'API doit répondre de façon explicite avec un code HTTP clair, plutôt que de laisser le client deviner ce qui s'est passé. C'est important parce que les clients (front, scripts et autres services) doivent pouvoir décider quoi faire : réessayer, afficher un message utilisateur, ou corriger une requête. Une API bien conçue rend donc le système prévisible, robuste et plus facile à intégrer dans un projet réel.

```python
from fastapi import HTTPException

FAKE_DB: dict[int, dict] = {}


@app.get("/items/{item_id}", response_model=ItemRead)
def get_item(item_id: int):
    item = FAKE_DB.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} introuvable")
    return item
```

`raise HTTPException(...)` interrompt le traitement et produit une réponse JSON
`{"detail": "..."}` avec le bon code.

Trois règles que je vérifierai dans vos projets :

1. **Aucun `500` volontaire.** Un cas prévu (ressource absente, conflit) a son code dédié. Un `500`
   signale un bug.
2. **Pas de fuite d'information dans le message.** `detail="Item 42 introuvable"` est bien ;
   `detail=str(exception_sql)` expose votre schéma de base à l'extérieur.
3. **Cohérence.** La même situation renvoie toujours le même code dans toute l'API.

Pour centraliser, FastAPI permet d'enregistrer des gestionnaires d'exception :

```python
from fastapi import Request
from fastapi.responses import JSONResponse


class ReservationConflict(Exception):
    def __init__(self, message: str):
        self.message = message


@app.exception_handler(ReservationConflict)
def handle_reservation_conflict(request: Request, exc: ReservationConflict):
    return JSONResponse(status_code=409, content={"detail": exc.message})
```

Vos couches métier lèvent alors des exceptions **métier** (`ReservationConflict`) sans rien savoir
de HTTP, et la traduction en code HTTP se fait à un seul endroit. C'est le pattern que vous mettrez
en place en séance 3.

## 8. Documentation automatique : OpenAPI

FastAPI génère, à partir de vos annotations, un document **OpenAPI** décrivant tout le contrat de
votre API. Trois URL disponibles dès le démarrage :

- `http://localhost:8000/docs` — interface Swagger UI, où vous pouvez **exécuter** les requêtes ;
- `http://localhost:8000/redoc` — documentation en lecture ;
- `http://localhost:8000/openapi.json` — le contrat brut, exploitable par des outils.

Utilisez `/docs` en permanence pendant les TP : c'est votre client HTTP le plus rapide.

Vous améliorez cette documentation gratuitement en soignant votre code :

```python
@app.post(
    "/items",
    response_model=ItemRead,
    status_code=201,
    tags=["items"],
    summary="Publier du matériel",
    responses={409: {"description": "Un matériel du même nom existe déjà"}},
)
def create_item(payload: ItemCreate):
    """Publie un nouveau matériel dans le catalogue.

    Le propriétaire est déduit de l'utilisateur authentifié.
    """
```

La docstring devient la description longue dans Swagger.

## 9. Structurer : les routers

Un fichier `main.py` de 800 lignes est ingérable — pour vous comme pour un agent, dont la qualité
chute quand le contexte est un gros fichier fourre-tout. FastAPI fournit `APIRouter` pour découper
par ressource.

```python
# app/routers/items.py
from fastapi import APIRouter, HTTPException

from app.schemas.item import ItemCreate, ItemRead

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemRead])
def list_items(skip: int = 0, limit: int = 20):
    ...


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int):
    ...
```

On branche ensuite ce router dans l'application principale pour exposer les endpoints correspondants
sous le bon préfixe :

```python
# app/main.py
from fastapi import FastAPI

from app.routers import items, users

app = FastAPI(title="GearShare API")
app.include_router(items.router)
app.include_router(users.router)
```

L'arborescence cible, que vous garderez tout le module :

```text
backend/
├── app/
│   ├── main.py            # création de l'app, include_router, middlewares
│   ├── routers/           # une route = HTTP entrant/sortant, rien d'autre
│   ├── schemas/           # modèles Pydantic (contrat public)
│   ├── services/          # logique métier (séance 4)
│   ├── repositories/      # accès données (séance 4)
│   └── models/            # modèles SQLAlchemy (séance 4)
├── requirements.txt
└── Dockerfile
```

Aujourd'hui vous ne remplissez que `routers/` et `schemas/`, mais **créez déjà les dossiers** : la
structure guide l'agent autant que vous.

## 10. Faire produire une API par un agent

Un agent produit d'autant mieux qu'il reçoit une spécification précise — c'est le principe que
vous formaliserez en séance 6. Pour une API, cette spécification a une forme naturelle :
**le contrat**.

Comparez :

> « Fais-moi une API pour gérer du matériel. »

et :

> « Ajoute un router `items` monté sur `/items`, avec :
> - `GET /items?skip&limit&disponible` → `list[ItemRead]`, `limit` plafonné à 100 ;
> - `GET /items/{item_id}` → `ItemRead`, `404` si absent ;
> - `POST /items` → `201` + `ItemRead`, corps `ItemCreate` (titre 3–120 caractères,
>   `tarif_jour > 0`) ;
> - `DELETE /items/{item_id}` → `204`, `404` si absent.
>
> Stockage en dictionnaire en mémoire pour l'instant. Schémas Pydantic dans
> `app/schemas/item.py`, router dans `app/routers/items.py`. Pas de logique métier dans le router. »

La seconde tient en dix lignes et produit un résultat exploitable du premier coup. C'est le
travail que vous ferez au TP.

Ce que vous devez **systématiquement vérifier** dans une API générée — j'en ferai une checklist en
séance 7, mais commencez dès maintenant :

| Point | Question à vous poser |
|---|---|
| Codes de statut | `201` sur création ? `204` sur suppression ? Pas de `200` partout ? |
| `response_model` | Présent sur chaque route ? Ne fuite-t-il aucun champ interne ? |
| Modèles d'entrée/sortie | Distincts, ou l'agent a-t-il réutilisé le même partout ? |
| Validation | Les contraintes métier sont-elles dans le modèle Pydantic, ou en `if` dispersés ? |
| Erreurs | `404` levé quand la ressource manque, ou `None` renvoyé silencieusement ? |
| Ordre des routes | Les routes littérales avant les routes paramétrées ? |
| Async | `async def` sans le moindre `await` à l'intérieur : inutile, souvent copié d'un exemple |
| Dépendances | Des paquets inventés ou obsolètes dans `requirements.txt` ? |

Ce dernier point mérite une insistance : un agent peut suggérer une bibliothèque qui n'existe pas,
ou une version qui n'existe plus. **Vérifiez toujours ce qui entre dans votre `requirements.txt`.**

## 11. Synthèse

- Une API est un **contrat** ; en REST, ce contrat s'exprime en ressources + méthodes HTTP + codes
  de statut.
- Choisissez la méthode selon la sémantique (`GET` ne modifie rien) et le code selon le résultat
  (`201`, `204`, `404`, `409`, `422`…).
- Dans FastAPI, **les annotations de types font le travail** : validation, sérialisation,
  documentation.
- Séparez toujours modèle d'entrée (`Create`/`Update`) et modèle de sortie (`Read`), et posez un
  `response_model` sur chaque route.
- Levez des `HTTPException` explicites ; aucune erreur ne doit remonter en `500`.
- Découpez en routers dès le début, avec l'arborescence cible du projet.
- Face à un agent, spécifiez le **contrat** avant de demander du code, et relisez avec la checklist.

Passez au [TP](../tp/README.md) : vous construisez votre première API, dans un conteneur.
