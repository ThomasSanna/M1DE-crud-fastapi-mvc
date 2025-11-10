"""
Service de gestion des images
"""
import os
import shutil
from fastapi import UploadFile
from pathlib import Path

class ImageService:
    """Service pour gérer les images"""
    
    def __init__(self):
        # Chemin vers le dossier d'images des produits
        self.images_dir = Path("static/images/produits")
        
        # Créer le dossier s'il n'existe pas
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        # Extensions autorisées
        self.allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif'}
        
    async def save_product_image(self, image: UploadFile) -> str:
        """
        Sauvegarde une image de produit
        
        Args:
            image: Fichier image uploadé
            
        Returns:
            Nom du fichier sauvegardé ou None si erreur
        """
        if not image:
            return None
            
        # Vérifier l'extension
        ext = Path(image.filename).suffix.lower()
        if ext not in self.allowed_extensions:
            return None
            
        # Créer un nom de fichier sécurisé
        safe_filename = Path(image.filename).stem.lower()
        safe_filename = "".join(c for c in safe_filename if c.isalnum() or c in ('-', '_'))
        safe_filename = f"{safe_filename}{ext}"
        
        # Chemin complet du fichier
        file_path = self.images_dir / safe_filename
        
        try:
            # Sauvegarder le fichier
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            return safe_filename
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de l'image: {e}")
            return None
            
    def delete_product_image(self, filename: str) -> bool:
        """
        Supprime une image de produit
        
        Args:
            filename: Nom du fichier à supprimer
            
        Returns:
            True si la suppression a réussi, False sinon
        """
        if not filename:
            return False
            
        file_path = self.images_dir / filename
        try:
            if file_path.exists():
                file_path.unlink()
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression de l'image: {e}")
            return False

image_service = ImageService()