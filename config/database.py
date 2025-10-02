"""
Configuration de la base de données
Ce module gère la connexion à PostgreSQL
"""
import psycopg
from psycopg.rows import dict_row
from contextlib import contextmanager
from typing import Generator


class DatabaseConfig:
    """Configuration centralisée pour la base de données"""
    
    def __init__(self):
        self.dbname = "2025_M1"
        self.user = "postgres" 
        self.password = "postgres"
        self.host = "localhost"
        self.port = "5430"
    
    def get_connection_params(self) -> dict:
        """Retourne les paramètres de connexion"""
        return {
            "dbname": self.dbname,
            "user": self.user,
            "password": self.password,
            "host": self.host,
            "port": self.port,
            "row_factory": dict_row
        }


# Instance globale de configuration
db_config = DatabaseConfig()


@contextmanager
def get_db_connection():
    """
    Context manager pour la connexion à la base de données
    Garantit la fermeture automatique de la connexion
    """
    connection = None
    try:
        connection = psycopg.connect(**db_config.get_connection_params())
        yield connection
    finally:
        if connection:
            connection.close()


def get_db() -> Generator[psycopg.Connection, None, None]:
    """
    Dependency pour FastAPI
    Fournit une connexion à la base de données qui sera fermée automatiquement
    """
    with psycopg.connect(**db_config.get_connection_params()) as connection:
        yield connection