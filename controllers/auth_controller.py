"""
Contrôleur d'authentification
Gère les routes liées à la connexion, déconnexion et inscription
"""
from fastapi import Form, Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import psycopg

from config.database import get_db
from models.user_model import User
from services.auth_service import auth_service
from services.session_service import session_service
from services.validation_service import validation_service


class AuthController:
    """Contrôleur pour l'authentification"""
    
    def __init__(self, templates: Jinja2Templates):
        self.templates = templates
    
    def login_form(self, request: Request):
        """
        Affiche le formulaire de connexion
        Redirige vers l'accueil si l'utilisateur est déjà connecté
        """
        if session_service.is_authenticated(request):
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        
        return self.templates.TemplateResponse("auth/login.html", {"request": request})
    
    def login(self, request: Request, login: str = Form(...), password: str = Form(...), db=Depends(get_db)):
        """
        Traite la connexion d'un utilisateur
        """
        # Validation des données
        validation_errors = validation_service.validate_login_data(login, password)
        if validation_errors:
            return self.templates.TemplateResponse(
                "auth/login.html", 
                {"request": request, "error": validation_errors[0]}
            )
        
        try:
            # Recherche de l'utilisateur
            user = User.find_by_login(db, login.strip())
            
            # Vérification du mot de passe
            if not user or not auth_service.verify_password(password, user.password_hash):
                return self.templates.TemplateResponse(
                    "auth/login.html", 
                    {"request": request, "error": "Login ou mot de passe incorrect"}
                )
            
            # Mise à jour de la date de connexion
            user.update_last_login(db)
            
            # Création de la session
            session_service.create_user_session(request, user)
            
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
            
        except Exception as e:
            print(f"Erreur lors de la connexion: {e}")
            return self.templates.TemplateResponse(
                "auth/login.html", 
                {"request": request, "error": "Erreur de connexion"}
            )
    
    def logout(self, request: Request):
        """Déconnecte l'utilisateur"""
        session_service.clear_session(request)
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    def register_form(self, request: Request):
        """
        Affiche le formulaire d'inscription
        Redirige vers l'accueil si l'utilisateur est déjà connecté
        """
        if session_service.is_authenticated(request):
            return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        
        return self.templates.TemplateResponse("auth/register.html", {"request": request})
    
    def register(self, request: Request, login: str = Form(...), email: str = Form(...), 
                password: str = Form(...), db=Depends(get_db)):
        """
        Traite l'inscription d'un nouvel utilisateur
        """
        # Validation des données
        validation_errors = validation_service.validate_registration_data(login, email, password)
        if validation_errors:
            return self.templates.TemplateResponse(
                "auth/register.html", 
                {"request": request, "error": validation_errors[0]}
            )
        
        try:
            # Vérification de l'unicité du login/email
            existing_user = User.find_by_login_or_email(db, login.strip(), email.strip())
            if existing_user:
                return self.templates.TemplateResponse(
                    "auth/register.html", 
                    {"request": request, "error": "Ce login ou cette adresse email est déjà utilisé(e)"}
                )
            
            # Création du nouvel utilisateur
            password_hash = auth_service.hash_password(password)
            new_user = User(
                login=login.strip(),
                email=email.strip(),
                password_hash=password_hash
            )
            
            # Sauvegarde en base de données
            if new_user.save(db):
                # Création de la session pour l'utilisateur nouvellement inscrit
                session_service.create_user_session(request, new_user)
                return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
            else:
                return self.templates.TemplateResponse(
                    "auth/register.html", 
                    {"request": request, "error": "Erreur lors de la création du compte"}
                )
                
        except Exception as e:
            print(f"Erreur lors de l'inscription: {e}")
            return self.templates.TemplateResponse(
                "auth/register.html", 
                {"request": request, "error": "Erreur lors de la création du compte"}
            )