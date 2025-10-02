"""
Service de gestion des sessions utilisateur
Gère la création, validation et nettoyage des sessions
"""
import html
from typing import Optional, Dict, Any
from fastapi import Request

from models.user_model import User


class SessionService:
    """Service pour la gestion des sessions utilisateur"""
    
    @staticmethod
    def create_user_session(request: Request, user: User) -> None:
        """
        Crée une session utilisateur avec protection XSS
        
        Args:
            request: Requête FastAPI
            user: Objet utilisateur
        """
        request.session["user"] = {
            "id": user.user_id,
            "login": html.escape(user.login),
            "email": html.escape(user.email)
        }
    
    @staticmethod
    def get_current_user(request: Request) -> Optional[Dict[str, Any]]:
        """
        Récupère l'utilisateur actuellement connecté depuis la session
        
        Args:
            request: Requête FastAPI
            
        Returns:
            Dictionnaire avec les données utilisateur ou None
        """
        return request.session.get("user")
    
    @staticmethod
    def clear_session(request: Request) -> None:
        """
        Efface la session utilisateur
        
        Args:
            request: Requête FastAPI
        """
        request.session.clear()
    
    @staticmethod
    def is_authenticated(request: Request) -> bool:
        """
        Vérifie si un utilisateur est authentifié
        
        Args:
            request: Requête FastAPI
            
        Returns:
            True si l'utilisateur est connecté, False sinon
        """
        return "user" in request.session and request.session["user"] is not None


# Instance globale du service de session
session_service = SessionService()