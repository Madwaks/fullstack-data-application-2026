# Fullstack data application — présentation du module

---

## 1. En une phrase

Vous allez construire une application web complète — API FastAPI, base PostgreSQL, frontend
séparé, le tout conteneurisé — et vous allez la construire **avec un agent de code**, sans jamais
perdre la maîtrise de ce qu'il produit.

---

## 2. Pourquoi ce module, et pourquoi maintenant

Vous arrivez sur le marché du travail à un moment où les agents de code transforment déjà la
manière de développer. Ils accélèrent fortement les tâches répétitives, proposent des
implémentations complètes et permettent d'explorer rapidement une base de code. Mais ils ne
remplacent ni la compréhension du besoin, ni les choix d'architecture, ni la vérification du
résultat.

Face à ces outils, deux réactions sont tentantes, et toutes deux montrent vite leurs limites :

- **« Je n'ai plus besoin d'apprendre »** : on finit par produire du code qu'on ne sait ni
  expliquer, ni corriger, ni défendre. Le jour où l'application tombe en production à 23 h, on se
  retrouve seul devant une stack trace.
- **« Je n'utilise pas ces outils »** : on se prive d'un levier devenu courant, sans pour autant
  mieux résoudre les problèmes difficiles.

Ce module propose une voie entre les deux, celle qui est aussi recherchée en entreprise :

> **Utiliser pleinement l'agent, en comprenant ce qu'il vous a donné.**

Concrètement, il s'agit d'apprendre deux choses en parallèle :

| Ce que vous apprendrez à faire                                       | Pourquoi                               |
| -------------------------------------------------------------------- | -------------------------------------- |
| **Construire** une API, une base, une auth, des tests.         | Pour savoir ce qu'est un bon résultat |
| **Piloter** un agent : spécifier, planifier, reviewer, tester | Pour aller vite sans produire de dette |

La première moitié est le contenu technique classique, la seconde est ce qui change avec les
agents. Le module travaille les deux, et l'évaluation en tient compte.

---

## 3. Ce que vous saurez faire à la fin

À l'issue du module, vous saurez :

**Côté technique**

- concevoir et écrire une API REST avec FastAPI : routes, validation Pydantic, codes HTTP,
  documentation automatique ;
- modéliser un schéma relationnel PostgreSQL correct (clés, contraintes, index) et écrire le SQL
  qui va avec ;
- structurer une application en couches (routers / services / repositories / models) avec
  SQLAlchemy et des migrations Alembic versionnées ;
- implémenter une authentification JWT correcte et une autorisation par propriété de ressource ;
- écrire une suite de tests pytest qui couvre les cas nominaux **et** les cas d'erreur ;
- conteneuriser le tout avec Docker Compose et vérifier lint, tests et build avant chaque PR.

**Côté agentic**

- rédiger une spécification qu'un agent peut réellement exécuter ;
- configurer un projet pour un agent (instructions projet, conventions, définition de « terminé ») ;
- valider un plan d'implémentation avant d'écrire la moindre ligne ;
- **relire du code généré** : reconnaître un schéma faux, une migration destructrice, une
  autorisation oubliée, un test qui ne teste rien ;

---

## 4. Ce que vous allez construire

Le fil rouge de tout le module est un projet unique, identique pour tous les groupes :

### GearShare — plateforme de prêt de matériel entre étudiants

Publier du matériel qu'on prête, chercher et réserver du matériel disponible sur un créneau, gérer
son compte, consulter son historique de prêts, laisser un avis après un emprunt.

Le sujet est **volontairement simple** sur le plan fonctionnel, pour que l'attention se porte sur
la qualité de ce que vous construisez et sur la façon dont vous le construisez, plutôt que sur le
nombre de fonctionnalités.

### L'architecture cible

```text
┌─────────────┐   HTTP/JSON   ┌─────────────┐   SQL   ┌──────────────┐
│  frontend   │ ────────────► │   backend   │ ──────► │  PostgreSQL  │
│  (Python)   │ ◄──────────── │  (FastAPI)  │ ◄────── │              │
└─────────────┘               └─────────────┘         └──────────────┘
      conteneur                   conteneur               conteneur
                    docker compose up  →  tout démarre
```

Trois services, trois conteneurs, un seul `docker compose up`.

### Une stack commune

| Couche           | Technologie                                                                             |
| ---------------- | --------------------------------------------------------------------------------------- |
| Backend          | Python 3.12+,**FastAPI**, SQLAlchemy 2.0, Alembic                                 |
| Base de données | **PostgreSQL 17**                                                                 |
| Frontend         | Python,**application séparée** du backend, communique uniquement via l'API REST |
| Conteneurisation | **Docker + Docker Compose**, au minimum 3 services                                |
| Authentification | Utilisateurs +**JWT**, mots de passe hachés                                      |
| Tests            | **pytest**, cas nominaux et cas d'erreur                                          |
| Agent            | **GitHub Copilot** par défaut (gratuit avec GitHub Education) ; Claude Code ou Codex acceptés |

Tous les groupes partagent cette stack, et le projet doit la respecter pour être évalué. C'est ce
qui me permet de vous aider efficacement quand vous êtes bloqués, d'évaluer les projets sur une
base équitable et de vous faire travailler sur des technologies que vous retrouverez en entreprise.

---

## 5. Le déroulé

| # | Séance                                                                     | Ce que vous en repartez avec                                                |
| - | --------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| 0 | **Docker : histoire et fondamentaux** *(optionnelle, en autonomie)* | Images, conteneurs, Dockerfile, Compose                                     |
| 1 | **Les API et FastAPI**                                                | Une API REST avec validation, codes HTTP, documentation auto                |
| 2 | **Tester une API**                                                    | pytest, contrats HTTP, cas nominaux et cas d'erreur, couverture             |
| 3 | **PostgreSQL et le modèle relationnel**                              | Un schéma correct, du SQL, des index, une base dans Compose                |
| 4 | **L'application web en couches**                                      | SQLAlchemy, architecture en couches, Compose à 3 services                  |
| 5 | **Authentification et autorisation**                                  | JWT, hachage de mots de passe, routes protégées, ownership                |
| 6 | **Développer une feature avec un agent**                              | Instructions projet, skills, agents spécialisés ; fiche feature → plan → implémentation → PR → revue → merge |

Chaque séance est construite pareil : **Cours + TP**.

### Compétences par séance

Voici les compétences techniques et agentic que vous travaillez au fil du module. Les objectifs
détaillés et les critères de réussite sont précisés dans le support de cours de chaque séance.

| Séance | Compétences travaillées |
| ------ | ----------------------- |
| **0 — Docker** | Comprendre l'émergence du DevOps ; gérer images, conteneurs, volumes et persistance ; configurer une application multi-services ; analyser les logs et indicateurs de base avec `docker logs` et `docker stats`. |
| **1 — API et FastAPI** | Expliquer le rôle d'une API dans une architecture moderne ; lire et construire une requête HTTP ; créer une API Python/FastAPI dans un environnement de développement reproductible. |
| **2 — Tests** | Expliquer le rôle des tests ; écrire des tests simples pour une API, y compris les cas d'erreur ; comprendre et interpréter la couverture de code. |
| **3 — Base de données** | Différencier bases SQL et NoSQL ; maîtriser les notions fondamentales de PostgreSQL ; définir une structure de données relationnelle ; manipuler et interroger les données avec des commandes SQL simples. |
| **4 — Application web** | Expliquer l'architecture d'une application web moderne ; identifier les rôles respectifs de l'API et de la base de données ; connecter les services ; développer une API qui agit sur une base de données ; produire une première application structurée. |
| **5 — Authentification** | Identifier les mécanismes classiques d'authentification ; expliquer le rôle et la structure d'un jeton d'authentification ; appliquer les bonnes pratiques de sécurité ; sécuriser une API. |
| **6 — Développer une feature avec un agent** | Donner du contexte et des consignes utiles à un agent (instructions projet, skills, agents spécialisés, mode Plan) ; conduire une fonctionnalité de la fiche feature au merge ; rédiger des critères d'acceptation et un plan ; travailler avec branches, pull requests et revue de code ; contrôler les changements générés par un agent. |

---

## 6. La place de l'agent dans ce module

**L'agent est bienvenu partout, et même encouragé.** Je ne vous demanderai pas d'écrire du code à
la main pour prouver que vous savez le faire.

Trois principes accompagnent cette liberté :

### 1. Comprendre ce que vous rendez

L'objectif est que vous puissiez expliquer chaque partie de votre code, y compris ce que l'agent a
produit. Vos documents de review sont l'occasion de montrer cette compréhension.

### 2. Garder une trace de votre démarche

Les documents de **review** racontent ce que vous avez demandé, ce que l'agent a produit, ce que
vous avez corrigé et pourquoi. Ils rendent visibles votre raisonnement et vos décisions, et ils
comptent dans l'évaluation.

### 3. Assumer le résultat, quel qu'en soit l'auteur

Un `docker compose up` qui échoue, une migration qui perd des données ou un secret commité restent
vos problèmes, que la ligne fautive vienne de vous ou de l'agent. Le plus simple est de les
anticiper.

---

## 7. L'organisation pratique

### Les groupes

Pour le projet d'évaluation, vous travaillerez en **groupes de 2**.
Chaque groupe crée **son propre dépôt GitHub** pour le projet.

### Le rythme des rendus

Chaque séance a ses **livrables**, listés en fin de TP. Ils ne sont pas notés individuellement,
mais ils construisent le rendu final.
Le rendu final, c'est votre dépôt GitHub. Rien d'autre à envoyer.

### Ce dont vous avez besoin avant la séance 1

Tout est détaillé dans [OUTILS.md](OUTILS.md). En résumé :

- [ ] un compte **GitHub** + **GitHub Education** activé (Copilot gratuit) ;
- [ ] **Git** installé et configuré ;
- [ ] **GitHub Copilot** actif dans votre IDE ;
- [ ] **Docker Desktop** installé (`docker run hello-world` fonctionne) ;
- [ ] **VS Code** ou PyCharm ;

Les prérequis de connaissances sont Python, les bases de HTTP/REST, les bases de SQL et les bases
de Git. Les séances reviendront sur ces notions, avec un rythme adapté à un niveau E5.

---

## 8. L'évaluation

### Le projet évalué : GearShare

Le point de départ est **GearShare**, la plateforme de prêt de matériel entre étudiants décrite en
[section 4](#4-ce-que-vous-allez-construire), que vous construisez TP après TP : API FastAPI,
tests, base PostgreSQL, application en couches, frontend, authentification. À la fin de la
séance 6, ce socle existe.

**L'évaluation porte sur les fonctionnalités que vous ajoutez à ce socle.** Chaque
fonctionnalité suit le flow travaillé en séance 6 : fiche feature, plan validé, implémentation
avec l'agent, pull request, revue, merge. Ce qui est jugé, c'est la qualité de ces ajouts et de
la démarche qui les a produits, dans le respect de l'architecture cible et de la stack commune.

### La note

Une note sur 20, sur le projet de groupe. Le détail complet est dans la
grille d'évaluation ; voici la logique.

| Bloc                                         | Ce que je regarde                                                                                       |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **Processus produit & agentic**        | Vos specs, vos instructions projet, vos documents de review, vos traces de prompts avec les itérations |
| **Qualité technique & architecture**  | L'API, le schéma, les migrations, l'auth, la gestion d'erreurs, Docker                                 |
| **Flow d'équipe**                     | Pull requests, reviews réelles, tests verts                                                            |
| **Qualité du rendu & recul critique** | Projet livré, clarté des choix documentés, retour d'expérience honnête sur l'agent                 |

Deux points qui comptent beaucoup, et qu'on a tendance à sous-estimer :

1. **Un démarrage qui fonctionne du premier coup.** `git clone`, `cp .env.example .env`,
   `docker compose up`.
2. **Un retour d'expérience honnête.** Expliquer précisément où l'agent s'est trompé, comment vous
   vous en êtes aperçus et ce que vous avez corrigé a plus de valeur qu'affirmer que tout s'est bien
   passé.

### Points de vigilance

- Le respect de la stack commune est nécessaire pour que le projet puisse être évalué.
- Pensez à conserver des traces de votre usage de l'agent : instructions, reviews et prompts.
- Ne commitez jamais de secret dans le dépôt. Si cela arrive, signalez-le immédiatement et
  remplacez le secret concerné.

---

## 9. Comment travailler dans ce module

Quelques conseils, tirés des années précédentes.

**Faites tourner ce que vous produisez.** C'est sans doute le réflexe le plus utile du module. Du code
généré qui n'a pas été exécuté n'est pas du code, c'est une hypothèse. Testez à chaque lot, pas à
la fin de la séance.

**Lisez les diffs.** Les suppressions autant que les ajouts. C'est là que se cachent les
mauvaises surprises.

**Écrivez ce que vous voulez avant de le demander.** Cinq minutes de spécification écrite valent
mieux qu'une heure d'allers-retours avec un agent qui ne comprend pas ce que vous voulez. Vous
verrez la différence dès la séance 1.

**N'hésitez pas à demander de l'aide.** Au-delà d'une vingtaine de minutes bloqués sur un bug ou
sur un agent qui tourne en rond, venez me voir ou sollicitez un autre groupe.

**Commitez souvent, sur des branches.**

---

## 10. Ce dépôt

```text
.
├── PRESENTATION.md   ← vous êtes ici
├── OUTILS.md          ← installation des outils, à faire avant la séance 1
├── README.md         ← l'index et le calendrier
├── seances/          ← les 7 séances : un dossier cours/ et un dossier tp/ par séance
└── templates/        ← modèles à copier dans votre dépôt (fiche feature, plan d'implémentation)
```
