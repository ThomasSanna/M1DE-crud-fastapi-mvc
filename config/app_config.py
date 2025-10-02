"""
Configuration générale de l'application
"""

class AppConfig:
    """Configuration centralisée de l'application"""
    
    # Clé secrète pour les sessions
    SECRET_KEY = "eziuzhfeuihHIUZEFHIEUHhiauhu"
    
    # Configuration des templates
    TEMPLATES_DIR = "templates"
    
    # Configuration des fichiers statiques
    STATIC_DIR = "static"
    STATIC_URL = "/static"
    
    # Configuration de sécurité
    PASSWORD_MIN_LENGTH = 6
    USERNAME_MIN_LENGTH = 3


# Instance globale de configuration
app_config = AppConfig()