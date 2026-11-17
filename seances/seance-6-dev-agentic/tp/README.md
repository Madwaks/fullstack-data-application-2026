# TP — Séance 6 : livrer une feature avec un agent

## Ce que vous allez faire

Vous allez outiller votre dépôt pour travailler avec un agent — un fichier d'instructions, un
skill et deux agents spécialisés — puis dérouler avec eux, de bout en bout, une feature guidée :
**les avis sur les prêts terminés**.

Ce TP est la répétition générale du projet. Le workflow que vous construisez ici est celui que
vous réutiliserez pour chacune de vos propres features.

En séance, je vous propose d'aller jusqu'au plan validé (étapes 0 à 4). L'implémentation, la
revue et la PR (étapes 5 à 8) se terminent chez vous.

## Objectifs du TP

À la fin de ce TP, vous saurez :

- écrire un fichier d'instructions court et utile, commun à plusieurs outils ;
- écrire un skill dont la description le déclenche au bon moment ;
- définir un agent spécialisé avec des outils restreints ;
- produire avec l'agent une fiche feature et un plan, et les valider ;
- implémenter un plan étape par étape, tests au vert à chaque étape ;
- faire relire le code par un agent à contexte vierge, puis le relire vous-même ;
- prouver chaque critère d'acceptation par un test.

## Prérequis

- Le TP de la séance 5 terminé : authentification, propriété des ressources, tests au vert avec
  `docker compose run --rm backend pytest`.
- Les deux templates du module, que vous allez copier dans votre dépôt :
  [fiche-feature.md](../../../templates/fiche-feature.md) et
  [plan-implementation.md](../../../templates/plan-implementation.md).
- Votre agent : Copilot dans VS Code par défaut. Si vous avez Claude Code ou Codex, vous pouvez
  les utiliser ; chaque étape indique où ranger les fichiers pour eux.

Travaillez sur une branche dédiée :

```bash
git switch -c feature/avis
```

---

## Étape 0 — Un fichier d'instructions commun

Créez `AGENTS.md` à la racine du dépôt. C'est la source de vérité sur votre projet pour tous les
outils.

Visez une soixantaine de lignes au plus. Il contient :

- la stack et l'arborescence (`backend/`, `frontend/`, où sont routers, services, repositories) ;
- les commandes : démarrer, lancer les tests, créer et appliquer une migration ;
- les conventions que vous avez fixées pendant le module : où vit la logique métier, codes HTTP,
  nommage des tests (`test_ac_<story>_<critère>_...`) ;
- les interdits : pas de secret dans le code, pas de modification d'une migration déjà appliquée,
  pas d'identité lue dans le corps d'une requête.

Faites ensuite pointer les autres outils vers ce fichier :

| Outil | Ce qu'il faut faire |
|---|---|
| Copilot | Rien : il lit `AGENTS.md`. Si vous avez déjà un `.github/copilot-instructions.md`, réduisez-le à ce qui est propre à Copilot, ou fusionnez-le dans `AGENTS.md`. |
| Claude Code | Rien : il lit `AGENTS.md` tant que le dépôt ne contient pas de `CLAUDE.md` (version récente de Claude Code requise). Si vous avez déjà un `CLAUDE.md`, réduisez-le à la ligne `@AGENTS.md`. |
| Codex | Rien : il lit `AGENTS.md`. |

**Vérifiez votre compréhension** (à discuter en binôme) : pourquoi ce fichier doit-il rester
court ? Qu'est-ce qui, dans votre premier jet, relèverait plutôt d'un skill ?

---

## Étape 1 — Le skill `fiche-feature`

Copiez les deux templates du module dans votre dépôt :

```text
docs/templates/fiche-feature.md
docs/templates/plan-implementation.md
```

Créez ensuite le skill. Dans Copilot, il se range dans `.github/skills/fiche-feature/SKILL.md`
(Claude Code : `.claude/skills/…` ; Codex : `.agents/skills/…`). Voici un point de départ, à
compléter :

```markdown
---
name: fiche-feature
description: Rédige la fiche d'une nouvelle fonctionnalité de GearShare dans
  docs/features/<nom>/fiche.md. À utiliser quand on demande de cadrer, spécifier,
  décrire ou rédiger la PRD d'une feature, avant tout plan ou tout code.
---

# Rédiger une fiche feature

1. Ne rédige rien tout de suite. Pose d'abord des questions, une série à la fois, sur :
   le problème, les utilisateurs, les cas de refus, ce qui est hors périmètre.
2. Lis le code concerné (modèles, services, routers) pour remplir l'évaluation technique.
   Signale explicitement tout prérequis absent de l'existant.
3. Remplis docs/templates/fiche-feature.md et écris le résultat dans
   docs/features/<nom>/fiche.md.
4. Dans la section « Options et compromis », propose des options mais laisse la colonne
   « Décision » vide : c'est à moi de trancher.
5. ...
```

Complétez la procédure avec au moins deux règles qui vous semblent manquer. Par exemple : chaque
user story a au moins un critère de refus ; les critères ne mentionnent ni route ni code HTTP.

**Vérifiez votre compréhension** : relisez votre `description`. Si vous écriviez à l'agent
« on va ajouter des avis, tu peux m'écrire la spec ? », votre skill serait-il sélectionné ?

---

## Étape 2 — Deux agents spécialisés

Vous allez créer un **planificateur** et un **relecteur**. Tous deux sont en lecture seule : ils
ne modifient jamais le code.

Dans Copilot, ils se rangent dans `.github/agents/` (Claude Code : `.claude/agents/<nom>.md` ;
Codex : `.codex/agents/<nom>.toml`, un fichier TOML avec les champs `name`, `description` et
`developer_instructions`).

`.github/agents/planificateur.agent.md` :

```markdown
---
description: Rédige le plan d'implémentation d'une feature à partir de sa fiche validée.
  Ne modifie jamais le code.
tools: ['read', 'search']
---

Tu es le planificateur de GearShare. On te donne une fiche feature validée.

1. Lis la fiche, puis le code concerné, pour connaître les conventions en place.
2. Remplis docs/templates/plan-implementation.md pour le seul MVP et rends le plan
   dans ta réponse : je l'enregistrerai moi-même dans docs/features/<nom>/plan.md.
3. Chaque étape doit pouvoir être implémentée, testée et relue seule.
4. Chaque critère d'acceptation de la fiche apparaît dans le tableau de traçabilité.
5. Si la fiche est ambiguë, pose la question au lieu de choisir.
```

`.github/agents/relecteur.agent.md` : écrivez-le vous-même. Il doit :

- n'avoir que des outils de lecture et de recherche, plus l'exécution des tests si votre outil le
  permet ;
- relire le diff de la branche par rapport à `main`, et le comparer à la fiche et au plan ;
- appliquer la checklist ci-dessous ;
- rendre une liste de défauts au format `fichier:ligne — problème — correction proposée`, et ne
  rien corriger lui-même ;
- dire explicitement ce qu'il a vérifié sans rien trouver.

Checklist à intégrer au relecteur, une ligne par séance du module :

- [ ] **API** : validation dans les schémas Pydantic, pas dans des `if` du router ; codes de
  statut conformes au plan.
- [ ] **Tests** : un test par critère d'acceptation ; aucun test qui reste vert quand on casse la
  règle qu'il protège.
- [ ] **Base** : les règles qui peuvent l'être sont garanties par une contrainte (`UNIQUE`,
  `CHECK`, clé étrangère) ; contraintes nommées.
- [ ] **Couches** : logique métier dans les services ; migration présente, réversible et non
  destructrice.
- [ ] **Sécurité** : chaque route d'écriture protégée ; identité tirée du jeton ; `403` sur
  violation de propriété.
- [ ] **Périmètre** : aucun fichier modifié hors de ceux prévus par le plan.

Pour utiliser un agent dans Copilot, sélectionnez-le dans le sélecteur d'agents du chat. Si VS
Code signale un nom d'outil inconnu dans l'en-tête, choisissez les outils avec le bouton de
configuration des outils : les noms évoluent d'une version à l'autre.

---

## Étape 3 — La fiche feature

Voici l'intuition de départ, telle qu'elle vous arrive :

> Lors d'une enquête auprès des utilisateurs de GearShare, six utilisateurs sur dix disent hésiter à
> emprunter du matériel à quelqu'un qu'ils ne connaissent pas. Plusieurs prêteurs regrettent de
> ne pas pouvoir « se faire une réputation ».

Ouvrez une **nouvelle conversation** et demandez à l'agent de cadrer la feature avec votre skill.
Répondez à ses questions. L'idée est de le laisser vous interroger, plutôt que de lui souffler la solution.

Quand la fiche est écrite, relisez-la et tranchez la section « Options et compromis ». Je vous
propose de retenir pour le MVP :

- un prêt devient terminé quand **le prêteur le clôture** explicitement ;
- un avis = une note entière de 1 à 5 et un commentaire optionnel, **un seul par réservation**,
  par **l'emprunteur** uniquement, **non modifiable** ;
- la **moyenne et le nombre d'avis** sont calculés à la lecture et affichés sur l'annonce.

Si l'agent n'a pas relevé de lui-même qu'aucune route ne permet aujourd'hui de terminer une
réservation, c'est un bon indicateur de la qualité de son exploration : notez-le, et ajoutez ce
prérequis à la fiche.

Avant de passer à la suite, cochez :

- [ ] Le problème est formulé sans solution ; l'hypothèse a une métrique.
- [ ] Au moins trois user stories : clôturer un prêt, laisser un avis, voir la réputation.
- [ ] Les critères couvrent les refus : non connecté, pas l'emprunteur, prêt non terminé, avis en
  double, note hors bornes, réservation inexistante.
- [ ] Clôturer un prêt est réservé au propriétaire du matériel, et seulement pour une réservation
  `active`.
- [ ] Le hors périmètre mentionne au moins : modification d'un avis, notation de l'emprunteur,
  modération.
- [ ] Chaque compromis a une décision et sa raison, écrites par vous.

Passez le statut de la fiche à « validée » et commitez-la.

---

## Étape 4 — Le plan

Dans une **nouvelle conversation**, sélectionnez l'agent planificateur et donnez-lui la fiche.
Enregistrez le plan qu'il rend dans `docs/features/avis/plan.md`.

Relisez le plan. C'est la porte la plus rentable de tout le workflow : prenez le temps qu'il
faut.

- [ ] Le prérequis (clôturer une réservation) est la première étape.
- [ ] L'ordre va de la base vers le frontend ; aucune étape ne dépend d'une étape suivante.
- [ ] Chaque étape a une vérification exécutable.
- [ ] La migration crée la table `avis` avec `UNIQUE` sur la réservation et `CHECK` sur la note,
  et son `downgrade` est écrit.
- [ ] Le tableau de traçabilité contient tous les critères de la fiche, sans ligne vide.
- [ ] Rien dans le plan ne sort du MVP.

Corrigez le plan — à la main ou en renvoyant vos remarques au planificateur — jusqu'à ce que
toutes les cases soient cochées. Passez-le à « validé » et commitez-le.

---

## Étape 5 — L'implémentation, une étape à la fois (à terminer chez vous)

Pour chaque étape du plan :

1. Demandez à l'agent d'implémenter **cette étape seulement**, en citant le plan.
2. Laissez-le lancer les tests jusqu'au vert.
3. Lisez le diff. S'il touche un fichier absent de l'étape, demandez-lui pourquoi avant
   d'accepter.
4. Commitez, avec un message qui cite l'étape.

Une conversation neuve toutes les deux ou trois étapes est une bonne habitude : le plan et le
code commité suffisent à reprendre le fil.

---

## Étape 6 — La revue (à terminer chez vous)

Dans une **nouvelle conversation**, sélectionnez l'agent relecteur et demandez-lui de relire la
branche `feature/avis`.

Pour chaque défaut remonté, décidez : corriger, ou écarter avec une raison. Puis relisez
vous-même le diff complet.

Faites enfin l'exercice de la séance 2 sur trois tests de votre choix : cassez volontairement la
règle protégée (retirez le contrôle de l'emprunteur, retirez la contrainte `UNIQUE`…), relancez.
Le test doit passer au rouge. Restaurez.

**Vérifiez votre compréhension** : pourquoi le relecteur travaille-t-il dans une conversation
neuve, et non dans celle où le code a été écrit ?

---

## Étape 7 — La recette (à terminer chez vous)

- [ ] `grep -rn "test_ac_" backend/tests` retrouve un test pour chaque ligne du tableau de
  traçabilité.
- [ ] `docker compose run --rm backend pytest` passe intégralement.
- [ ] Vous avez joué la recette manuelle du plan dans le navigateur : clôturer un prêt en tant que
  prêteur, laisser un avis en tant qu'emprunteur, voir la moyenne sur l'annonce, et constater les
  messages d'erreur sur un second avis.

---

## Étape 8 — La pull request (à terminer chez vous)

Ouvrez la PR de `feature/avis` vers `main`. Sa description renvoie à la fiche et au plan, liste
les critères couverts et ce qui a été écarté de la revue. Faites-la relire par un membre de votre
groupe avant de fusionner.

---

## Ce que vous devez me rendre à la fin du TP

Sur le dépôt Git de votre projet :

1. **`AGENTS.md`**.
2. **Le skill `fiche-feature`** et **les agents planificateur et relecteur**, dans les dossiers de
   votre outil.
3. **`docs/templates/`** avec les deux templates.
4. **`docs/features/avis/fiche.md`** et **`docs/features/avis/plan.md`**, au statut validé.
5. **La feature implémentée**, un commit par étape du plan, tests au vert.
6. **La PR** relue et fusionnée.

## Pour aller plus loin

- **Un hook** : faites lancer automatiquement le lint après chaque modification de fichier par
  l'agent. Comparez avec une consigne dans `AGENTS.md` : laquelle est respectée à coup sûr ?
- **Un deuxième skill** : `nouvelle-verticale`, qui ajoute modèle, migration, repository, service,
  router et tests selon vos conventions. Testez-le sur une petite ressource.
- **La V2** : reprenez le workflow depuis la fiche pour la notation de l'emprunteur par le
  prêteur. Qu'est-ce qui change dans l'autorisation et dans la contrainte d'unicité ?
- **Comparer deux outils** : si un membre du groupe a Claude Code ou Codex, faites planifier la
  même fiche par les deux et comparez les plans.
