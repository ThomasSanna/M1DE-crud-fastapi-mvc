"""
Modèle User - Gestion des utilisateurs
Ce module contient la logique métier et les opérations CRUD pour les utilisateurs
"""
from typing import Optional, Dict, Any
from datetime import datetime
import psycopg
from psycopg.rows import dict_row


class User:
    """
    Modèle représentant un utilisateur
    Encapsule toutes les opérations liées aux utilisateurs
    """
    
    def __init__(self, user_id: Optional[int] = None, login: Optional[str] = None, 
                 email: Optional[str] = None, password_hash: Optional[str] = None,
                 date_new: Optional[datetime] = None, date_login: Optional[datetime] = None):
        self.user_id = user_id
        self.login = login
        self.email = email
        self.password_hash = password_hash
        self.date_new = date_new
        self.date_login = date_login
    
    @staticmethod
    def find_by_login(connection: psycopg.Connection, login: str) -> Optional['User']:
        """
        Recherche un utilisateur par son login
        
        Args:
            connection: Connexion à la base de données
            login: Login de l'utilisateur
            
        Returns:
            User ou None si non trouvé
        """
        try:
            result = connection.execute(
                'SELECT * FROM "user" WHERE user_login = %s', 
                (login,)
            ).fetchone()
            
            if result:
                return User(
                    user_id=result["user_id"],
                    login=result["user_login"],
                    email=result["user_mail"],
                    password_hash=result["user_password"],
                    date_new=result.get("user_date_new"),
                    date_login=result.get("user_date_login")
                )
            return None
        except Exception as e:
            print(f"Erreur lors de la recherche par login: {e}")
            return None
    
    @staticmethod
    def find_by_email(connection: psycopg.Connection, email: str) -> Optional['User']:
        """
        Recherche un utilisateur par son email
        
        Args:
            connection: Connexion à la base de données
            email: Email de l'utilisateur
            
        Returns:
            User ou None si non trouvé
        """
        try:
            result = connection.execute(
                'SELECT * FROM "user" WHERE user_mail = %s', 
                (email,)
            ).fetchone()
            
            if result:
                return User(
                    user_id=result["user_id"],
                    login=result["user_login"],
                    email=result["user_mail"],
                    password_hash=result["user_password"],
                    date_new=result.get("user_date_new"),
                    date_login=result.get("user_date_login")
                )
            return None
        except Exception as e:
            print(f"Erreur lors de la recherche par email: {e}")
            return None
    
    @staticmethod
    def find_by_login_or_email(connection: psycopg.Connection, login: str, email: str) -> Optional['User']:
        """
        Recherche un utilisateur par login OU email
        
        Args:
            connection: Connexion à la base de données
            login: Login de l'utilisateur
            email: Email de l'utilisateur
            
        Returns:
            User ou None si non trouvé
        """
        try:
            result = connection.execute(
                'SELECT * FROM "user" WHERE user_login = %s OR user_mail = %s', 
                (login, email)
            ).fetchone()
            
            if result:
                return User(
                    user_id=result["user_id"],
                    login=result["user_login"],
                    email=result["user_mail"],
                    password_hash=result["user_password"],
                    date_new=result.get("user_date_new"),
                    date_login=result.get("user_date_login")
                )
            return None
        except Exception as e:
            print(f"Erreur lors de la recherche par login/email: {e}")
            return None
    
    def save(self, connection: psycopg.Connection) -> bool:
        """
        Sauvegarde l'utilisateur en base de données
        
        Args:
            connection: Connexion à la base de données
            
        Returns:
            True si la sauvegarde a réussi, False sinon
        """
        try:
            if self.user_id is None:
                # Création d'un nouvel utilisateur
                result = connection.execute(
                    'INSERT INTO "user" (user_login, user_password, user_mail) VALUES (%s, %s, %s) RETURNING user_id, user_login, user_mail',
                    (self.login, self.password_hash, self.email)
                ).fetchone()
                
                if result:
                    self.user_id = result["user_id"]
                    connection.commit()
                    return True
                return False
            else:
                # Mise à jour d'un utilisateur existant
                connection.execute(
                    'UPDATE "user" SET user_login = %s, user_password = %s, user_mail = %s WHERE user_id = %s',
                    (self.login, self.password_hash, self.email, self.user_id)
                )
                connection.commit()
                return True
                
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            connection.rollback()
            return False
    
    def update_last_login(self, connection: psycopg.Connection) -> bool:
        """
        Met à jour la date de dernière connexion
        
        Args:
            connection: Connexion à la base de données
            
        Returns:
            True si la mise à jour a réussi, False sinon
        """
        try:
            connection.execute(
                'UPDATE "user" SET user_date_login = %s WHERE user_id = %s',
                (datetime.now(), self.user_id)
            )
            connection.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de la mise à jour de la date de connexion: {e}")
            connection.rollback()
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit l'utilisateur en dictionnaire pour les sessions/templates
        
        Returns:
            Dictionnaire avec les données de l'utilisateur
        """
        return {
            "id": self.user_id,
            "login": self.login,
            "email": self.email
        }
    
    def __repr__(self) -> str:
        """Représentation string de l'utilisateur"""
        return f"User(id={self.user_id}, login='{self.login}', email='{self.email}')"