# Projet démo — TP séance 2

Ce dossier est le point de départ du [TP de la séance 2](../README.md). Il contient l'API en
mémoire **telle que je l'attendais à la fin du TP de la séance 1** : le CRUD complet sur `items`,
la ressource `reservations` telle que spécifiée en séance 1, le découpage en routers et la
validation croisée des dates dans le schéma Pydantic.

Vous travaillez normalement sur **votre** API de la séance 1. Ce projet sert de secours si votre
rendu n'est pas terminé ou n'est pas conforme, et de référence pour comparer : si un test du TP 2
échoue chez vous et passe ici, la différence est dans votre code, pas dans le test.

Il n'y a **aucun test dans ce dossier** : c'est vous qui les écrivez, à partir de l'étape 0 du
TP. Vous y trouverez aussi, volontairement, les deux compteurs globaux `_next_id` que l'étape 1.2
vous demande de supprimer.

## Arborescence

```text
projet-demo/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── reservations.py
│   └── schemas/
│       ├── __init__.py
│       ├── item.py
│       └── reservation.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Démarrer

Depuis ce dossier :

```bash
docker compose up --build
```

L'API répond sur [http://localhost:8000/health](http://localhost:8000/health) et sa documentation
interactive est disponible sur [http://localhost:8000/docs](http://localhost:8000/docs), avec les
deux ressources `items` et `reservations`.

Le montage de volume et `--reload` sont réservés au développement : le code est rechargé à chaque
sauvegarde sans reconstruction de l'image. L'étape 0 du TP vous fera ajouter `tests/` et
`pytest.ini` au `Dockerfile` et au `docker-compose.yml`.
