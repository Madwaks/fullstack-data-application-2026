# Séance 0 — Docker : histoire et fondamentaux (cours)

Cette séance 0 est une **mise à niveau optionnelle**, à faire en autonomie avant la séance 1. Si
vous avez déjà manipulé Docker (stage, projet précédent), parcourez-la rapidement pour vérifier
que vous maîtrisez le vocabulaire ; sinon, prenez le temps de la lire en entier avant de commencer
le TP.

- [Séance 0 — Docker : histoire et fondamentaux (cours)](#séance-0--docker--histoire-et-fondamentaux-cours)
  - [Objectifs pédagogiques](#objectifs-pédagogiques)
  - [1. Petite histoire du déploiement logiciel](#1-petite-histoire-du-déploiement-logiciel)
    - [1.1. Bare-metal](#11-bare-metal)
    - [1.2. Machines virtuelles](#12-machines-virtuelles)
    - [1.3. Conteneurs](#13-conteneurs)
  - [2. Pourquoi les conteneurs sont une révolution](#2-pourquoi-les-conteneurs-sont-une-révolution)
    - [2.1. Cascade, agile, DevOps : l'accélération du cycle de développement](#21-cascade-agile-devops--laccélération-du-cycle-de-développement)
    - [2.2. Infrastructure mutable vs infrastructure immuable](#22-infrastructure-mutable-vs-infrastructure-immuable)
    - [2.3. Scaling vertical vs scaling horizontal](#23-scaling-vertical-vs-scaling-horizontal)
    - [2.4. Ce que ça change concrètement pour vous](#24-ce-que-ça-change-concrètement-pour-vous)
  - [3. Terminologie Docker](#3-terminologie-docker)
  - [4. Construire une image : le Dockerfile](#4-construire-une-image--le-dockerfile)
  - [5. Lancer et gérer des conteneurs](#5-lancer-et-gérer-des-conteneurs)
  - [6. Les volumes](#6-les-volumes)
  - [7. Les réseaux Docker](#7-les-réseaux-docker)
    - [7.1. Le réseau `bridge` par défaut](#71-le-réseau-bridge-par-défaut)
    - [7.2. Les réseaux user-defined et le DNS embarqué](#72-les-réseaux-user-defined-et-le-dns-embarqué)
    - [7.3. Réseau et publication de port : deux choses différentes](#73-réseau-et-publication-de-port--deux-choses-différentes)
  - [8. Docker Compose et le DNS interne](#8-docker-compose-et-le-dns-interne)
  - [9. Aller plus loin](#9-aller-plus-loin)
    - [9.1. Images de base et Alpine](#91-images-de-base-et-alpine)
    - [9.2. Multi-stage builds](#92-multi-stage-builds)
    - [9.3. Registry d'images](#93-registry-dimages)
    - [9.4. Développer depuis un conteneur](#94-développer-depuis-un-conteneur)
  - [10. Synthèse et lien avec la suite du module](#10-synthèse-et-lien-avec-la-suite-du-module)

## Objectifs pédagogiques

À la fin de ce cours, vous devez être capables de :

- situer les conteneurs dans l'histoire du déploiement logiciel (bare-metal, machines virtuelles, conteneurs) ;
- expliquer en quoi les conteneurs répondent aux besoins des méthodes agile et DevOps ;
- utiliser le vocabulaire Docker correctement (image, conteneur, registry, tag, volume) ;
- écrire un `Dockerfile` simple et construire une image ;
- lancer, inspecter et arrêter des conteneurs en ligne de commande ;
- expliquer pourquoi deux conteneurs se joignent par IP mais pas par nom sur le réseau par défaut, et ce qu'un réseau *user-defined* change ;
- comprendre le rôle du réseau et du DNS interne de Docker Compose pour faire communiquer plusieurs services.

Ce socle vous servira dès la séance 1, quand vous lancerez votre API GearShare dans un conteneur.
Il sera complété au fil du module : la base de données PostgreSQL arrive en séance 3, et le
`docker-compose.yml` à trois services (backend, frontend, base de données) en séance 4.

## 1. Petite histoire du déploiement logiciel

Avant de parler de Docker, il faut comprendre le problème qu'il résout. Depuis toujours,
faire tourner une application soulève la même question : sur quelle machine, avec quelles
ressources, et comment isoler cette application des autres qui tournent à côté ?

### 1.1. Bare-metal

Historiquement, une application tourne directement sur une machine physique ("bare-metal"),
généralement hébergée dans un data center, qui n'appartient qu'à un seul locataire. Cette
approche garantit une sécurité et une exploitation maximale des ressources : rien n'est
partagé avec personne d'autre.

Mais le coût est élevé (acheter et maintenir du matériel), le délai de mise en service se
compte en jours ou en semaines, et une panne matérielle rend l'application indisponible
sans filet de sécurité. Faire évoluer les ressources (plus de RAM, plus de CPU) demande
souvent de changer de machine.

### 1.2. Machines virtuelles

Une couche d'hyperviseur, installée sur le matériel ou sur un système d'exploitation hôte,
permet de créer et gérer plusieurs machines virtuelles sur une même machine physique. Chaque
VM embarque son propre système d'exploitation complet.

Cela apporte plusieurs bénéfices : plusieurs applications peuvent cohabiter sur le même
matériel, le réseau peut être configuré virtuellement, les ressources physiques sont mieux
exploitées, et les sauvegardes (snapshots) renforcent la résilience face aux pannes. En
contrepartie, chaque VM a un coût : licences, ressources dédiées à son propre OS, temps de
démarrage de l'ordre de la minute.

### 1.3. Conteneurs

Les conteneurs reprennent le principe d'isolation des machines virtuelles, mais sans
dupliquer un système d'exploitation complet pour chaque instance. Un conteneur runtime — Docker
ou containerd par exemple — s'appuie directement sur le noyau de l'OS hôte pour isoler des
processus les uns des autres, tout en leur donnant l'illusion d'un environnement dédié
(système de fichiers, réseau, dépendances).

Résultat : des images légères (quelques dizaines à quelques centaines de Mo, contre plusieurs
Go pour une VM), un démarrage en quelques secondes voire millisecondes, une empreinte
ressources minimale, et un fonctionnement identique sur n'importe quel OS hôte compatible.
Chaque application devient une pièce indépendante et portable.

L'inconvénient principal est la marche d'apprentissage (nouveaux outils, nouveau vocabulaire,
parfois adapter du code ou des déploiements existants) et la nécessité de rester à jour sur un
écosystème qui évolue vite. Mais c'est ce découplage — et sa compatibilité native avec les
philosophies agile et DevOps — qui a fait des conteneurs un standard de l'industrie en une
dizaine d'années.

## 2. Pourquoi les conteneurs sont une révolution

Les conteneurs n'ont pas seulement rendu le déploiement plus rapide : ils ont changé la façon
dont les équipes de développement conçoivent, testent et livrent leurs applications.

### 2.1. Cascade, agile, DevOps : l'accélération du cycle de développement

Le développement en cascade (recueil des besoins → conception → implémentation → vérification
→ maintenance, dans cet ordre et sans retour en arrière) suppose un cycle long et un périmètre
figé dès le départ. Dans un contexte où plusieurs développeurs travaillent en parallèle sur un
produit qui évolue vite, cette approche est devenue largement obsolète.

La méthode agile, formalisée par le [manifeste agile](http://agilemanifesto.org/), découpe le
travail en cycles courts (souvent deux semaines), rythmés par des évènements réguliers : sprint
planning (définition et priorisation des tâches), daily standup (point quotidien sur l'avancement
et les blocages), démo (présentation du travail réalisé) et rétrospective (identification des
axes d'amélioration). Elle repose sur une livraison régulière de code de
qualité.

L'approche DevOps prolonge cette logique côté organisation : son objectif est de raccourcir le
temps entre une idée et sa mise en production, en automatisant les vérifications et le
déploiement.

**Premier point clé** : les conteneurs permettent d'empaqueter une application dans un
environnement identique, du poste du développeur jusqu'à la production, en passant par le
staging. C'est exactement ce dont l'agile et le DevOps ont besoin pour livrer vite et souvent,
sans surprise entre "ça marche chez moi" et "ça marche en prod".

### 2.2. Infrastructure mutable vs infrastructure immuable

Cette opposition est aussi connue sous le nom imagé **"pets vs cattle"** (animaux de compagnie
vs troupeau).

Une **infrastructure mutable** traite chaque machine comme un animal de compagnie : on la crée,
on la configure, on la patche régulièrement, on met à jour son OS et ses applications au fil du
temps, jusqu'à sa mise hors service. Ce cycle de vie est long et nécessite des interventions
souvent manuelles et ponctuelles — avec le risque d'oublier une mise à jour ou de mal la
documenter, provoquant un **configuration drift** (une dérive de configuration par rapport à
l'état attendu).

Une **infrastructure immuable** traite les machines comme un troupeau : on crée des instances
avec une version figée d'OS, d'application et de ressources, on les démarre, et dès qu'une mise
à jour est nécessaire, on crée de nouvelles instances à jour qui remplacent les anciennes
(supprimées, pas modifiées). Rien n'est jamais patché en place.

**Deuxième point clé** : à l'échelle du cloud, l'approche immuable est largement préférée,
parfois même la seule option réaliste — il est impossible de gérer manuellement chaque machine
d'une flotte de centaines d'instances. Les conteneurs, rapides à construire, démarrer et jeter,
sont la brique de base de cette approche. Combinés à un orchestrateur comme Kubernetes, ils
répondent nativement aux besoins d'infrastructures cloud-native.

### 2.3. Scaling vertical vs scaling horizontal

Quand le trafic d'une application augmente, deux stratégies existent :

- Le **scaling vertical** consiste à augmenter les ressources de la machine qui héberge
  l'application (plus de CPU, plus de RAM, plus de stockage). C'est simple, en particulier avec
  une infrastructure mutable, mais les ressources ajoutées sont difficiles à libérer une fois la
  machine en marche, et rien ne garantit qu'ajouter des ressources résolve le problème.
- Le **scaling horizontal** consiste à ajouter des machines supplémentaires qui hébergent la
  même application, avec une répartition du trafic entre elles. Une fois le pic de trafic passé,
  les machines en trop sont supprimées et leurs ressources rendues au pool commun.

**Troisième point clé** : le scaling horizontal, particulièrement adapté à une infrastructure
immuable, est l'approche privilégiée dès que l'application le permet — et les conteneurs, légers
et rapides à instancier, sont taillés pour ça.

### 2.4. Ce que ça change concrètement pour vous

Ces trois points clés expliquent pourquoi les conteneurs ne sont pas juste "une autre façon
d'installer une application" : ils alignent le déploiement logiciel sur les besoins d'itération
rapide (agile), d'automatisation (DevOps), de fiabilité (infrastructure immuable) et de montée
en charge (scaling horizontal) qui dominent l'industrie aujourd'hui. C'est pour ça que la stack
imposée pour votre projet (voir `projet/sujet.md`) repose sur Docker et Docker Compose dès la
séance 1.

## 3. Terminologie Docker

Quatre notions reviennent en permanence, et il faut les distinguer clairement :

| Terme | Définition |
|---|---|
| **Image** | Un template en lecture seule contenant tout ce qu'il faut pour faire tourner un conteneur (dépendances, fichiers, configuration). Une image est souvent construite à partir d'une autre image, avec des ajouts spécifiques. Elle est partageable et portable, comme un binaire. |
| **Conteneur** | Une instance exécutable d'une image. On peut le créer, le démarrer, l'arrêter, le déplacer ou le supprimer via l'API ou le CLI Docker. |
| **Registry** | Une collection de repositories d'images (un peu comme GitHub héberge des repositories de code). Dockerhub est le registry public le plus connu. |
| **Tag** | Une étiquette appliquée à une image dans un repository, pour distinguer ses versions (`latest`, `v1`, `v2`...). |
| **Volume** | Un mécanisme de stockage persistant qui permet à des données de survivre au-delà du cycle de vie d'un conteneur, et d'être partagées entre conteneurs ou avec l'hôte. |

## 4. Construire une image : le Dockerfile

Une image se construit à partir d'un `Dockerfile`, qui décrit étape par étape comment
l'assembler :

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Chaque instruction (`FROM`, `WORKDIR`, `COPY`, `RUN`, `CMD`...) ajoute une couche à l'image.

Attention à `EXPOSE` : contrairement à ce que son nom laisse croire, cette instruction **ne publie
aucun port** et ne change rien au fonctionnement du conteneur. C'est une documentation lisible par
les humains et par les outils : elle déclare « ce conteneur écoute sur le port 8000 ». C'est
l'option `-p` de `docker run` (section 5) qui publie réellement un port vers votre machine.

Pour construire l'image :

```bash
docker build -t image_name .
```

Par défaut, Docker cherche un fichier nommé `Dockerfile` dans le dossier de contexte (le dernier
argument passé à la commande — ici `.`, le dossier courant). Pour utiliser un Dockerfile à un
autre emplacement :

```bash
docker build -t image_name -f dockerfiles/autre_Dockerfile dossier_contexte/
```

## 5. Lancer et gérer des conteneurs

Lancer un conteneur :

```bash
docker run --name container_name image_name
```

Exposer un port (mapping port local → port du conteneur) :

```bash
docker run --name container_name -p local_port:container_port image_name
```

Lancer en arrière-plan (mode détaché) :

```bash
docker run -d --name container_name image_name
```

Gérer images et conteneurs :

```bash
docker images                    # ou docker image ls
docker ps                        # ou docker container ls
docker rm container_name         # supprimer un conteneur arrêté
docker rm -f container_name      # forcer la suppression d'un conteneur en cours d'exécution
docker rmi image_name             # supprimer une image
```

Consulter les logs :

```bash
docker logs container_name
docker logs -f container_name    # en continu (follow)
```

Ouvrir un shell à l'intérieur d'un conteneur en cours d'exécution :

```bash
docker exec -it container_name bash
```

(`-it` = interactif + pseudo-terminal ; on sort avec `CTRL-D` ou `exit`.)

## 6. Les volumes

Un conteneur est éphémère par nature : à sa suppression, tout ce qui a été écrit dans son
système de fichiers disparaît. Les volumes permettent de faire persister des données au-delà du
cycle de vie d'un conteneur.

Il existe trois types de volumes :

- **Volumes nommés** : gérés par Docker, identifiés par un nom, réutilisables par plusieurs conteneurs indépendamment de leur cycle de vie.
- **Volumes anonymes** : créés quand on monte un volume sans lui donner de nom ; Docker lui attribue un nom aléatoire. Utile pour des données temporaires, mais plus difficile à gérer.
- **Bind mounts** : montent directement un dossier ou fichier de l'hôte dans le conteneur. Très utilisé en développement (monter son code source dans le conteneur), mais moins portable qu'un volume nommé.

```bash
docker volume create my_volume
docker volume ls
docker volume inspect my_volume

# attacher un volume nommé
docker run -v my_volume:/path/in/container image_name

# attacher un bind mount
docker run -v /host/path:/path/in/container image_name

# supprimer un volume, ou tous les volumes inutilisés
docker volume rm my_volume
docker volume prune
```

## 7. Les réseaux Docker

Avant de parler de Docker Compose, il faut comprendre ce qui se passe au niveau réseau quand vous
lancez plusieurs conteneurs — c'est ce mécanisme que Compose automatisera ensuite.

### 7.1. Le réseau `bridge` par défaut

Docker installe trois réseaux dès le départ, que vous pouvez lister :

```bash
docker network ls
```

```text
NETWORK ID     NAME      DRIVER    SCOPE
7f0e1c2b3a4d   bridge    bridge    local
9a8b7c6d5e4f   host      host      local
1122334455aa   none      null      local
```

Un conteneur lancé avec `docker run` sans précision est automatiquement attaché au réseau
`bridge`. Deux conteneurs lancés ainsi sont donc **sur le même réseau**, et chacun y reçoit une
adresse IP. Vous pouvez la lire :

```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name
```

Une idée fausse très répandue mérite d'être corrigée tout de suite : **ces deux conteneurs ne sont
pas isolés l'un de l'autre**. Depuis l'un, vous joignez parfaitement l'autre par son adresse IP.

Ce qui ne fonctionne pas sur le réseau `bridge` par défaut, c'est la **résolution du nom** : y
demander l'adresse de `container_name` échoue avec un `Name or service not known`. Docker n'y
active pas son serveur DNS interne, pour des raisons de compatibilité historique.

Se rabattre sur l'adresse IP n'est pas une solution viable. Docker attribue à chaque conteneur la
plus petite adresse libre du réseau au moment où il démarre : elle dépend donc de l'ordre de
lancement, et rien ne garantit qu'un conteneur retrouve la même après avoir été supprimé et
recréé. Coder une IP en dur dans une configuration, c'est se préparer une panne au prochain
redémarrage.

### 7.2. Les réseaux user-defined et le DNS embarqué

La solution est de créer votre propre réseau — on parle de réseau *user-defined* :

```bash
docker network create my_network
```

Sur un réseau créé de cette façon, et **uniquement sur ce type de réseau**, Docker active un
serveur DNS embarqué : chaque conteneur y est joignable par son **nom**, quelle que soit son
adresse IP du moment.

Deux façons d'y attacher un conteneur :

```bash
# à la création du conteneur
docker run -d --name container_name --network my_network image_name

# ou après coup, sur un conteneur déjà lancé
docker network connect my_network container_name
```

La seconde forme *ajoute* un réseau sans retirer le précédent : un conteneur peut appartenir à
plusieurs réseaux à la fois. Vérifiez à tout moment qui est attaché à quoi :

```bash
docker network inspect my_network      # dont la liste des conteneurs attachés et leurs IP
docker network rm my_network           # supprimer un réseau (une fois les conteneurs détachés)
docker network prune                   # supprimer tous les réseaux inutilisés
```

Une fois deux conteneurs sur le même réseau user-defined, l'un joint l'autre par
`http://<nom_du_conteneur>:<port>/`. C'est ce nom qu'on passe à l'application, en général par une
variable d'environnement, avec l'option `-e` de `docker run` :

```bash
docker run -d --name front --network my_network -e API_URL=http://api:8000 front_image
```

### 7.3. Réseau et publication de port : deux choses différentes

C'est la confusion la plus fréquente, autant la lever maintenant :

| | À quoi ça sert | Qui en a besoin |
|---|---|---|
| `-p 8000:8000` | Publier un port du conteneur vers **votre machine** | Votre navigateur, `curl` depuis votre terminal |
| Même réseau + nom | Joindre un conteneur **depuis un autre conteneur** | Le frontend qui appelle le backend |

Un conteneur backend attaché au même réseau que le frontend est joignable par celui-ci **même sans
aucun `-p`**. La publication de port ne sert qu'à ouvrir une porte depuis l'extérieur de Docker.
De la même façon, `EXPOSE` dans le Dockerfile (section 4) ne joue aucun rôle ici : c'est de la
documentation.

Retenez la règle : `-p` pour vous, le réseau pour les conteneurs entre eux.

## 8. Docker Compose et le DNS interne

Docker Compose définit et lance plusieurs conteneurs à partir d'un seul fichier de
configuration YAML, `docker-compose.yml` — un raccourci par rapport à enchaîner des `docker run`
un par un, avec en plus la possibilité de définir comment construire les images.

```yaml
services:
  api:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - my_named_volume:/data/named
      - /data/anonymous
      - ./host_data:/data/bind
  redis:
    image: "redis:alpine"

volumes:
  my_named_volume:
```

Commandes principales :

```bash
docker compose up            # démarrer les services
docker compose up --build    # démarrer en forçant la reconstruction des images
docker compose up -d         # démarrer en arrière-plan
docker compose down          # arrêter et supprimer les conteneurs
docker compose ps            # lister les conteneurs du projet
docker compose exec service_name bash   # ouvrir un shell dans un service en cours d'exécution
```

Le point le plus important pour la suite du module : **Docker Compose fournit un DNS interne**.
Dans l'exemple ci-dessus, les services `api` et `redis` peuvent se joindre entre eux en utilisant
simplement leur **nom de service** comme nom d'hôte — pas besoin de connaître leur adresse IP.
L'URL prend la forme `http://<nom_du_service>:<port>/`.

Ce n'est pas de la magie, c'est exactement le mécanisme de la section 7 : au démarrage, Compose
**crée automatiquement un réseau user-defined** pour votre projet et y attache tous les services
déclarés. Le DNS embarqué de ce réseau fait le reste. La seule différence avec la manipulation
manuelle, c'est le nom qui résout : Compose enregistre le **nom de service** (la clé dans le YAML),
pas le nom du conteneur — lequel est de toute façon généré par Compose. Vous pouvez le vérifier
après un `docker compose up` :

```bash
docker network ls        # un réseau <nom_du_projet>_default est apparu
```

C'est ce mécanisme qui permettra à votre frontend de contacter votre backend, et à votre backend de
contacter votre base de données, uniquement en connaissant leur nom de service dans le
`docker-compose.yml`.

## 9. Aller plus loin

### 9.1. Images de base et Alpine

La première ligne d'un Dockerfile (`FROM ...`) désigne l'image de base. Elle peut préciser un
langage (`python`, `golang`, `java`...), une version (`python:3.12`, `python:3.11`...) et un
système d'exploitation (`slim`, `bullseye`, `alpine`...).

[Alpine Linux](https://alpinelinux.org/about/) est une distribution qui ne tourne quasiment que
sur des conteneurs, très populaire pour son poids plume (moins de 6 Mo), sa simplicité et sa
sécurité — elle sert de base à une grande partie des images utilisées en production.

### 9.2. Multi-stage builds

Chaque instruction d'un Dockerfile ajoute une couche à l'image. Un Dockerfile peut être composé
de plusieurs étapes (*stages*), pour se débarrasser des couches temporaires (outils de
compilation, dépendances de build) qui ne sont pas nécessaires à l'image finale.

```dockerfile
# première étape : build
FROM python:3.12 AS builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# deuxième étape : image finale, allégée
FROM python:3.12-slim
COPY --from=builder /root/.local /root/.local
COPY ./src .

CMD ["python", "./server.py"]
```

Voir la [documentation officielle](https://docs.docker.com/develop/develop-images/multistage-build/).

### 9.3. Registry d'images

En développement, il est normal de construire ses images localement pour ajuster le Dockerfile.
En production, la pratique courante est différente : une fois l'image optimisée et validée par
les tests d'intégration, on la pousse (`push`) dans un **registry d'images**, puis on lance les
conteneurs en production à partir de cette image déjà construite — ce qui évite de reconstruire
l'image en prod et les mauvaises surprises liées à un build raté.

[Dockerhub](https://hub.docker.com/) est le registry public le plus connu (gratuit au *pull*
pour la plupart des images). Il existe aussi des registries privés orientés entreprise
(Artifactory, Nexus, AWS ECR, Google Container Registry...) ou auto-hébergés.

### 9.4. Développer depuis un conteneur

Pour garantir que votre application tourne de façon identique chez tous vos collègues et en
production, il est possible — et parfois recommandé — de développer directement depuis un
conteneur, grâce au partage de volume (votre code local reste accessible dans le conteneur) :

```bash
docker run -it --name python_dev -v $PWD:/app python:3.12-alpine /bin/sh
```

L'avantage : vous ne polluez pas votre machine avec des dépendances, et si la configuration du
conteneur ne convient pas, il suffit de le supprimer et de recommencer. L'extension VS Code **Dev
Containers** (anciennement Remote - Containers) automatise cette approche en ouvrant une fenêtre
de l'IDE directement connectée à l'intérieur du conteneur.

## 10. Synthèse et lien avec la suite du module

Les conteneurs ne sont pas qu'un détail d'infrastructure : ils incarnent une philosophie de
déploiement — reproductible, portable, jetable — pensée pour l'agilité et le DevOps. Retenez
surtout trois idées : la portabilité (la même image tourne partout), l'isolation (chaque service
est une pièce indépendante) et le DNS interne des réseaux user-defined, dont Docker Compose se sert
pour que les services se contactent par leur nom plutôt que par une IP instable.

Ce socle sera mobilisé progressivement : dès la **séance 1** pour lancer votre API GearShare dans
un conteneur, en **séance 3** quand la base PostgreSQL rejoindra le `docker-compose.yml`, et en
**séance 4** quand vous passerez aux trois services (backend, frontend, base de données).
Avant ça, direction le [TP de cette séance 0](../tp/README.md) pour manipuler tout ça en
pratique.
