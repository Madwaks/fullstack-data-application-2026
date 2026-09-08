# Fullstack data application — API, données et pilotage d'agent

Bienvenue dans ce module de dernière année (E5) — cours et TD.

Vous allez construire une application fullstack (backend **FastAPI**, frontend Python séparé,
**PostgreSQL**, **Docker**) et apprendre à la construire **avec un agent de code** — **GitHub
Copilot** — sans jamais perdre la maîtrise de ce qu'il produit.

👉 **Commencez par [PRESENTATION.md](PRESENTATION.md)** : la présentation complète du module, ce
qu'on y fait, comment on est évalué, et comment travailler.

## Ce que vous allez apprendre

**Côté technique**

- concevoir une API REST avec FastAPI : routes, validation Pydantic, codes HTTP, documentation auto ;
- modéliser un schéma relationnel PostgreSQL correct et écrire le SQL correspondant ;
- structurer une application en couches avec SQLAlchemy et des migrations versionnées ;
- implémenter une authentification JWT et des autorisations ;
- écrire des tests pytest couvrant les cas nominaux **et** les cas d'erreur ;
- conteneuriser l'application avec Docker Compose et vérifier lint, tests et build avant chaque
  PR.

**Côté agentic**

- spécifier une feature de façon qu'un agent puisse réellement l'exécuter ;
- configurer un projet pour un agent (`.github/copilot-instructions.md`, conventions) ;
- valider un plan avant d'implémenter ;
- **reviewer du code généré** : schéma faux, migration destructrice, autorisation oubliée, test
  qui ne teste rien ;
- travailler en équipe : branches, pull requests, code review.

## Avant la séance 1 : mise à niveau Docker (optionnelle)

Si vous n'avez jamais utilisé Docker, faites en autonomie la
[séance 0 — Docker : histoire et fondamentaux](seances/seance-0-docker) : histoire du déploiement
logiciel, terminologie, Dockerfile, et un TP jusqu'à Docker Compose.

## Organisation

| # | Séance | Cours | TP |
|---|--------|-------|----|
| 0 | [Docker : histoire et fondamentaux](seances/seance-0-docker) *(optionnelle, en autonomie)* | [cours](seances/seance-0-docker/cours) | [tp](seances/seance-0-docker/tp) |
| 1 | [Les API et FastAPI](seances/seance-1-api) | [cours](seances/seance-1-api/cours) | [tp](seances/seance-1-api/tp) |
| 2 | [Tester une API](seances/seance-2-tests) | [cours](seances/seance-2-tests/cours) | [tp](seances/seance-2-tests/tp) |
| 3 | [PostgreSQL et le modèle relationnel](seances/seance-3-database) | [cours](seances/seance-3-database/cours) | [tp](seances/seance-3-database/tp) |
| 4 | [L'application web en couches](seances/seance-4-webapp) | [cours](seances/seance-4-webapp/cours) | [tp](seances/seance-4-webapp/tp) |
| 5 | [Authentification et autorisation](seances/seance-5-authentification) | [cours](seances/seance-5-authentification/cours) | [tp](seances/seance-5-authentification/tp) |
| 6 | [Fondations agentic](seances/seance-6-fondations-agentic) | [cours](seances/seance-6-fondations-agentic/cours) | [tp](seances/seance-6-fondations-agentic/tp) |
| 7 | [Le flow complet d'une feature](seances/seance-7-dev-agentic) | [cours](seances/seance-7-dev-agentic/cours) | [tp](seances/seance-7-dev-agentic/tp) |

Chaque séance se partage entre cours et TP — la séance 6 est plus dense.

Le TP n'est pas un exercice d'application : c'est là que vous construisez votre projet. À la fin
de la séance 7, l'essentiel de votre application existe.

## Le projet

- [Sujet du projet](projet/sujet.md) — GearShare, identique pour tous les groupes
- [Grille d'évaluation](projet/grille-evaluation.md)

## Templates réutilisables

À copier et adapter dans votre propre dépôt de projet :

- [Exemple d'instructions projet pour l'agent](templates/claude-md-example.md)
- [Checklist code review](templates/checklist-code-review.md)
- [Template de PRD](templates/prd-template.md)

## Ce que vous devez avoir avant la séance 1

- Un compte GitHub avec **GitHub Education** activé (Copilot gratuit).
- Git, Docker Desktop, et VS Code (ou PyCharm) installés.
- Les bases : Python, HTTP/REST, SQL, Git.

Suivez [OUTILS.md](OUTILS.md) pour la procédure d'installation détaillée, à faire **avant** le
premier cours.
