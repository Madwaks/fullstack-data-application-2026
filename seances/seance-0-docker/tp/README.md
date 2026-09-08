# TP — Séance 0 : Docker

## Objectifs du TP

Ce TP vous fait manipuler en pratique tout le vocabulaire et les commandes vus dans le
[cours de cette séance 0](../cours/README.md). À la fin du TP, vous devez savoir :

- construire une image à partir d'un `Dockerfile` et lancer un conteneur ;
- exposer un port et vérifier qu'un service répond ;
- diagnostiquer pourquoi un conteneur n'arrive pas à en joindre un autre par son nom ;
- créer un réseau Docker, y attacher des conteneurs et l'inspecter ;
- distinguer publier un port (`-p`) et faire communiquer deux conteneurs entre eux ;
- écrire un `docker-compose.yml` qui orchestre plusieurs services et utilise le DNS interne de Compose.

Aucun rendu formel n'est attendu pour cette séance 0 : elle sert de mise à niveau avant la séance
1. Assurez-vous simplement d'être à l'aise avec les manipulations ci-dessous avant le début du
module.

## Prérequis

- Docker Desktop installé et lancé (`docker run hello-world` doit fonctionner — voir
  [OUTILS.md](../../../OUTILS.md), section 5, si ce n'est pas déjà fait).
- Un terminal et un éditeur de code.

Le support de ce TP est le dossier [`demo-app/`](./demo-app), qui contient deux mini-applications
FastAPI indépendantes :

```text
demo-app/
├── api/     # renvoie {"message": "Hello from api!"}
└── front/   # affiche une page HTML qui va chercher ce message auprès de l'api
```

## Partie 1 — Construire et lancer un premier conteneur (25 min)

1. Dans `demo-app/api/`, regardez le `Dockerfile` : de quelle image de base part-il ? Que fait
   chaque instruction ?
2. Construisez l'image :

   ```bash
   cd demo-app/api
   docker build -t tp0-api .
   ```

3. Lancez un conteneur en exposant le port 8000, en arrière-plan :

   ```bash
   docker run -d --name tp0-api -p 8000:8000 tp0-api
   ```

4. Vérifiez que l'API répond, avec votre navigateur, puis avec `curl` :

   ```bash
   curl http://localhost:8000
   ```

5. Consultez les logs du conteneur, puis listez les conteneurs et les images :

   ```bash
   docker logs tp0-api
   docker ps
   docker images
   ```

6. Entraînez-vous au cycle de vie du conteneur — arrêt, redémarrage — **sans le supprimer** :

   ```bash
   docker stop tp0-api
   docker ps            # il n'apparaît plus
   docker ps -a         # il est là, à l'état "Exited"
   docker start tp0-api
   curl http://localhost:8000
   ```

   Gardez `tp0-api` en vie jusqu'à la fin de la partie 3 : tout le reste du TP s'appuie dessus.

Questions à noter :

- Que se passe-t-il si vous lancez un second `docker run --name tp0-api ...` alors que le premier
  conteneur existe encore ?
- À quoi sert exactement `-p 8000:8000` ? Que se passe-t-il si vous changez le port côté hôte
  (`-p 9000:8000`) ?
- Quelle est la différence entre `docker stop` et `docker rm -f` ?

## Partie 2 — Deux conteneurs qui n'arrivent pas à se parler (20 min)

1. Construisez et lancez le front, en exposant le port 8080 :

   ```bash
   cd ../front
   docker build -t tp0-front .
   docker run -d --name tp0-front -p 8080:8080 tp0-front
   ```

2. Ouvrez `http://localhost:8080` dans votre navigateur. Vous voyez la page du front, mais elle
   affiche **"impossible de contacter l'api"** — alors que votre conteneur `tp0-api` tourne
   toujours, et que `http://localhost:8000` répond parfaitement depuis votre navigateur.

Regardez le code de `demo-app/front/app/main.py` : la variable `API_URL` vaut par défaut
`http://localhost:8000`. Le piège est là. `localhost` ne désigne pas une machine en particulier :
il désigne **"celui qui pose la question"**. Depuis votre navigateur, c'est votre machine, où le
port 8000 est bien publié. Depuis l'intérieur du conteneur front, c'est **le conteneur front
lui-même** — où rien n'écoute sur le port 8000.

Le front ne cherche donc pas l'api au mauvais endroit du réseau : il ne sort même pas de son
propre conteneur.

Gardez les deux conteneurs en vie, la partie 3 part de cet état.

## Partie 3 — Comprendre et manipuler les réseaux Docker (35 min)

L'objectif de cette partie n'est pas seulement de faire marcher le front : c'est de comprendre
**pourquoi** la solution est un réseau Docker, en observant d'abord ce qui échoue.

### 3.1. Les conteneurs sont-ils vraiment isolés ? (10 min)

Vous entendrez souvent dire que deux conteneurs sont isolés et ne peuvent pas communiquer. Vérifions.

1. Regardez les réseaux existants et celui de vos deux conteneurs :

   ```bash
   docker network ls
   docker inspect -f '{{.Name}} {{range $k,$v := .NetworkSettings.Networks}}{{$k}}={{$v.IPAddress}}{{end}}' tp0-api tp0-front
   ```

   Notez ce que vous voyez : vos deux conteneurs sont sur le **même** réseau, `bridge`, celui que
   Docker utilise par défaut. Relevez l'adresse IP de `tp0-api`, vous en aurez besoin.

2. Depuis le front, essayez de joindre l'api **par son nom**. L'image ne contient pas `curl`, on
   utilise donc `httpx`, déjà installé dans le front :

   ```bash
   docker exec -it tp0-front bash
   python -c "import httpx; print(httpx.get('http://tp0-api:8000').json())"
   ```

   Échec. Lisez le message : il parle de résolution de nom, pas de connexion refusée ni de timeout.

3. Toujours depuis ce shell, réessayez **par l'adresse IP** relevée à l'étape 1 (remplacez
   `172.17.0.X`) :

   ```bash
   python -c "import httpx; print(httpx.get('http://172.17.0.X:8000').json())"
   exit
   ```

   Cette fois, vous obtenez `{'message': 'Hello from api!'}`.

**Première conclusion, contre-intuitive : les deux conteneurs ne sont pas isolés du tout.** Le
paquet passe très bien. Ce qui manque sur le réseau `bridge` par défaut, c'est uniquement le
**DNS** : Docker n'y traduit pas `tp0-api` en adresse IP.

### 3.2. Pourquoi l'adresse IP n'est pas une solution (5 min)

On pourrait s'arrêter là et écrire l'IP en dur. Voyons ce que ça vaut.

1. Supprimez l'api, lancez un conteneur quelconque à sa place, puis recréez l'api :

   ```bash
   docker rm -f tp0-api
   docker run -d --name squatteur python:3.12-slim sleep 300
   docker run -d --name tp0-api -p 8000:8000 tp0-api
   docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' tp0-api
   ```

2. L'adresse de `tp0-api` a changé : Docker attribue la plus petite adresse libre au moment du
   démarrage, et `squatteur` a pris la place. L'IP que vous aviez notée pointe maintenant vers un
   autre conteneur.

   ```bash
   docker rm -f squatteur
   ```

**Deuxième conclusion : une adresse IP de conteneur n'est pas une donnée stable.** Elle dépend de
l'ordre de démarrage. Toute configuration qui la code en dur casse au prochain redémarrage. Il
nous faut un nom.

### 3.3. Un réseau user-defined pour obtenir le DNS (15 min)

Le DNS embarqué de Docker n'est actif que sur les réseaux que **vous** créez — pas sur le `bridge`
par défaut.

1. Créez un réseau et attachez-y l'api déjà lancée :

   ```bash
   docker network create tp0-net
   docker network connect tp0-net tp0-api
   ```

2. Inspectez le réseau pour voir qui y est attaché :

   ```bash
   docker network inspect tp0-net
   ```

   Dans la section `Containers`, vous trouvez `tp0-api` et son adresse **sur ce réseau** — qui
   n'est pas celle qu'il a sur `bridge`. Un conteneur peut appartenir à plusieurs réseaux et y
   avoir une adresse différente ; `docker network connect` ajoute un réseau, il ne remplace pas
   l'ancien.

3. Recréez le front sur ce réseau, en lui donnant la bonne URL via une variable d'environnement
   (`-e`) :

   ```bash
   docker rm -f tp0-front
   docker run -d --name tp0-front -p 8080:8080 --network tp0-net -e API_URL=http://tp0-api:8000 tp0-front
   ```

   Ici le front est attaché dès sa création avec `--network` : c'est la forme à préférer quand
   vous maîtrisez le lancement du conteneur. `docker network connect` sert quand le conteneur
   tourne déjà, comme pour l'api à l'étape 1.

4. Rafraîchissez `http://localhost:8080` : vous voyez **"Hello from api!"**.

   > Laissez deux ou trois secondes à l'api pour démarrer avant de rafraîchir. Si vous êtes trop
   > rapide, la page affiche encore l'ancien message d'erreur — ce n'est pas un problème de
   > réseau, juste uvicorn qui n'a pas fini de se lancer. Rafraîchissez à nouveau.

5. Refaites le test par nom qui échouait en 3.1 :

   ```bash
   docker exec -it tp0-front bash
   python -c "import httpx; print(httpx.get('http://tp0-api:8000').json())"
   exit
   ```

   Le nom résout, cette fois. C'est la seule chose qui a changé — et c'est tout l'intérêt d'un
   réseau user-defined.

### 3.4. Le test qui lève la confusion la plus fréquente (5 min)

Beaucoup d'étudiants pensent qu'il faut publier un port (`-p`) pour que deux conteneurs
communiquent. Démontrez-vous le contraire.

1. Recréez l'api sur le réseau, **sans aucun `-p`** :

   ```bash
   docker rm -f tp0-api
   docker run -d --name tp0-api --network tp0-net tp0-api
   ```

2. Attendez deux ou trois secondes que l'api démarre, puis constatez les deux effets :
   - `http://localhost:8080` (le front) affiche toujours **"Hello from api!"** ;
   - `curl http://localhost:8000` depuis votre terminal échoue désormais.

**Troisième conclusion :** `-p` n'a rien à voir avec la communication entre conteneurs. Il ouvre
une porte depuis **votre machine** vers un conteneur. Entre eux, les conteneurs se joignent par le
réseau, publication de port ou pas.

3. Nettoyez :

   ```bash
   docker rm -f tp0-api tp0-front
   docker network rm tp0-net
   ```

### Ce que vous devez pouvoir expliquer avant de passer à la suite

- Pourquoi `http://tp0-api:8000` échoue sur le réseau par défaut alors que l'IP fonctionne.
- Pourquoi on ne configure jamais une application avec l'IP d'un conteneur.
- Ce qu'un réseau user-defined apporte exactement (un seul mot : le DNS).
- La différence entre `-p 8000:8000` et attacher deux conteneurs au même réseau.

## Partie 4 — Orchestration avec Docker Compose (40 min)

Refaire manuellement un réseau, deux `docker run` et une variable d'environnement à chaque
lancement n'est pas tenable dès que le nombre de services augmente. C'est exactement ce que
Docker Compose automatise — et il n'y a aucune magie nouvelle : Compose crée pour vous un réseau
user-defined comme celui de la partie 3, et y attache tous les services. Vous le vérifierez à
l'étape 3.

1. À la racine de `demo-app/`, créez un fichier `docker-compose.yml` qui :
   - construit et lance le service `api` à partir de `./api`, en exposant le port 8000 ;
   - construit et lance le service `front` à partir de `./front`, en exposant le port 8080, avec
     la variable d'environnement `API_URL` pointant vers le service `api` (rappel : dans Compose,
     un service joint un autre par son **nom de service**, pas par un nom de conteneur ni une IP).

   Aidez-vous de l'exemple de syntaxe donné dans le [cours, section 8](../cours/README.md#8-docker-compose-et-le-dns-interne).

2. Lancez l'ensemble :

   ```bash
   docker compose up --build
   ```

3. Vérifiez que `http://localhost:8080` affiche à nouveau **"Hello from api!"** — sans avoir créé
   de réseau à la main. Depuis un autre terminal, allez voir ce que Compose a fabriqué :

   ```bash
   docker network ls                          # un réseau demo-app_default est apparu
   docker network inspect demo-app_default    # vos deux services y sont attachés
   ```

   C'est le même mécanisme qu'à la partie 3, créé automatiquement à partir du YAML.

4. Modifiez le texte du template `demo-app/front/app/templates/index.html`, relancez
   `docker compose up --build` et vérifiez que le changement apparaît.

5. Ouvrez un shell dans un des deux services via Compose (remarquez la différence avec
   `docker exec` de la partie 3) :

   ```bash
   docker compose exec front bash
   ```

6. Arrêtez et nettoyez :

   ```bash
   docker compose down
   ```

Questions à noter :

- En partie 3, le nom qui résolvait était `tp0-api`, le **nom du conteneur**. Dans votre
  `docker-compose.yml`, c'est `api`, le **nom du service**. Pourquoi ce changement ? (Regardez le
  nom réel des conteneurs avec `docker compose ps`.)
- Que fait `docker compose down` de plus que `docker rm -f` sur chaque conteneur un par un ?
  (Indice : refaites un `docker network ls` après.)

## Partie 5 — Pour aller plus loin (bonus, 20 min)

Ces manipulations ne sont pas obligatoires mais vous serviront dès la séance 1.

1. **Volumes** : ajoutez un volume nommé à votre service `api` dans `docker-compose.yml`
   (`volumes: - mon_volume:/data`, à déclarer aussi au niveau racine du fichier). Relancez,
   inspectez-le avec `docker volume inspect`, puis supprimez-le avec `docker volume rm`.
2. **Multi-stage build** : réécrivez le `Dockerfile` de `demo-app/api` en deux étapes (`builder`
   puis image finale allégée), sur le modèle donné dans le
   [cours, section 9.2](../cours/README.md#92-multi-stage-builds). Vérifiez que l'image obtenue
   fonctionne toujours (`docker build`, puis `docker run`) et comparez sa taille avec
   `docker images` par rapport à la version d'origine.
3. **Registry** : si vous avez un compte Dockerhub, taguez votre image
   (`docker tag tp0-api votre_pseudo/tp0-api:v1`) et poussez-la (`docker push`). Supprimez-la
   localement (`docker rmi`), puis re-téléchargez-la (`docker pull`) pour vérifier qu'elle
   fonctionne toujours.

## Ce que vous devez retenir avant la séance 1

- La différence entre une image et un conteneur.
- Que deux conteneurs sur le réseau par défaut se joignent par IP mais **pas par nom**, et qu'un
  réseau user-defined ajoute exactement une chose : le DNS.
- Qu'une IP de conteneur n'est jamais stable, donc qu'on configure toujours par un nom.
- Que `-p` publie un port vers votre machine et ne joue aucun rôle entre conteneurs.
- Comment Docker Compose remplace une série de `docker run`/`docker network` manuels, et comment
  ses services se contactent par leur nom de service.

Vous mobiliserez ces mécanismes progressivement : dès la **séance 1** pour lancer votre API
GearShare dans un conteneur, en **séance 3** quand la base PostgreSQL rejoindra le
`docker-compose.yml`, et en **séance 4** quand vous passerez aux trois services (backend, frontend,
base de données).
