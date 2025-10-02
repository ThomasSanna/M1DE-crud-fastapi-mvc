"""
Service d'authentification
Gère le hachage des mots de passe et la vérification d'authentification
"""
from passlib.context import CryptContext
import hashlib


class AuthService:
    """Service pour l'authentification et la gestion des mots de passe"""
    
    # Limite de bcrypt : 72 bytes maximum
    BCRYPT_MAX_BYTES = 72
    
    def __init__(self):
        """Initialise le contexte de hachage des mots de passe"""
        self.password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def _prepare_password(self, password: str) -> str:
        """
        Prépare un mot de passe pour bcrypt en gérant la limitation de 72 bytes
        
        Pour les mots de passe longs, utilise SHA-256 pour les réduire à une taille acceptable
        tout en préservant l'entropie.
        
        Args:
            password: Mot de passe en clair
            
        Returns:
            Mot de passe préparé (72 bytes max)
        """
        # Encode le mot de passe en UTF-8
        password_bytes = password.encode('utf-8')
        
        # Si le mot de passe dépasse 72 bytes, utilise SHA-256
        if len(password_bytes) > self.BCRYPT_MAX_BYTES:
            # SHA-256 produit toujours 32 bytes (< 72), compatible avec bcrypt
            return hashlib.sha256(password_bytes).hexdigest()
        
        return password
    
    def hash_password(self, password: str) -> str:
        """
        Hache un mot de passe
        
        Args:
            password: Mot de passe en clair
            
        Returns:
            Mot de passe haché
        """
        prepared_password = self._prepare_password(password)
        return self.password_context.hash(prepared_password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Vérifie un mot de passe contre son hash
        
        Args:
            plain_password: Mot de passe en clair
            hashed_password: Mot de passe haché
            
        Returns:
            True si le mot de passe correspond, False sinon
        """
        prepared_password = self._prepare_password(plain_password)
        return self.password_context.verify(prepared_password, hashed_password)


# Instance globale du service d'authentification
auth_service = AuthService()