# Fiche feature — <nom de la feature>

> Copiez ce fichier dans `docs/features/<nom-feature>/fiche.md`. Les sections 1 à 5 décrivent le
> **quoi** et le **pourquoi** ; les sections 6 à 8 le **coût** et les **décisions**. Rien sur le
> **comment** détaillé : c'est le rôle du plan d'implémentation.

**Statut** : brouillon / validée
**Auteurs** :
**Date** :

## 1. Le problème

- Quel problème rencontrent les utilisateurs ? Formulez un problème, pas une solution.
- Quel signal vous fait penser qu'il existe ?

## 2. L'hypothèse et la métrique

> *Si nous [changement], alors [utilisateurs] [comportement attendu].*

- **Métrique** : ce qu'on mesurerait pour savoir si l'hypothèse était juste.

## 3. Les utilisateurs concernés

- Rôle 1 (ex. emprunteur) : ce qu'il cherche.
- Rôle 2 :

## 4. User stories et critères d'acceptation

Format des stories : *En tant que [rôle], je veux [action] afin de [bénéfice].*
Format des critères : *Given / When / Then*, observables de l'extérieur. **Incluez les cas de
refus** (non connecté, pas le droit, ressource absente, doublon, donnée invalide).

### US-01 — <titre>

En tant que ..., je veux ... afin de ...

```text
AC-01.1  Given ...
         When  ...
         Then  ...

AC-01.2  Given ...
         When  ...
         Then  ...
```

### US-02 — <titre>

...

## 5. Hors périmètre

Ce que cette version ne fait **pas**, volontairement.

- ...

## 6. Évaluation technique

### 6.1. Impacts par couche

| Couche | Impact |
|---|---|
| Base de données (tables, contraintes, migration) | |
| Modèle métier (règles, où elles sont vérifiées) | |
| API (routes, codes de statut) | |
| Autorisation (qui a le droit de quoi) | |
| Frontend (écrans, formulaires) | |
| Prérequis absents de l'existant | |

### 6.2. Risques

- Sécurité :
- Données existantes :
- Performance :

### 6.3. Taille estimée

S / M / L — et pourquoi.

## 7. Options et compromis

Une ligne par choix structurant. La colonne « Décision » est remplie par vous, pas par l'agent.

| Question | Option A | Option B | Décision et raison |
|---|---|---|---|
| | | | |

## 8. MVP et itérations suivantes

- **MVP** : la plus petite version qui permet de tester l'hypothèse. Listez les user stories
  incluses.
- **V2** :
- **Plus tard / backlog** :

## 9. Questions ouvertes

- ...
