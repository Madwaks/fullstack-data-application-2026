# Outils requis — avant la séance 1

Ce document liste les outils que **chaque étudiant** doit avoir installés et configurés avant le
début du cours. Prévoir **30 à 45 minutes** pour l'ensemble de la procédure. En cas de blocage
(licence non reconnue, droits admin manquants sur le poste...), contacter l'enseignant avant la
séance 1 plutôt que le jour même.

## Récapitulatif

| Outil | Obligatoire | Coût |
|---|---|---|
| Compte GitHub + GitHub Education | Oui | Gratuit |
| Git | Oui | Gratuit |
| GitHub Copilot Education | Oui | Gratuit (via GitHub Education) |
| Un second LLM (Claude, ChatGPT, ou autre) | Oui (au moins un) | Gratuit ou payant selon l'outil |
| Docker Desktop | Oui | Gratuit (usage étudiant/individuel) |
| Un IDE (VS Code ou JetBrains) | Oui | Gratuit |

---

## 1. Compte GitHub + GitHub Education

Le compte GitHub est le point d'entrée : il sert à héberger le repo de projet, à activer
GitHub Copilot Education, et potentiellement à obtenir d'autres avantages étudiants (Student
Developer Pack).

**Procédure :**
1. Créer un compte sur [github.com](https://github.com/) si vous n'en avez pas déjà un — utiliser
   de préférence votre adresse e-mail étudiante (`@edu.esiee.fr` ou équivalent), cela simplifie la
   vérification.
2. Faire une demande d'accès sur [GitHub Education](https://education.github.com/) via le bouton
   "Get student benefits".
3. Vérifier votre statut étudiant (carte étudiante, justificatif de scolarisation...). La validation peut prendre de quelques minutes à quelques jours.
4. Une fois validé, le [Student Developer Pack](https://education.github.com/pack) est accessible
   depuis les paramètres de votre compte GitHub.

## 2. Git

Git est l'outil de contrôle de version utilisé pour cloner votre repo de projet, faire vos
commits, et suivre le flow de PR/code review enseigné à partir de la séance 4. Il est indispensable
même si vous passez principalement par l'interface de votre IDE.

**Procédure :**
1. Installer Git :
   - **Windows** : télécharger [Git for Windows](https://git-scm.com/download/win) et suivre
     l'assistant (les options par défaut conviennent).
   - **macOS** : Git est généralement préinstallé avec les outils en ligne de commande Xcode ;
     sinon l'installer via [Homebrew](https://brew.sh/) (`brew install git`) ou le
     [site officiel](https://git-scm.com/download/mac).
   - **Linux** : installer via le gestionnaire de paquets de votre distribution
     (ex. `sudo apt install git` sur Debian/Ubuntu).
2. Configurer votre identité (nécessaire pour que vos commits soient correctement attribués) :
   ```bash
   git config --global user.name "Prénom Nom"
   git config --global user.email "votre-email@edu.esiee.fr"
   ```
3. Vérifier l'installation en terminal :
   ```bash
   git --version
   ```

## 3. GitHub Copilot Education

Copilot Education est inclus dans le Student Developer Pack et donne accès à Copilot Chat,
aux chat modes et à l'intégration IDE utilisés en cours.

**Procédure :**
1. Une fois le Student Developer Pack validé (étape précédente), aller sur
   [github.com/settings/copilot](https://github.com/settings/copilot).
2. Activer l'accès Copilot individuel si ce n'est pas déjà proposé automatiquement suite à la
   validation du statut étudiant.
3. Vérifier l'activation via la documentation officielle :
   [docs.github.com/copilot](https://docs.github.com/en/copilot).
4. L'extension Copilot sera installée au niveau de l'IDE (voir section 4).

## 4. Un second LLM (Claude, ChatGPT, ou équivalent)

Le cours attend que vous croisiez les réponses d'au moins **deux agents/LLM différents**
(comparaison de sorties, choix de l'outil le plus adapté à une tâche). Copilot Education seul
ne suffit pas : il faut un accès à Claude, ChatGPT, ou un autre LLM gratuit.

**Utiliser des LLMs gratuits ou avec des limites de tokens vous force à optimiser votre consommation de tokens** — 
formuler des requêtes concises et efficaces pour obtenir le meilleur résultat avec un budget restreint. 
Cette discipline est essentielle en contexte professionnel, où chaque token a un coût réel.

**Options (au moins une, gratuite suffisant) :**

- **Claude** (Anthropic) — [claude.ai](https://claude.ai/) : créer un compte avec une adresse e-mail,
  l'offre gratuite (Claude Free) est suffisante pour un usage ponctuel en TD. Claude Code (CLI) est
  disponible séparément si vous voulez un agent en ligne de commande :
  [docs.claude.com/claude-code](https://docs.claude.com/en/docs/claude-code/overview).
- **ChatGPT** (OpenAI) — [chatgpt.com](https://chatgpt.com/) : créer un compte, l'offre gratuite
  (ChatGPT Free) suffit.
- **Autre LLM gratuit** (Gemini, Mistral Le Chat, etc.) : accepté, à condition de pouvoir l'utiliser
  en chat interactif pendant les TD.

**Procédure générique :**
1. Créer un compte sur la plateforme choisie avec une adresse e-mail valide.
2. Vérifier l'e-mail si demandé.
3. Tester l'accès en posant une question simple avant la séance 1 (pas de configuration
   supplémentaire nécessaire pour un usage web basique).

## 5. Docker Desktop

La stack du projet (backend, frontend, base de données PostgreSQL) est conteneurisée avec
Docker Compose — Docker Desktop est indispensable dès la séance 1.

**Procédure :**
1. Télécharger Docker Desktop depuis [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
   (versions Windows, macOS Intel/Apple Silicon, Linux disponibles).
2. Installer en suivant l'assistant (redémarrage du poste probable sur Windows/macOS).
3. Sur Windows, s'assurer que **WSL2** est activé si l'installeur le demande — suivre le lien
   fourni par l'installeur ([docs Microsoft WSL](https://learn.microsoft.com/fr-fr/windows/wsl/install)).
4. Lancer Docker Desktop et attendre que l'icône indique "Running"/"En cours d'exécution".
5. Vérifier l'installation en terminal :
   ```bash
   docker --version
   docker compose version
   docker run hello-world
   ```
   La dernière commande doit afficher un message de confirmation Docker.

## 6. Un IDE (VS Code ou JetBrains)

Le choix de l'IDE n'est pas imposé par le cours — **VS Code** et les IDE **JetBrains**
(PyCharm notamment) sont tous deux couverts par les extensions Copilot Education. Choisir celui
avec lequel vous êtes le plus à l'aise, ou VS Code par défaut si aucune préférence.

### Option A — VS Code

1. Télécharger depuis [code.visualstudio.com](https://code.visualstudio.com/).
2. Installer en suivant l'assistant.
3. Dans l'onglet Extensions, installer :
   - **French Language Pack** (interface en français — recherche "French Language Pack" dans le marketplace).
   - **Python** (extension officielle Microsoft).
   - **GitHub Copilot** et **GitHub Copilot Chat**, si vous ne les avez pas déjà (recherche "Copilot" dans le marketplace).
4. Se connecter avec votre compte GitHub via l'icône Copilot dans la barre d'état ou la barre
   latérale — l'IDE doit reconnaître automatiquement votre licence Copilot Education.

### Option B — JetBrains (PyCharm)

1. Installer le [JetBrains Toolbox](https://www.jetbrains.com/toolbox-app/), qui gère les
   installations et mises à jour des IDE JetBrains.
2. Via Toolbox, installer **PyCharm** (édition Community suffisante, Professional accessible
   gratuitement aux étudiants via le Student Developer Pack).
3. Installer le plugin **GitHub Copilot** depuis `Settings/Preferences → Plugins → Marketplace`.
4. Se connecter avec votre compte GitHub dans les paramètres du plugin Copilot.

## 7. (Optionnel) Réduire sa consommation de tokens — rtk

Vu la discipline d'optimisation des tokens attendue dans ce cours (section 4), [rtk](https://github.com/rtk-ai/rtk)
est un proxy CLI qui réécrit vos commandes courantes (git, recherche de fichiers...) en équivalents
moins coûteux en tokens. Ce n'est pas un outil imposé, mais il fonctionne avec la plupart des agents
utilisés en cours — GitHub Copilot CLI, Claude Code, Cursor, Gemini CLI, et une dizaine d'autres.

**Installation :**

- **macOS/Linux** (Homebrew) :
  ```bash
  brew install rtk
  ```
  Ou via script d'installation :
  ```bash
  curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
  ```
  (ajoute `~/.local/bin` à votre PATH si besoin).
- **Windows** : téléchargez `rtk-x86_64-pc-windows-msvc.zip` depuis les
  [releases GitHub](https://github.com/rtk-ai/rtk/releases), extrayez `rtk.exe` et placez-le dans
  votre PATH (ex. `C:\Users\<vous>\.local\bin`). Lancez l'installation depuis un terminal
  (Command Prompt, PowerShell ou Windows Terminal), jamais par double-clic. Sous WSL, suivez la
  procédure macOS/Linux.

**Activer l'intégration avec votre agent :**

```bash
rtk init -g              # hook générique (Claude Code et autres agents compatibles)
rtk init -g --copilot    # intégration spécifique GitHub Copilot
```

**Vérifier l'installation :**

```bash
rtk --version
rtk gain
```

---

## Checklist finale

- [ ] Compte GitHub créé, Student Developer Pack validé.
- [ ] Git installé et configuré (`git --version` fonctionne, identité renseignée).
- [ ] GitHub Copilot Education actif (visible dans `github.com/settings/copilot`).
- [ ] Au moins un second LLM accessible (Claude, ChatGPT, ou autre).
- [ ] Docker Desktop installé, `docker run hello-world` fonctionne.
- [ ] IDE installé avec extension/plugin Copilot connecté à votre compte GitHub.
