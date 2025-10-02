"""
Configuration de la base de données
Ce module gère la connexion à MySQL
"""
import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
from typing import Generator, Dict, Any
import os


class DatabaseConfig:
    """Configuration centralisée pour la base de données MySQL"""
    
    def __init__(self):
        # Configuration MySQL sécurisée avec les paramètres fournis
        self.database = "2025_M1"
        self.user = "root"
        self.password = ""  # Mot de passe vide comme spécifié
        self.host = "localhost"
        self.port = 3306
        self.charset = "utf8mb4"
        # Options de sécurité MySQL
        self.autocommit = False
        self.use_unicode = True
        self.sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO'
    
    def get_connection_params(self) -> dict:
        """Retourne les paramètres de connexion MySQL sécurisés"""
        return {
            "database": self.database,
            "user": self.user,
            "password": self.password,
            "host": self.host,
            "port": self.port,
            "charset": self.charset,
            "autocommit": self.autocommit,
            "use_unicode": self.use_unicode,
            "sql_mode": self.sql_mode,
            "raise_on_warnings": True,
            "get_warnings": True
        }


# Instance globale de configuration
db_config = DatabaseConfig()


@contextmanager
def get_db_connection():
    """
    Context manager pour la connexion à la base de données MySQL
    Garantit la fermeture automatique de la connexion
    """
    connection = None
    try:
        connection = mysql.connector.connect(**db_config.get_connection_params())
        yield connection
    except Error as e:
        print(f"Erreur de connexion MySQL: {e}")
        if connection and connection.is_connected():
            connection.rollback()
        raise
    finally:
        if connection and connection.is_connected():
            connection.close()


def get_db() -> Generator[mysql.connector.MySQLConnection, None, None]:
    """
    Dependency pour FastAPI
    Fournit une connexion à la base de données MySQL qui sera fermée automatiquement
    """
    connection = None
    try:
        connection = mysql.connector.connect(**db_config.get_connection_params())
        yield connection
    except Error as e:
        print(f"Erreur de connexion MySQL: {e}")
        if connection and connection.is_connected():
            connection.rollback()
        raise
    finally:
        if connection and connection.is_connected():
            connection.close()