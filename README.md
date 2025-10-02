# Application de connexion - Architecture MVC

Cette application démontre une implémentation claire et rigoureuse du pattern MVC (Model-View-Controller) avec FastAPI.

## 🏗️ Architecture MVC

### Structure du projet

```
login-python/
├── config/                  # Configuration centralisée
│   ├── __init__.py
│   ├── app_config.py       # Configuration générale
│   └── database.py         # Configuration base de données
├── controllers/            # Contrôleurs (C)
│   ├── __init__.py
│   ├── auth_controller.py  # Gestion authentification
│   └── main_controller.py  # Contrôleur principal
├── models/                 # Modèles (M)
│   ├── __init__.py
│   └── user_model.py      # Modèle User avec CRUD
├── services/              # Services métier
│   ├── __init__.py
│   ├── auth_service.py    # Service d'authentification
│   ├── session_service.py # Service de session
│   └── validation_service.py # Service de validation
├── templates/             # Vues (V)
│   ├── base.html         # Template de base
│   ├── index.html        # Page d'accueil
│   ├── login.html        # Formulaire de connexion
│   └── register.html     # Formulaire d'inscription
├── static/
│   └── css/
│       └── style.css     # Styles CSS
├── sql/
│   └── db.sql           # Structure de la base
├── main.py              # Point d'entrée FastAPI
└── requirements.txt     # Dépendances
```

## 📁 Composants MVC

### **Models (Modèles)** 📊
- **`models/user_model.py`** : Encapsule la logique métier des utilisateurs
  - Opérations CRUD (Create, Read, Update, Delete)
  - Méthodes de recherche (par login, email, etc.)
  - Sauvegarde et mise à jour des données

### **Views (Vues)** 🎨
- **`templates/`** : Templates Jinja2 avec héritage
  - `base.html` : Template de base partagé
  - Templates spécialisés pour chaque page
  - Interface utilisateur propre et moderne

### **Controllers (Contrôleurs)** 🎯
- **`controllers/auth_controller.py`** : Gestion de l'authentification
  - Formulaires de connexion/inscription
  - Validation et traitement des données
  - Gestion des redirections
- **`controllers/main_controller.py`** : Pages principales
  - Page d'accueil adaptée selon l'état de connexion

### **Services** ⚙️
Couche intermédiaire pour la logique métier :
- **`services/auth_service.py`** : Hachage et vérification des mots de passe
- **`services/session_service.py`** : Gestion des sessions utilisateur
- **`services/validation_service.py`** : Validation des données

### **Configuration** 🔧
- **`config/database.py`** : Gestion de la base de données PostgreSQL
- **`config/app_config.py`** : Configuration centralisée de l'application

## 🚀 Installation et démarrage

### Prérequis
- Python 3.8+
- PostgreSQL
- Base de données "2025_M1" configurée

### Installation
```bash
# Installer les dépendances
pip install -r requirements.txt

# Configurer la base de données (voir config/database.py)
# Adapter les paramètres de connexion si nécessaire
```

### Démarrage
```bash
# Méthode 1 : Via uvicorn
uvicorn main:app --reload

# Méthode 2 : Via le script main.py
python main.py
```

L'application sera accessible sur : http://localhost:8000

## ✨ Avantages de cette architecture MVC

### 🎯 **Séparation claire des responsabilités**
- **Modèles** : Logique métier et données
- **Vues** : Interface utilisateur et présentation  
- **Contrôleurs** : Orchestration et logique de navigation

### 🔧 **Maintenabilité**
- Code organisé et structuré
- Composants réutilisables
- Facilité de modification et d'extension

### 🧪 **Testabilité**
- Chaque composant peut être testé indépendamment
- Injection de dépendances facilitée
- Mocks et stubs plus simples

### 📈 **Scalabilité**
- Ajout facile de nouvelles fonctionnalités
- Extension possible sans refactoring majeur
- Architecture prête pour la croissance

### 👥 **Collaboration**
- Structure claire pour le travail en équipe
- Responsabilités bien définies
- Code auto-documenté

## 🔒 Sécurité

- Hachage sécurisé des mots de passe (bcrypt)
- Protection XSS dans les sessions
- Validation rigoureuse des données
- Sessions sécurisées avec clé secrète

## 📋 Fonctionnalités

- ✅ Inscription utilisateur avec validation
- ✅ Connexion/déconnexion sécurisée  
- ✅ Gestion des sessions
- ✅ Interface responsive et moderne
- ✅ Messages d'erreur informatifs
- ✅ Protection contre les vulnérabilités communes

## 🛠️ Extension possible

Cette architecture facilite l'ajout de :
- Nouveaux modèles (Article, Comment, etc.)
- Nouveaux contrôleurs (Admin, API, etc.)  
- Nouveaux services (Email, Upload, etc.)
- Middlewares personnalisés
- Tests automatisés

---

Cette implémentation démontre comment structurer une application web moderne en suivant les principes MVC de manière claire et rigoureuse.