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
import re


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
    
    def profile(self, request: Request, db=Depends(get_db)):
        """
        Affiche le profil de l'utilisateur connecté
        """
        # Vérifier si l'utilisateur est connecté
        if not session_service.is_authenticated(request):
            return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        
        current_user_data = session_service.get_current_user(request)
        user = User.find_by_id(db, current_user_data["id"])
        
        if not user:
            session_service.clear_session(request)
            return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        
        # Récupérer les messages flash
        flash_messages = session_service.get_flash_messages(request)
        
        return self.templates.TemplateResponse(
            "auth/profile.html", 
            {"request": request, "user": current_user_data, "profile_user": user, "flash_messages": flash_messages}
        )
    
    def edit_profile_form(self, request: Request, db=Depends(get_db)):
        """
        Affiche le formulaire de modification du profil
        """
        # Vérifier si l'utilisateur est connecté
        if not session_service.is_authenticated(request):
            return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        
        current_user_data = session_service.get_current_user(request)
        user = User.find_by_id(db, current_user_data["id"])
        
        if not user:
            session_service.clear_session(request)
            return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        
        return self.templates.TemplateResponse(
            "auth/edit_profile.html", 
            {"request": request, "user": current_user_data, "profile_user": user}
        )
    
    def edit_profile(self, request: Request, login: str = Form(...), 
                    email: str = Form(...), current_password: str = Form(None),
                    new_password: str = Form(None), db=Depends(get_db)):
        """
        Traite la modification du profil utilisateur
        """
        # Vérifier si l'utilisateur est connecté
        if not session_service.is_authenticated(request):
            return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        
        current_user_data = session_service.get_current_user(request)
        user = User.find_by_id(db, current_user_data["id"])
        
        if not user:
            session_service.clear_session(request)
            return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        
        try:
            # Validation des données de base
            login = login.strip()
            email = email.strip()
            
            errors = []
            
            # Validation du login
            if not login or len(login) < 3:
                errors.append("Le login doit contenir au moins 3 caractères")
            
            # Validation de l'email
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not email or not re.match(email_regex, email):
                errors.append("L'adresse email n'est pas valide")
            
            # Vérifier si le login ou l'email est déjà utilisé par un autre utilisateur
            if login != user.login or email != user.email:
                existing_user = User.find_by_login_or_email(db, login, email)
                if existing_user and existing_user.user_id != user.user_id:
                    errors.append("Ce login ou cette adresse email est déjà utilisé(e) par un autre compte")
            
            # Si changement de mot de passe demandé
            if new_password:
                if not current_password:
                    errors.append("Vous devez entrer votre mot de passe actuel pour le modifier")
                elif not auth_service.verify_password(current_password, user.password_hash):
                    errors.append("Le mot de passe actuel est incorrect")
                elif len(new_password) < 6:
                    errors.append("Le nouveau mot de passe doit contenir au moins 6 caractères")
            
            if errors:
                return self.templates.TemplateResponse(
                    "auth/edit_profile.html",
                    {"request": request, "user": current_user_data, 
                     "profile_user": user, "error": errors[0]}
                )
            
            # Mise à jour des informations
            user.login = login
            user.email = email
            
            # Mise à jour du mot de passe si demandé
            if new_password:
                user.password_hash = auth_service.hash_password(new_password)
            
            # Sauvegarde en base de données
            if user.save(db):
                # Mise à jour de la session
                session_service.create_user_session(request, user)
                session_service.add_flash_message(request, "Profil mis à jour avec succès", "success")
                return RedirectResponse(url="/profile", status_code=status.HTTP_303_SEE_OTHER)
            else:
                return self.templates.TemplateResponse(
                    "auth/edit_profile.html",
                    {"request": request, "user": current_user_data,
                     "profile_user": user, "error": "Erreur lors de la mise à jour du profil"}
                )
        
        except Exception as e:
            print(f"Erreur lors de la mise à jour du profil: {e}")
            return self.templates.TemplateResponse(
                "auth/edit_profile.html",
                {"request": request, "user": current_user_data,
                 "profile_user": user, "error": "Erreur lors de la mise à jour du profil"}
            )
    
    def delete_account_form(self, request: Request, db=Depends(get_db)):
        """
        Affiche le formulaire de confirmation de suppression du compte
        """
        # Vérifier si l'utilisateur est connecté
        if not session_service.is_authenticated(request):
            return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        
        current_user_data = session_service.get_current_user(request)
        user = User.find_by_id(db, current_user_data["id"])
        
        if not user:
            session_service.clear_session(request)
            return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        
        return self.templates.TemplateResponse(
            "auth/delete_account.html",
            {"request": request, "user": current_user_data, "profile_user": user}
        )
    
    def delete_account(self, request: Request, password: str = Form(...), db=Depends(get_db)):
        """
        Traite la suppression du compte utilisateur
        """
        # Vérifier si l'utilisateur est connecté
        if not session_service.is_authenticated(request):
            return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        
        current_user_data = session_service.get_current_user(request)
        user = User.find_by_id(db, current_user_data["id"])
        
        if not user:
            session_service.clear_session(request)
            return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        
        try:
            # Vérifier le mot de passe
            if not password:
                return self.templates.TemplateResponse(
                    "auth/delete_account.html",
                    {"request": request, "user": current_user_data,
                     "profile_user": user, "error": "Vous devez entrer votre mot de passe"}
                )
            
            if not auth_service.verify_password(password, user.password_hash):
                return self.templates.TemplateResponse(
                    "auth/delete_account.html",
                    {"request": request, "user": current_user_data,
                     "profile_user": user, "error": "Le mot de passe est incorrect"}
                )
            
            # Supprimer le compte
            if user.delete(db):
                session_service.clear_session(request)
                session_service.add_flash_message(request, "Votre compte a été supprimé avec succès", "success")
                return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
            else:
                return self.templates.TemplateResponse(
                    "auth/delete_account.html",
                    {"request": request, "user": current_user_data,
                     "profile_user": user, "error": "Erreur lors de la suppression du compte"}
                )
        
        except Exception as e:
            print(f"Erreur lors de la suppression du compte: {e}")
            return self.templates.TemplateResponse(
                "auth/delete_account.html",
                {"request": request, "user": current_user_data,
                 "profile_user": user, "error": "Erreur lors de la suppression du compte"}
            )