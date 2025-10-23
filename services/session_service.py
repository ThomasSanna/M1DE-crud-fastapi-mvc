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
        # Utiliser la méthode to_dict() du modèle User afin d'inclure
        # systématiquement le flag is_admin et de garder un seul point
        # de vérité pour la forme des données utilisateur en session.
        try:
            user_data = user.to_dict()
        except Exception:
            # En cas d'objet non conforme, construire manuellement
            user_data = {
                "id": getattr(user, "user_id", None),
                "login": getattr(user, "login", ""),
                "email": getattr(user, "email", ""),
                "is_admin": bool(getattr(user, "is_admin", False))
            }

        # Protection basique contre les attaques XSS pour les champs affichés
        user_data["login"] = html.escape(user_data.get("login", ""))
        user_data["email"] = html.escape(user_data.get("email", ""))

        # Défensivement forcer la présence et le type du flag is_admin
        user_data["is_admin"] = bool(user_data.get("is_admin", False))
        request.session["user"] = user_data

    @staticmethod
    def set_user_admin_flag(request, is_admin: bool) -> None:
        """
        Met à jour le flag is_admin dans la session si nécessaire
        """
        if "user" in request.session and request.session["user"] is not None:
            request.session["user"]["is_admin"] = bool(is_admin)
    
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
    
    @staticmethod
    def is_admin(request: Request) -> bool:
        """
        Vérifie si l'utilisateur connecté est un admin
        
        Args:
            request: Requête FastAPI
            
        Returns:
            True si l'utilisateur est connecté et admin, False sinon
        """
        user = SessionService.get_current_user(request)
        return user is not None and user.get('is_admin', False)
    
    @staticmethod
    def add_flash_message(request: Request, message: str, category: str = "success") -> None:
        """
        Ajoute un message flash à la session
        
        Args:
            request: Requête FastAPI
            message: Message à afficher
            category: Catégorie du message (success, error, warning, info)
        """
        if "flash_messages" not in request.session:
            request.session["flash_messages"] = []
        
        request.session["flash_messages"].append({
            "message": message,  # No need to escape our own system messages
            "category": category
        })
    
    @staticmethod
    def get_flash_messages(request: Request) -> list:
        """
        Récupère et supprime les messages flash de la session
        
        Args:
            request: Requête FastAPI
            
        Returns:
            Liste des messages flash
        """
        messages = request.session.pop("flash_messages", [])
        return messages


# Instance globale du service de session
session_service = SessionService()