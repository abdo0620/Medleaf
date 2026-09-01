# **MedLeaf - Assistant Conversationnel IA pour la Compréhension des Notices Médicales**

**MedLeaf** est une application Streamlit pour explorer les notices de médicaments avec un assistant basé sur la Retrieval-Augmented Generation (RAG). Les utilisateurs peuvent poser des questions à **Mia** sur les informations de médicaments indexées, inspecter les fragments de texte récupérés, et télécharger des fichiers PDF ou TXT pour enrichir la base de connaissances locale.

L'assistant fonctionne entièrement en local avec **Ollama** et le modèle `qwen2.5:3b-instruct`. Les réponses sont générées à partir du texte récupéré dans une base de données vectorielle **ChromaDB** persistante, sans dépendre d'API externes.

![MedLeaf interface](Rag/app/assets/images/Gemini_Generated_Image_pjw0i6pjw0i6pjw0.png)

> **Avertissement important** : MedLeaf est un outil éducatif de recherche documentaire, non un substitut à un médecin, pharmacien ou notice officielle de médicament. Vérifiez toujours les décisions médicales avec un professionnel qualifié.

---

## **I. Architecture générale**

Le projet repose sur une architecture modulaire conçue pour le traitement, l'indexation et l'interrogation de documents via un pipeline RAG. Il est structuré autour de trois composants fonctionnels distincts :

- **Chunking** : module chargé de la préparation des documents, incluant le nettoyage, la normalisation et le découpage sémantique en segments exploitables par les modèles de langage. Utilise `tiktoken` pour un comptage précis des tokens.

- **Embedding & Retrieval** : composant responsable de la vectorisation des segments et de leur indexation dans la base vectorielle **ChromaDB**, ainsi que de la recherche sémantique pour récupérer les trois fragments les plus pertinents par rapport à la requête utilisateur.

- **Application (App)** : interface utilisateur développée avec **Streamlit**, permettant l'interaction en chat avec Mia, le téléchargement de documents (PDF/TXT), l'inspection des chunks récupérés, et la consultation de l'historique des échanges.

L'ensemble de l'infrastructure est entièrement conteneurisé via **Docker Compose**, garantissant la reproductibilité des environnements, l'isolation des services et la facilité de déploiement.

### **Technologies utilisées**
- **Python 3.12** — langage principal
- **Streamlit 1.58** — interface utilisateur
- **ChromaDB 1.5.9** — stockage vectoriel persistant
- **Ollama** — exécution locale des modèles LLM (`qwen2.5:3b-instruct`)
- **PyMuPDF** — extraction de texte depuis PDF
- **tiktoken** — comptage de tokens pendant le chunking
- **Docker & Docker Compose** — conteneurisation et orchestration

---

## **II. Lancer le projet en 1 commande**

### **⚡ Démarrage rapide avec Docker**

Ce projet est **entièrement dockerisé**. Une seule commande pour tout démarrer :

```bash
docker compose up --build
```

C'est tout !

#### **Prérequis minimum**
- Docker Desktop (Windows/macOS) ou Docker Engine avec Compose (Linux)
- Au moins 8 GB de RAM disponible
- Connexion Internet pour le premier téléchargement des modèles

#### **Durée d'exécution**

| Étape | Durée |
|-------|-------|
| **Premier lancement** (téléchargement des modèles ~3 GB) | 10-15 minutes |
| **Lancements suivants** (conteneurs déjà prêts) | < 1 minute |

#### **Accéder à l'application**

Une fois la commande terminée, ouvrez votre navigateur :

```
http://localhost:8501
```

#### **Arrêter l'application**

Appuyez sur `Ctrl+C` pour arrêter gracieusement tous les conteneurs.

Pour nettoyer complètement (supprimer les conteneurs mais garder les données) :

```bash
docker compose down
```

**Important** : Les données (ChromaDB et documents) sont persistées via des volumes Docker et seront disponibles lors du prochain démarrage.

---

### **Logs et diagnostic**

Pour afficher les logs en temps réel :

```bash
docker compose logs -f
```

Pour afficher les logs d'un service spécifique (ex. Ollama) :

```bash
docker compose logs -f ollama-server
```

---

## **Interface & Galerie**

### **Chat avec Mia**
![Main app interface](screenshots/Screenshot%202026-07-22%20121857.png)

### **Téléchargement de documents**
![Upload documents](screenshots/Screenshot%202026-07-22%20122503.png)

---

## **III. Fonctionnement du système**

1. **Ingestion** : Les données FDA et les documents uploadés sont traités par le module **Chunking**
2. **Indexation** : Les chunks sont vectorisés et indexés dans **ChromaDB**
3. **Requête utilisateur** : L'utilisateur pose une question via l'interface Streamlit
4. **Récupération** : Le système récupère les 3 chunks les plus pertinents depuis ChromaDB
5. **Génération** : **Ollama** génère une réponse basée sur ces chunks et l'historique de conversation
6. **Affichage** : La réponse et les sources sont affichées à l'utilisateur

---

## **IV. Base de données FDA**

Les données FDA sont **déjà incluses** dans le conteneur Docker et sont indexées automatiquement au premier démarrage.

Les données sont stockées dans :
- **Source** : `Rag/database/files/drug_json_files/` et `drug_text_files/`
- **Index** : `Rag/database/Vectordb/` (ChromaDB persistante)

### **Réinitialiser la base de données**

Si vous voulez effacer tous les documents indexés (FDA + uploads) :

```bash
docker compose exec app python Rag/database/files/reset.py
```

Puis relancez Docker Compose pour réindexer les données FDA.

---

## **V. Structure du projet**

```
Rag/
├── agent/              # Mia + intégration Ollama
├── app/                # Interface Streamlit (pages: chat, upload, about)
├── Chunking/           # Découpage sémantique des textes
├── database/
│   ├── db.py           # Client ChromaDB
│   ├── inject_fda_db.py # Indexation FDA
│   └── files/          # Données FDA + documents uploadés
└── retreival/          # Recherche vectorielle

eval/                   # Scripts d'évaluation
docker-compose.yml      # Configuration Docker (le cœur du projet)
Dockerfile              # Image Docker
requirements.txt        # Dépendances Python
```

---

## **VI. Configuration rapide**

- **Modèle LLM** : `qwen2.5:3b-instruct` (configurable dans `Rag/agent/agent.py`)
- **Endpoint Ollama** : `http://ollama-server:11434` (local pour Docker)
- **Collection ChromaDB** : `mrooc`
- **UI** : Streamlit sur `http://localhost:8501`

---

## **VII. Troubleshooting**

| Problème | Solution |
|----------|----------|
| Docker ne démarre pas | Vérifiez les logs : `docker compose logs -f` |
| Port 8501 déjà utilisé | `docker compose down` puis relancez |
| Ollama slow/timeout | Attendre le téléchargement du modèle (~10-15 min la première fois) |
| Connexion ChromaDB refused | Vérifiez que tous les conteneurs tournent : `docker ps` |

---

## **VIII. Lancer localement (Sans Docker - Non recommandé)**

Si vous insistez absolument pour ignorer Docker :

```bash
python -m venv .env
.env/Scripts/activate       # Windows
source .env/bin/activate   # macOS/Linux
pip install -r requirements.txt

# Dans un terminal séparé
ollama serve
ollama pull qwen2.5:3b-instruct

# Lancer l'app
streamlit run Rag/app/main.py
```

**Mais sérieusement, utilisez Docker. C'est plus simple.**

---

## **À propos**

**MedLeaf** est un projet éducatif démontrant les systèmes RAG modernes avec LLMs open-source et stockage vectoriel local. Entièrement dockerisé pour une simplicité maximale.
