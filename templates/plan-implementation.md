# Plan d'implémentation — <nom de la feature>

> Copiez ce fichier dans `docs/features/<nom-feature>/plan.md`. Le plan part d'une fiche
> **validée** et ne porte que sur le MVP. Chaque étape doit pouvoir être implémentée, testée et
> relue seule, en laissant l'application dans un état qui marche.

**Fiche** : [fiche.md](fiche.md)
**Statut** : brouillon / validé / en cours / livré

## 1. Rappel du périmètre

- User stories couvertes par ce plan : US-01, US-02, ...
- Hors plan (renvoyé à une itération suivante) : ...

## 2. Décisions retenues

Reprise des décisions de la section 7 de la fiche, et décisions techniques prises en écrivant le
plan (nom des routes, emplacement d'une règle, choix de migration).

- ...

## 3. Étapes

Une étape = un commit (ou une PR) cohérent. Ordre : du bas vers le haut (base, puis métier, puis
API, puis frontend), en commençant par les prérequis.

### Étape 1 — <titre>

- **Objectif** : une phrase.
- **Fichiers touchés** :
  - `backend/app/...`
- **Changements** :
  - ...
- **Tests à écrire** :
  - `test_ac_01_2_...` : ce qu'il vérifie
- **Critères d'acceptation couverts** : AC-01.2
- **Vérification** : la commande ou l'appel qui prouve que l'étape est finie.

  ```bash
  docker compose run --rm backend pytest -k ...
  ```

### Étape 2 — <titre>

...

## 4. Traçabilité critères → tests

Chaque critère de la fiche apparaît ici. Une ligne vide dans la colonne « Test » est un critère
non livré.

| Critère | Test | Étape |
|---|---|---|
| AC-01.1 | `test_ac_01_1_...` | 3 |
| AC-01.2 | | |

## 5. Migration et retour arrière

- La migration est-elle réversible (`downgrade`) ? Que devient une donnée existante ?
- Que faut-il faire si l'on doit annuler la feature après livraison ?

## 6. Recette manuelle

Le parcours à jouer dans le navigateur avant de déclarer la feature terminée.

1. ...
