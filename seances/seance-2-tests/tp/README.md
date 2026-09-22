# TP — Séance 2 : tester l'API de la séance 1 (2h)

## Ce que vous allez faire

Ce TP consiste à écrire les tests de l'API que vous avez developpé en séance 1 : le CRUD `items` et
la ressource `reservations`.

## Objectifs du TP

À la fin de ce TP, vous devez savoir :

- installer et lancer pytest dans le projet de la séance 1, dans son conteneur ;
- tester une API FastAPI avec `TestClient`, sans démarrer de serveur ;
- écrire des fixtures : un client partagé, un stockage remis à zéro, un item déjà créé ;
- automatiser, en tests de contrat, toutes les vérifications faites à la main en séance 1 ;

