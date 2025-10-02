"""
Contrôleur principal de l'application
Gère les pages principales comme l'accueil
"""
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from services.session_service import session_service


class MainController:
    """Contrôleur pour les pages principales"""
    
    def __init__(self, templates: Jinja2Templates):
        self.templates = templates
    
    def home(self, request: Request):
        """
        Affiche la page d'accueil
        Adapte le contenu selon que l'utilisateur est connecté ou non
        """
        current_user = session_service.get_current_user(request)
        return self.templates.TemplateResponse(
            "index.html", 
            {"request": request, "user": current_user}
        )