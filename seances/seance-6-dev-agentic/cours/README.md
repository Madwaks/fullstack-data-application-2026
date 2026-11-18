# Cours — Séance 6 : développer une feature avec un agent

Vous savez maintenant construire GearShare couche par couche : une API, des tests, une base
relationnelle, une architecture en couches, une authentification. Il vous reste à apprendre à
**faire naître une fonctionnalité** — de l'idée jusqu'à la PR fusionnée — et à le faire avec un
agent de code sans perdre la maîtrise de ce qu'il produit.

C'est la dernière séance avant le projet. Ensuite, vous imaginerez vos propres fonctionnalités
pour GearShare et vous les livrerez de bout en bout avec l'outil de votre choix : GitHub Copilot,
Claude Code ou Codex.

En séance, je passe rapidement sur chaque partie. Ce document est écrit pour être relu à tête
reposée : prenez le temps de le parcourir avant de démarrer vos propres features.

- [Cours — Séance 6 : développer une feature avec un agent](#cours--séance-6--développer-une-feature-avec-un-agent)
  - [Objectifs pédagogiques](#objectifs-pédagogiques)
  - [Déroulé de la séance](#déroulé-de-la-séance)
  - [Partie 1 — La vie d'une feature en entreprise](#partie-1--la-vie-dune-feature-en-entreprise)
    - [1.1. L'intuition business](#11-lintuition-business)
    - [1.2. La PRD : le quoi et le pourquoi](#12-la-prd--le-quoi-et-le-pourquoi)
    - [1.3. L'évaluation technique](#13-lévaluation-technique)
    - [1.4. Les compromis](#14-les-compromis)
    - [1.5. Le MVP et les itérations](#15-le-mvp-et-les-itérations)
    - [1.6. Le découpage en étapes livrables](#16-le-découpage-en-étapes-livrables)
    - [1.7. Des critères d'acceptation aux tests](#17-des-critères-dacceptation-aux-tests)
    - [1.8. Mesurer, puis itérer](#18-mesurer-puis-itérer)
  - [Partie 2 — Comment fonctionne un agent de code](#partie-2--comment-fonctionne-un-agent-de-code)
    - [2.1. La boucle agentique](#21-la-boucle-agentique)
    - [2.2. Le contexte, une ressource rare](#22-le-contexte-une-ressource-rare)
    - [2.3. Le fichier d'instructions](#23-le-fichier-dinstructions)
    - [2.4. Les skills](#24-les-skills)
    - [2.5. Les subagents](#25-les-subagents)
    - [2.6. Les autres briques](#26-les-autres-briques)
    - [2.7. Copilot, Claude Code, Codex : les mêmes concepts](#27-copilot-claude-code-codex--les-mêmes-concepts)
  - [Partie 3 — Le workflow agentic d'une feature](#partie-3--le-workflow-agentic-dune-feature)
    - [3.1. Une étape, un artefact, une porte](#31-une-étape-un-artefact-une-porte)
    - [3.2. Ce que vous ne déléguez pas](#32-ce-que-vous-ne-déléguez-pas)
    - [3.3. Les échecs typiques, et la séance qui vous apprend à les voir](#33-les-échecs-typiques-et-la-séance-qui-vous-apprend-à-les-voir)
  - [Synthèse](#synthèse)
  - [Pour aller plus loin](#pour-aller-plus-loin)

## Objectifs pédagogiques

À la fin de ce cours, vous saurez :

- dérouler les étapes d'une feature en entreprise, de l'intuition business à la mesure ;
- rédiger une fiche feature : problème, hypothèse, user stories, critères d'acceptation ;
- évaluer l'impact technique d'une feature et arbitrer entre valeur et complexité ;
- définir un MVP et repousser le reste dans des itérations suivantes ;
- découper une feature en étapes livrables, chacune vérifiable ;
- traduire chaque critère d'acceptation en au moins un test ;
- expliquer comment fonctionne un agent de code : boucle, contexte, outils ;
- distinguer fichier d'instructions, skill et subagent, et savoir quand utiliser chacun ;
- retrouver ces concepts dans Copilot, Claude Code et Codex ;
- organiser un workflow où l'agent produit et où vous validez à chaque étape.

## Déroulé de la séance

1. Partie 1 — la vie d'une feature, illustrée sur la notation dans GearShare ;
2. Partie 2 — agents, skills, subagents ;
3. Partie 3 — le workflow agentic, démo du flow complet ;
4. [TP](../tp/README.md) — outiller votre dépôt et lancer la feature « avis ».

Le TP se termine chez vous : il est la répétition générale du projet.

---

## Partie 1 — La vie d'une feature en entreprise

Une feature ne commence pas par du code, et elle ne se termine pas au merge. Entre les deux, une
équipe produit enchaîne des étapes qui ont toutes le même principe : **chaque étape produit un
document, et ce document est validé par quelqu'un avant de passer à la suivante**. On appelle ces
validations des *portes*. Elles coûtent quelques minutes ; une erreur qui les franchit coûte des
jours.

![Les étapes d'une feature : intuition business, PRD, évaluation technique, compromis et MVP, plan, code et revue, tests des critères, mesure. La mesure relance une itération suivante qui repart de l'intuition business.](schemas/cycle-feature.svg)

*Chaque flèche est une porte : l'étape produit un document, quelqu'un le valide avant de passer à la suivante. En bleu, le plan, la porte la plus rentable (voir partie 3).*

Tout ce cours s'appuie sur un exemple fil rouge : **les avis sur GearShare**. Vous l'implémenterez
en TP.

### 1.1. L'intuition business

Le point de départ est un **signal** : un retour utilisateur, une donnée d'usage, une demande
commerciale, un choix stratégique. Le réflexe à prendre est de formuler un **problème**, pas une
solution.

| Signal | Ce qu'on attend | À éviter |
|---|---|---|
| Retour utilisateur (enquête) | « Les utilisateurs hésitent à emprunter à quelqu'un qu'ils ne connaissent pas. » | « Il faut ajouter des notes. » |
| Retour utilisateur (support) | « Prêteur et emprunteur n'arrivent pas à se mettre d'accord sur le lieu et l'heure de la remise du matériel. » | « Il faut une messagerie entre utilisateurs. » |
| Donnée d'usage | « Un prêt sur cinq est rendu en retard, et les prêteurs ne savent pas quand relancer. » | « Il faut envoyer des rappels par e-mail. » |
| Donnée d'usage | « La moitié des recherches se terminent sans aucune réservation. » | « Il faut des filtres de recherche avancés. » |
| Demande d'un partenaire | « Le BDE a du matériel à prêter, mais aucun de ses membres ne veut l'engager sur son compte personnel. » | « Il faut des comptes pour les associations. » |

Une solution formulée trop tôt ferme toutes les autres. Pour la première ligne, le vrai levier
est peut-être un badge « étudiant vérifié », pas des notes. Pour la deuxième, un créneau de
remise choisi au moment de la réservation suffit peut-être, sans messagerie complète. Pour la
quatrième, il faut d'abord comprendre pourquoi les recherches échouent : des filtres ne servent
à rien si le matériel cherché n'existe tout simplement pas sur la plateforme.

On transforme ensuite le problème en **hypothèse testable**, avec une **métrique** qui dira si
l'on avait raison :

> *Si les emprunteurs voient la fiabilité d'un prêteur, alors ils réserveront davantage.
> Métrique : taux de réservation des annonces consultées, avant et après.*

Sans métrique, vous ne saurez jamais si la feature a servi à quelque chose.

### 1.2. La PRD : le quoi et le pourquoi

La PRD (*Product Requirements Document*) décrit **ce qu'on construit et pourquoi** — jamais
**comment**. Dans ce module, on en utilise une version courte : la **fiche feature**
([template](../../../templates/fiche-feature.md)). Elle contient :

- le problème, l'hypothèse et la métrique ;
- les utilisateurs concernés ;
- les **user stories** : *En tant que [rôle], je veux [action] afin de [bénéfice]* ;
- pour chaque story, des **critères d'acceptation** vérifiables, au format *Given / When / Then* ;
- ce qui est **hors périmètre**, écrit noir sur blanc.

Un critère d'acceptation décrit un comportement observable de l'extérieur, sans jargon technique :

```text
US-01 — En tant qu'emprunteur, je veux noter un prêt terminé afin d'informer
        les futurs emprunteurs.

AC-01.1  Given un prêt terminé dont je suis l'emprunteur
         When  je laisse une note de 4 et un commentaire
         Then  l'avis est enregistré et visible sur l'annonce

AC-01.2  Given un prêt encore en cours
         When  je tente de laisser un avis
         Then  la demande est refusée car le prêt n'est pas terminé

AC-01.3  Given un prêt que j'ai déjà noté
         When  je tente de laisser un second avis
         Then  la demande est refusée
```

Remarquez que les cas de refus sont des critères à part entière. Une PRD qui ne contient que des
cas nominaux produit du code qui ne gère que des cas nominaux — c'est vrai pour un développeur
humain, et encore plus pour un agent.

La section **hors périmètre** est la plus sous-estimée. « Modifier un avis » n'y figure pas par
oubli : on a décidé de ne pas le faire maintenant. Sans cette ligne, quelqu'un — ou un agent —
finira par l'implémenter « pour bien faire ».

### 1.3. L'évaluation technique

La PRD validée, le tech lead (ou vous) lit le code existant et répond à une question : **qu'est-ce
que cette feature touche, et qu'est-ce qui peut mal tourner ?**

Passez chaque couche en revue :

| Couche | Question à se poser | Pour les avis |
|---|---|---|
| Base de données | Nouvelle table ? Contrainte ? Migration sur des données existantes ? | Table `avis`, `UNIQUE` sur la réservation, `CHECK` sur la note |
| Modèle métier | Quelles règles ? Où les vérifier ? | Prêt terminé, auteur = emprunteur |
| API | Quelles routes, quels codes ? | `POST` d'un avis : `201`, `401`, `403`, `404`, `409`, `422` |
| Autorisation | Qui a le droit de faire quoi ? | Seul l'emprunteur de la réservation |
| Frontend | Quels écrans changent ? | Formulaire d'avis, moyenne sur l'annonce |
| Existant | Un prérequis manque-t-il ? | Aucune route ne fait passer une réservation au statut `terminee` |

La dernière ligne est typique : l'évaluation technique révèle souvent un **prérequis invisible
depuis la PRD**. Dans votre application, une réservation peut être annulée, mais jamais
terminée — donc personne ne pourrait jamais laisser d'avis. Mieux vaut le découvrir maintenant
qu'au moment de la démo.

On termine par une **estimation grossière** (S, M, L) et une liste de **risques** : sécurité,
données existantes, performance, dépendances à d'autres équipes. Il ne s'agit pas d'un devis
précis : il s'agit de savoir si la feature tient dans une itération.

### 1.4. Les compromis

L'évaluation technique fait remonter des coûts que la PRD n'avait pas vus. C'est le moment du
dialogue entre produit et technique : **la complexité technique ajuste le périmètre**, et le
produit dit ce qui compte vraiment.

Pour chaque choix structurant, on liste les options et on tranche :

| Question | Option A | Option B | Ce qui fait pencher |
|---|---|---|---|
| Comment un prêt devient-il terminé ? | Le prêteur le clôture explicitement | Il l'est automatiquement quand `date_fin` est passée | A : simple, explicite, testable. B : pas d'action utilisateur, mais un état qui change sans écriture en base |
| La note moyenne | Calculée à chaque lecture (`AVG`) | Stockée sur l'annonce | A tant que le volume est faible. B impose de la garder cohérente |
| Un avis est-il modifiable ? | Non | Oui | Non pour la V1 : modifier impose historique, droits et anti-abus |
| Qui note qui ? | L'emprunteur note le prêt | Notation dans les deux sens | Un seul sens pour la V1 : le deuxième double l'autorisation et les tests |

Une bonne décision est **écrite** avec sa raison. Dans trois mois, quelqu'un demandera pourquoi
la moyenne n'est pas stockée ; la réponse doit être dans la fiche, pas dans votre mémoire.

### 1.5. Le MVP et les itérations

Le **MVP** (*Minimum Viable Product*) est la plus petite version de la feature qui permet de
**valider l'hypothèse**. Ce n'est pas une version bâclée : elle est testée, sécurisée et propre.
Elle est simplement **étroite**.

```text
MVP   : le prêteur clôture un prêt ; l'emprunteur laisse une note de 1 à 5 et un commentaire
        optionnel, une seule fois par prêt ; la moyenne et le nombre d'avis s'affichent sur
        l'annonce.

V2    : l'emprunteur est noté lui aussi ; un avis est modifiable pendant 48 h ;
        tri des annonces par note.

V3    : signalement et modération des avis.
```

Ce qui n'entre pas dans le MVP n'est pas perdu : il part dans le **backlog**, et la mesure de la
V1 dira s'il vaut la peine d'être fait. C'est tout l'intérêt d'itérer : on ne construit la V2 que
si la V1 a montré que le problème était le bon.

Deux pièges symétriques :

- **le MVP trop gros** : on veut tout livrer d'un coup, on ne livre rien pendant trois semaines,
  et on découvre à la fin que l'hypothèse était fausse ;
- **le MVP trop maigre** : on livre une note sans afficher la moyenne — l'hypothèse ne peut pas
  être testée, l'itération ne sert à rien.

### 1.6. Le découpage en étapes livrables

Le MVP arrêté, on écrit le **plan d'implémentation**
([template](../../../templates/plan-implementation.md)). Il découpe la feature en étapes, et
chaque étape :

- a un **objectif** en une phrase ;
- liste les **fichiers touchés** ;
- précise les **tests** à écrire ;
- se termine par une **vérification exécutable** (une commande, un appel HTTP) ;
- indique les **critères d'acceptation** qu'elle couvre.

Pour les avis, un découpage raisonnable :

1. clôture d'une réservation par le prêteur (le prérequis découvert en 1.3) ;
2. table `avis` et migration Alembic ;
3. repository et service de création d'avis, avec les règles métier ;
4. route `POST` et ses codes d'erreur ;
5. moyenne et nombre d'avis sur l'annonce ;
6. frontend.

Visez une application **qui marche à la fin de chaque étape**, tests au vert. Si une
étape ne peut pas être vérifiée seule, c'est le signe qu'il faut la redécouper.

### 1.7. Des critères d'acceptation aux tests

Un critère d'acceptation sans test n'est pas livré : c'est une promesse. La traduction est presque
mécanique, et c'est exactement le schéma *Arrange / Act / Assert* de la séance 2 :

| Critère | Test |
|---|---|
| *Given* un prêt terminé dont je suis l'emprunteur | Arrange : une réservation `terminee`, un jeton de l'emprunteur |
| *When* je laisse une note de 4 | Act : `POST` de l'avis |
| *Then* l'avis est enregistré et visible | Assert : `201`, puis l'avis apparaît en lecture |

```python
def test_ac_01_1_emprunteur_note_un_pret_termine(client, reservation_terminee, token_emprunteur):
    response = client.post(
        f"/reservations/{reservation_terminee.id}/avis",
        json={"note": 4, "commentaire": "Vélo en parfait état"},
        headers={"Authorization": f"Bearer {token_emprunteur}"},
    )

    assert response.status_code == 201
    avis = client.get(f"/items/{reservation_terminee.item_id}/avis").json()
    assert avis[0]["note"] == 4
```

Nommer les tests d'après les critères (`test_ac_01_1_...`) rend la traçabilité gratuite : un
`grep` suffit pour savoir si chaque critère est couvert.

Les tests automatisés ne remplacent pas la **recette** : avant de déclarer la story terminée, vous
la jouez vous-même dans le navigateur, comme un utilisateur. C'est là qu'on découvre le bouton
qui n'apparaît pas ou le message d'erreur incompréhensible.

### 1.8. Mesurer, puis itérer

La feature en production, on revient à la métrique de l'étape 1.1. Le taux de réservation a
monté ? On peut envisager la V2. Il n'a pas bougé ? L'hypothèse était peut-être fausse, et c'est
une information précieuse : elle évite de construire la V2 pour rien.

Dans ce module, vous ne mesurerez pas en production. Je vous demande tout de même d'inscrire la métrique dans
votre fiche : c'est elle qui montre que vous avez réfléchi au *pourquoi*.

---

## Partie 2 — Comment fonctionne un agent de code

### 2.1. La boucle agentique

Un agent de code, c'est un modèle de langage, des **outils**, et une **boucle** :

![La boucle agentique : rassembler le contexte en lisant et en cherchant, agir en éditant et en créant, vérifier en lançant les tests et en lisant la sortie, puis recommencer un tour. La boucle s'arrête quand l'agent estime avoir fini ou quand vous l'arrêtez.](schemas/boucle-agentique.svg)

*Ce qui fait un agent, c'est l'étape « Vérifier » : il constate les conséquences de ce qu'il fait. Sa qualité dépend donc directement de la boucle de vérification que vous lui donnez.*

À chaque tour, le modèle décide quel outil appeler, lit le résultat, et décide du tour suivant.
Il s'arrête quand il estime avoir fini — ou quand vous l'arrêtez.

Ce qui distingue un agent d'un chat, ce n'est pas qu'il est plus intelligent : c'est qu'il **peut
constater les conséquences de ce qu'il fait**. D'où une règle très concrète : **donnez-lui une
boucle de vérification rapide et fiable**. Un agent qui peut lancer
`docker compose run --rm backend pytest` corrige lui-même une grande partie de ses erreurs. Un
agent qui ne le peut pas vous les laisse.

Le corollaire est moins confortable : l'agent vérifie **ce qu'on lui a demandé de vérifier**. Si
les tests sont faibles, il rend avec assurance un code faux qui passe des tests faibles.

### 2.2. Le contexte, une ressource rare

Tout ce que l'agent « sait » pendant une tâche tient dans sa **fenêtre de contexte** : vos
messages, les fichiers lus, les sorties de commandes, ses propres réponses. Cette fenêtre est
limitée et, bien avant d'être pleine, **plus elle est chargée, moins l'agent est précis** : il
oublie une consigne du début, mélange deux fichiers, reprend une hypothèse abandonnée.

Toute l'architecture qui suit — fichiers d'instructions, skills, subagents — répond à une seule
question : **comment donner à l'agent le bon contexte, au bon moment, et rien de plus ?**

Quelques réflexes qui en découlent :

- une conversation par tâche ; quand le sujet change, on repart d'une conversation neuve ;
- l'état d'avancement vit dans des **fichiers** (la fiche, le plan), pas dans l'historique du
  chat — une nouvelle conversation peut alors reprendre le travail ;
- on pointe l'agent vers les fichiers utiles plutôt que de le laisser lire tout le dépôt.

### 2.3. Le fichier d'instructions

C'est un fichier Markdown à la racine du dépôt, **chargé automatiquement au début de chaque
conversation**. Il contient ce que l'agent doit savoir sur tout le projet :

- la stack et l'architecture (routers / services / repositories) ;
- les commandes : lancer l'application, les tests, les migrations ;
- les conventions : nommage, codes HTTP, où vit la logique métier ;
- les interdits : pas de secret dans le code, pas de migration éditée après coup.

Parce qu'il est chargé **à chaque fois**, il doit rester **court**. Chaque ligne consomme du
contexte dans toutes les conversations. Une procédure de vingt lignes qui ne sert qu'une fois par
semaine n'a rien à y faire : c'est le rôle d'un skill.

`AGENTS.md` est un format ouvert, lu directement par les trois outils. Copilot et Codex le
chargent toujours ; Claude Code le charge tant que le projet ne contient pas de `CLAUDE.md`. Si un
`CLAUDE.md` existe, c'est lui que Claude Code lit à la place : une ligne `@AGENTS.md` dans ce
fichier suffit alors à importer le reste. Un seul fichier de vérité, trois outils.

### 2.4. Les skills

Un skill est une **procédure réutilisable**, rangée dans un dossier :

![Le dossier .github/skills/fiche-feature contient SKILL.md, la procédure avec un en-tête name et description, template.md, une ressource que la procédure utilise, et scripts/verifier.py, un script optionnel. L'en-tête de SKILL.md est chargé dès le démarrage, son corps si la demande correspond, les autres fichiers seulement si la procédure le dit.](schemas/dossier-skill.svg)

*Un skill est un dossier. Seul l'en-tête de `SKILL.md` occupe le contexte en permanence : le reste n'est lu qu'au moment où il sert.*

```markdown
---
name: fiche-feature
description: Rédige la fiche d'une nouvelle feature GearShare à partir d'une idée.
  À utiliser quand on demande de cadrer, spécifier ou décrire une fonctionnalité.
---

1. Avant d'écrire quoi que ce soit, pose-moi des questions sur le problème, ...
2. ...
```

Le mécanisme clé est la **divulgation progressive** (*progressive disclosure*) :

1. au démarrage, l'agent ne charge que le `name` et la `description` de chaque skill — quelques
   lignes ;
2. quand votre demande correspond à une description, il lit le `SKILL.md` complet ;
3. il n'ouvre le template ou le script que lorsque la procédure le lui dit.

Vous pouvez donc avoir vingt skills sans encombrer le contexte. La conséquence pratique : **la
`description` est ce qui déclenche le skill**. Une description vague (« aide pour les features »)
ne sera jamais sélectionnée au bon moment ; décrivez *quand* l'utiliser.

Bons candidats pour un skill : rédiger une fiche feature selon votre template, écrire une
migration Alembic selon vos conventions, ajouter une verticale complète, préparer une description
de PR. En résumé, tout ce que vous expliquez à l'agent plus de deux fois.

Le format `SKILL.md` est un **standard ouvert**, partagé par Copilot, Claude Code et Codex. Un
skill écrit pour l'un fonctionne dans les autres ; seul le dossier où on le range change.

### 2.5. Les subagents

Un subagent est un agent **spécialisé**, défini dans un fichier, avec :

- un **rôle** et des consignes propres (son prompt système) ;
- une **liste d'outils** restreinte — un relecteur n'a pas besoin d'éditer ;
- éventuellement un **modèle** différent ;
- surtout, **son propre contexte**.

L'agent principal lui délègue une tâche ; le subagent travaille dans sa fenêtre à lui, lit
autant de fichiers qu'il le faut, puis ne renvoie **qu'un résumé**. Deux bénéfices :

1. **le contexte principal reste propre** : l'exploration de quarante fichiers n'y laisse
   qu'une page de conclusions ;
2. **le regard reste neuf** : un relecteur qui n'a pas vu le raisonnement de l'implémenteur n'en
   hérite pas les angles morts. Un agent qui relit son propre code dans la même conversation
   trouve presque toujours que c'est bien.

Trois subagents utiles pour une feature :

| Subagent | Outils | Ce qu'il rend |
|---|---|---|
| Explorateur | lecture, recherche | Les fichiers et conventions concernés par la feature |
| Planificateur | lecture, recherche | Un plan au format du template, sans toucher au code |
| Relecteur | lecture, recherche, lancer les tests | Une liste de défauts localisés `fichier:ligne`, sans corriger |

Restreindre les outils n'est pas un détail : c'est ce qui garantit qu'un planificateur ne se
mettra pas à coder « pour gagner du temps ».

**Skill ou subagent ?** Un skill dit **comment** faire une tâche, dans le contexte courant. Un
subagent dit **qui** la fait, dans un contexte séparé. On les combine souvent : le subagent
relecteur applique le skill « checklist de revue ».

### 2.6. Les autres briques

- **Le mode plan** : l'agent explore et propose un plan sans rien modifier. C'est la version
  intégrée du subagent planificateur.
- **Les hooks** : des commandes lancées automatiquement à un moment du cycle, par exemple le lint
  après chaque édition, ou un refus de toute commande qui toucherait à `.env`. Un hook ne dépend
  pas de la bonne volonté du modèle : il s'exécute à chaque fois.
- **Les serveurs MCP** (*Model Context Protocol*) : un protocole standard pour brancher des
  outils externes — le gestionnaire de tickets, une base de données, la documentation de
  l'entreprise. C'est ce qui permet à l'agent de lire un ticket Jira ou d'interroger PostgreSQL.
- **Les plugins** : un paquet qui regroupe skills, subagents, hooks et serveurs MCP, pour
  distribuer un workflow complet à toute une équipe.

En entreprise, vous trouverez souvent ce workflow déjà outillé : un plugin interne avec un skill
de cadrage, un planificateur, un relecteur, des hooks de sécurité. Savoir lire et modifier ces
fichiers fait partie du métier.

### 2.7. Copilot, Claude Code, Codex : les mêmes concepts

Les trois outils implémentent les mêmes idées ; seuls les noms de dossiers changent.

| Concept | GitHub Copilot (VS Code) | Claude Code | Codex |
|---|---|---|---|
| Instructions projet | `AGENTS.md` ou `.github/copilot-instructions.md` | `AGENTS.md`, ou `CLAUDE.md` s'il existe (prioritaire) | `AGENTS.md` |
| Instructions ciblées | `AGENTS.md` dans un sous-dossier, ou `.github/instructions/*.instructions.md` (`applyTo`) | `AGENTS.md` ou `CLAUDE.md` dans un sous-dossier | `AGENTS.md` dans un sous-dossier |
| Skills | `.github/skills/<nom>/SKILL.md` | `.claude/skills/<nom>/SKILL.md` | `.agents/skills/<nom>/SKILL.md` |
| Subagents | `.github/agents/<nom>.agent.md` | `.claude/agents/<nom>.md` | `.codex/agents/<nom>.toml` |
| Commande réutilisable | un skill appelé par `/<nom>` | un skill appelé par `/<nom>` | un skill appelé par `$<nom>` |
| Planifier sans éditer | agent *Plan* (`/plan`) | mode plan (`Shift+Tab` ou `/plan`) | mode plan (`/plan`) |

Côté Copilot, les anciens *prompt files* (`.github/prompts/*.prompt.md`) sont en voie
d'abandon : VS Code recommande de les convertir en skills, qui s'appellent eux aussi par `/<nom>`.

Ces outils évoluent tous les mois : la colonne qui vous concerne se vérifie dans la documentation
officielle (liens en fin de document). Ce qui ne bouge pas, ce sont les concepts : instructions
toujours chargées, procédures chargées à la demande, agents à contexte séparé.

---

## Partie 3 — Le workflow agentic d'une feature

### 3.1. Une étape, un artefact, une porte

On reprend les étapes de la partie 1. L'agent prend en charge la production ; vous gardez les
portes.

| Étape | Qui produit | Artefact | Porte : ce que vous vérifiez |
|---|---|---|---|
| Intuition business | Vous | Problème, hypothèse, métrique | — |
| Fiche feature | Skill `fiche-feature` : l'agent vous interroge, puis remplit le template | `docs/features/<feature>/fiche.md` | Les critères couvrent les refus ; le hors périmètre est explicite |
| Évaluation technique | Subagent explorateur ou planificateur | Section « Évaluation technique » de la fiche | Les prérequis manquants sont identifiés |
| Compromis et MVP | Vous, sur proposition de l'agent | Section « Compromis » et « MVP » de la fiche | Chaque décision a sa raison |
| Plan | Subagent planificateur | `docs/features/<feature>/plan.md` | Chaque étape est vérifiable seule ; chaque critère est couvert |
| Implémentation | Agent principal, une étape du plan à la fois | Code + tests, un commit par étape | Les tests passent ; le diff reste dans le périmètre de l'étape |
| Revue | Subagent relecteur, contexte vierge | Liste de défauts | Vous relisez le diff et les défauts remontés |
| Critères d'acceptation | Agent | Un test par critère | Vous jouez la recette dans le navigateur |
| PR | Agent | Description liée à la fiche | Revue humaine d'un coéquipier |

Le **plan** est la porte la plus rentable : dix minutes de relecture d'un plan évitent une heure
de relecture d'un diff qui part dans la mauvaise direction.

### 3.2. Ce que vous ne déléguez pas

- **Le problème et l'hypothèse.** L'agent peut reformuler, pas décider de ce qui compte pour vos
  utilisateurs.
- **Les compromis.** L'agent propose des options ; c'est vous qui portez la décision et sa raison.
- **La validation aux portes.** Que l'agent juge son code correct ne remplace pas votre relecture.
- **La compréhension du code fusionné.** Si une ligne vous reste obscure, prenez le temps de la
  comprendre (ou de vous la faire expliquer) avant de fusionner.

### 3.3. Les échecs typiques, et la séance qui vous apprend à les voir

Les défauts que produit un agent ne sont pas aléatoires : ce sont toujours les mêmes, et chaque
séance technique du module vous a appris à en repérer un.

| Ce que l'agent fait mal | Ce que vous voyez | Séance |
|---|---|---|
| Valide dans le router avec un `if`, au lieu du schéma Pydantic | Mauvais code d'erreur, contrainte absente de l'OpenAPI | 1 |
| Écrit des tests qui ne peuvent pas échouer, ou adapte le test au code | Test vert même quand on casse la règle | 2 |
| Oublie une contrainte en base (`UNIQUE`, `CHECK`, `ON DELETE`) | La règle ne tient que dans le code Python | 3 |
| Génère une migration destructrice, ou met de la logique dans le router | `DROP` + `ADD` au lieu d'un renommage, couches mélangées | 4 |
| Oublie l'autorisation, ou prend l'identité dans le corps de la requête | Un `403` manquant ; un `owner_id` accepté du client | 5 |
| Sort du périmètre | Un diff qui touche des fichiers absents du plan | 6 |

Un moyen simple de vérifier qu'un test sert à quelque chose : cassez volontairement la règle
qu'il protège, relancez-le. S'il reste vert, il ne teste rien.

---

## Synthèse

- Une feature suit un chemin : intuition, PRD, évaluation technique, compromis, MVP, plan, code,
  tests des critères, mesure. Chaque étape produit un document validé avant la suivante.
- Un critère d'acceptation sans test n'est pas livré ; un MVP est étroit, pas bâclé.
- Un agent est un modèle, des outils et une boucle ; sa qualité dépend de sa boucle de
  vérification et de la propreté de son contexte.
- Instructions : toujours chargées, donc courtes. Skills : procédures chargées à la demande.
  Subagents : contexte séparé, outils restreints, regard neuf.
- Ces concepts sont les mêmes dans Copilot, Claude Code et Codex.
- L'agent produit, vous gardez les portes : problème, compromis, plan, revue.

## Pour aller plus loin

- GitHub Copilot dans VS Code :
  [custom agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents),
  [personnalisation](https://code.visualstudio.com/docs/copilot/customization/overview)
- Claude Code : [documentation](https://code.claude.com/docs) (sections *Memory*, *Skills*,
  *Subagents*, *Hooks*)
- Codex : [skills](https://learn.chatgpt.com/docs/build-skills),
  [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents),
  [personnalisation](https://learn.chatgpt.com/docs/customization/overview)
- Le format ouvert des skills : [agentskills.io](https://agentskills.io)
- Le format ouvert `AGENTS.md` : [agents.md](https://agents.md)
