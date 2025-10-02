"""
Contrôleur de produits
"""
from fastapi import Form, Request, Depends, status, Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import psycopg
from datetime import date

from config.database import get_db
from models.produit_model import Produit
from services.session_service import session_service

class ProduitController:
    """Contrôleur pour la gestion des produits"""
    
    def __init__(self, templates: Jinja2Templates):
        self.templates = templates
    
    def list_produits(self, request: Request, db=Depends(get_db)):
        """
        Affiche la liste de tous les produits
        """
        produits = Produit.find_all(db)
        user = session_service.get_current_user(request)
        flash_messages = session_service.get_flash_messages(request)
        return self.templates.TemplateResponse(
            "produit/produits.html", 
            {"request": request, "produits": produits, "user": user, "flash_messages": flash_messages}
        )
    
    def add_produit_form(self, request: Request, db=Depends(get_db)):
        """
        Affiche le formulaire d'ajout de produit
        """
        user = session_service.get_current_user(request)
        if not user:
            return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        
        today = date.today()
        return self.templates.TemplateResponse(
            "produit/produit_add.html",
            {"request": request, "user": user, "today": today}
        )
        
    def add_produit(self, 
                    request: Request,
                    type_p: str = Form(...),
                    designation_p: str = Form(...),
                    prix_ht: float = Form(...),
                    date_in: str = Form(...),
                    stock_p: int = Form(...),
                    db=Depends(get_db)):
        """
        Traite le formulaire d'ajout de produit
        """
        user = session_service.get_current_user(request)
        if not user:
            return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        
        # Conversion de la date au format YYYY-MM-DD
        try:
            day, month, year = map(int, date_in.split('/'))
            formatted_date = date(year, month, day)
        except ValueError:
            formatted_date = date.today()
        
        new_produit = Produit(
            type_p=type_p,
            designation_p=designation_p,
            prix_ht=prix_ht,
            date_in=formatted_date,
            stock_p=stock_p
        )
        
        if new_produit.save(db):
            # Ajouter un message de succès
            session_service.add_flash_message(
                request, 
                f"Le produit '{designation_p}' a été ajouté avec succès !", 
                "success"
            )
            return RedirectResponse(url="/produits", status_code=status.HTTP_303_SEE_OTHER)
        else:
            error_message = "Erreur lors de l'ajout du produit. Veuillez réessayer."
            return self.templates.TemplateResponse(
                "produit/produit_add.html",
                {
                    "request": request, 
                    "user": user, 
                    "error": error_message,
                    "today": date.today()
                }
            )
    
    def delete_produit(self, request: Request, id: int, db=Depends(get_db)):
        """
        Supprime un produit par son ID
        
        Args:
            request: Objet Request de FastAPI
            id: ID du produit à supprimer
            db: Connexion à la base de données
        """
        user = session_service.get_current_user(request)
        if not user:
            return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        
        # Récupérer le produit pour avoir son nom avant suppression
        produit = Produit.find_by_id(db, id)
        
        if not produit:
            session_service.add_flash_message(
                request, 
                "Le produit à supprimer n'existe pas.", 
                "error"
            )
            return RedirectResponse(url="/produits", status_code=status.HTTP_303_SEE_OTHER)
        
        # Supprimer le produit
        if Produit.delete_by_id(db, id):
            session_service.add_flash_message(
                request, 
                f"Le produit '{produit.designation_p}' a été supprimé avec succès !", 
                "success"
            )
        else:
            session_service.add_flash_message(
                request, 
                "Erreur lors de la suppression du produit.", 
                "error"
            )
        
        return RedirectResponse(url="/produits", status_code=status.HTTP_303_SEE_OTHER)
    
    def view_produit(self, request: Request, id: int, db=Depends(get_db)):
        """
        Affiche les détails d'un produit par son ID
        """
        produit = Produit.find_by_id(db, id)
        user = session_service.get_current_user(request)
        flash_messages = session_service.get_flash_messages(request)
        
        if not produit:
            session_service.add_flash_message(
                request, 
                "Le produit demandé n'existe pas.", 
                "error"
            )
            return RedirectResponse(url="/produits", status_code=status.HTTP_303_SEE_OTHER)
        
        return self.templates.TemplateResponse(
            "produit/produit_view.html",
            {"request": request, "produit": produit, "user": user, "flash_messages": flash_messages}
        )

    def edit_produit_form(self, request: Request, id: int, db=Depends(get_db)):
        """
        Affiche le formulaire d'édition d'un produit
        """
        user = session_service.get_current_user(request)
        if not user:
            return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        
        produit = Produit.find_by_id(db, id)
        if not produit:
            session_service.add_flash_message(
                request, 
                "Le produit à éditer n'existe pas.", 
                "error"
            )
            return RedirectResponse(url="/produits", status_code=status.HTTP_303_SEE_OTHER)
        
        return self.templates.TemplateResponse(
            "produit/produit_edit.html",
            {"request": request, "produit": produit, "user": user}
        )
    
    def edit_produit(self, 
                     request: Request,
                     id: int,
                     type_p: str = Form(...),
                     designation_p: str = Form(...),
                     prix_ht: float = Form(...),
                     date_in: str = Form(...),
                     stock_p: int = Form(...),
                     db=Depends(get_db)):
        """
        Traite le formulaire de modification de produit
        """
        user = session_service.get_current_user(request)
        if not user:
            return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        
        # Vérifier que le produit existe
        produit = Produit.find_by_id(db, id)
        if not produit:
            session_service.add_flash_message(
                request, 
                "Le produit à modifier n'existe pas.", 
                "error"
            )
            return RedirectResponse(url="/produits", status_code=status.HTTP_303_SEE_OTHER)
        
        # Conversion de la date au format approprié
        try:
            if '/' in date_in:
                day, month, year = map(int, date_in.split('/'))
                formatted_date = date(year, month, day)
            else:
                # Format YYYY-MM-DD (de l'input date HTML)
                year, month, day = map(int, date_in.split('-'))
                formatted_date = date(year, month, day)
        except ValueError:
            formatted_date = produit.date_in or date.today()
        
        # Mettre à jour les propriétés du produit
        produit.type_p = type_p
        produit.designation_p = designation_p
        produit.prix_ht = prix_ht
        produit.date_in = formatted_date
        produit.stock_p = stock_p
        
        # Sauvegarder les modifications
        if produit.save(db):
            session_service.add_flash_message(
                request, 
                f"Le produit '{designation_p}' a été modifié avec succès !", 
                "success"
            )
            return RedirectResponse(url=f"/produits/{id}", status_code=status.HTTP_303_SEE_OTHER)
        else:
            error_message = "Erreur lors de la modification du produit. Veuillez réessayer."
            return self.templates.TemplateResponse(
                "produit/produit_edit.html",
                {
                    "request": request, 
                    "produit": produit, 
                    "user": user, 
                    "error": error_message
                }
            )