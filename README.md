# Application de gestion de produits avec FastAPI

Une application web développée avec FastAPI suivant le pattern MVC (Modèle-Vue-Contrôleur), permettant la gestion d'utilisateurs et de produits avec authentification.

## Fonctionnalités

- **Authentification utilisateur** : inscription, connexion, déconnexion
- **Gestion des produits** : création, lecture, modification, suppression (CRUD)
- **Interface web** : templates HTML avec CSS
- **Base de données** : MySQL/MariaDB
- **Sécurité** : hachage des mots de passe avec bcrypt, gestion des sessions

## Architecture

Le projet suit le pattern MVC :
- **Models** : gestion des données (utilisateurs, produits)
- **Views** : templates HTML avec Jinja2
- **Controllers** : logique métier et traitement des requêtes
- **Services** : services d'authentification, validation et sessions

## Prérequis

- Python 3.8+
- MySQL/MariaDB
- pip

## Installation

### 1. Cloner le projet

```bash
git clone <url-du-repo>
cd login-python
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configuration de la base de données

1. Créer une base de données MySQL nommée `2025_M1`
2. Importer le fichier SQL :

```bash
mysql -u root -p 2025_M1 < sql/2025_m1.sql
```

### 4. Configuration

Vérifier les paramètres de base de données dans `config/database.py` :
- Host : localhost
- User : root
- Password : (vide par défaut)
- Database : 2025_M1

## Lancement

### Méthode 1 : Uvicorn (recommandée pour le développement)

```bash
uvicorn main:app --reload
```

### Méthode 2 : Python direct

```bash
python main.py
```

L'application sera accessible à l'adresse : http://localhost:8000

## Structure du projet

```
├── main.py                 # Point d'entrée de l'application
├── config/                 # Configuration (app, database)
├── controllers/            # Contrôleurs MVC
├── models/                 # Modèles de données
├── services/               # Services métier
├── templates/              # Templates HTML
├── static/                 # Fichiers CSS/JS
├── sql/                    # Scripts de base de données
└── tests/                  # Tests unitaires
```

## Routes principales

- `/` - Page d'accueil
- `/login` - Connexion
- `/register` - Inscription
- `/produits` - Liste des produits
- `/produits/add` - Ajouter un produit
- `/produits/{id}` - Voir un produit
- `/produits/{id}/edit` - Modifier un produit

## Développement

Pour le développement, utilisez :

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Le mode `--reload` permet le rechargement automatique lors des modifications du code.

## Base de données

La base de données contient deux tables principales :
- `user` : gestion des utilisateurs (login, mot de passe haché, email)
- `produit` : gestion des produits (type, désignation, prix, stock)

## Sécurité

- Mots de passe hachés avec bcrypt
- Sessions sécurisées avec clé secrète
- Protection CSRF
- Validation des données d'entrée