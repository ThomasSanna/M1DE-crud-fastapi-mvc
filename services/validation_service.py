"""
Service de validation des données utilisateur
Centralise toute la logique de validation
"""
import re
from typing import List, Optional
from config.app_config import app_config


class ValidationService:
    """Service pour la validation des données utilisateur"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Valide le format d'un email
        
        Args:
            email: Adresse email à valider
            
        Returns:
            True si l'email est valide, False sinon
        """
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))
    
    @staticmethod
    def validate_username(username: str) -> List[str]:
        """
        Valide un nom d'utilisateur
        
        Args:
            username: Nom d'utilisateur à valider
            
        Returns:
            Liste des erreurs de validation (vide si valide)
        """
        errors = []
        
        if not username or len(username.strip()) == 0:
            errors.append("Le nom d'utilisateur est requis")
        elif len(username.strip()) < app_config.USERNAME_MIN_LENGTH:
            errors.append(f"Le nom d'utilisateur doit faire au moins {app_config.USERNAME_MIN_LENGTH} caractères")
        elif len(username.strip()) > 50:
            errors.append("Le nom d'utilisateur ne peut pas dépasser 50 caractères")
        elif not re.match(r'^[a-zA-Z0-9_-]+$', username.strip()):
            errors.append("Le nom d'utilisateur ne peut contenir que des lettres, chiffres, tirets et underscores")
        
        return errors
    
    @staticmethod
    def validate_password(password: str) -> List[str]:
        """
        Valide un mot de passe
        
        Args:
            password: Mot de passe à valider
            
        Returns:
            Liste des erreurs de validation (vide si valide)
        """
        errors = []
        
        if not password:
            errors.append("Le mot de passe est requis")
        elif len(password) < app_config.PASSWORD_MIN_LENGTH:
            errors.append(f"Le mot de passe doit faire au moins {app_config.PASSWORD_MIN_LENGTH} caractères")
        elif len(password) > 200:
            # Limite raisonnable pour l'UI, le backend gère les mots de passe longs avec SHA-256
            errors.append("Le mot de passe ne peut pas dépasser 200 caractères")
        
        return errors
    
    @staticmethod
    def validate_registration_data(username: str, email: str, password: str) -> List[str]:
        """
        Valide toutes les données d'inscription
        
        Args:
            username: Nom d'utilisateur
            email: Adresse email
            password: Mot de passe
            
        Returns:
            Liste des erreurs de validation (vide si tout est valide)
        """
        errors = []
        
        # Validation du nom d'utilisateur
        errors.extend(ValidationService.validate_username(username))
        
        # Validation de l'email
        if not email or len(email.strip()) == 0:
            errors.append("L'adresse email est requise")
        elif not ValidationService.validate_email(email.strip()):
            errors.append("Le format de l'adresse email est invalide")
        
        # Validation du mot de passe
        errors.extend(ValidationService.validate_password(password))
        
        return errors
    
    @staticmethod
    def validate_login_data(login: str, password: str) -> List[str]:
        """
        Valide les données de connexion
        
        Args:
            login: Login ou email
            password: Mot de passe
            
        Returns:
            Liste des erreurs de validation (vide si tout est valide)
        """
        errors = []
        
        if not login or len(login.strip()) == 0:
            errors.append("Le login est requis")
        
        if not password or len(password) == 0:
            errors.append("Le mot de passe est requis")
        
        return errors


# Instance globale du service de validation
validation_service = ValidationService()