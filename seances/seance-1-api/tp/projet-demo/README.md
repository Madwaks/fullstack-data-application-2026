# Projet démo — TP séance 1

Ce dossier est le point de départ du [TP de la séance 1](../README.md). Il contient une API
FastAPI exécutable, avec une seule route `GET /health`, ainsi que les dossiers qui accueilleront
les routes et schémas du TP.

Vous allez y construire une API en mémoire pour la ressource `items`, puis faire produire et
reviewer la ressource `reservations` par GitHub Copilot. Ce n'est ni le projet GearShare complet,
ni son architecture finale : PostgreSQL, les couches applicatives, l'authentification et le
frontend seront introduits dans les séances suivantes.

## Démarrer

Depuis ce dossier :

```bash
docker compose up --build
```

L'API répond sur [http://localhost:8000/health](http://localhost:8000/health) et sa documentation
interactive est disponible sur [http://localhost:8000/docs](http://localhost:8000/docs).

Le montage de volume et `--reload` sont réservés au développement : le code est rechargé à chaque
sauvegarde sans reconstruction de l'image.
