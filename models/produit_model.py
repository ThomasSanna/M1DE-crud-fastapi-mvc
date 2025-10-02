from typing import Optional, Dict, Any
from datetime import datetime
import mysql.connector
from mysql.connector import Error

class Produit:
    """
    Modèle représentant un produit
    Encapsule toutes les opérations liées aux produits
    """
    
    def __init__(self, id_p: Optional[int] = None, type_p: str = "", designation_p: str = "", 
                 prix_ht: float = 0.0, date_in: Optional[datetime] = None, 
                 timeS_in: Optional[str] = None, stock_p: int = 0):
        self.id_p = id_p
        self.type_p = type_p
        self.designation_p = designation_p
        self.prix_ht = prix_ht
        self.date_in = date_in
        self.timeS_in = timeS_in
        self.stock_p = stock_p
        
    @staticmethod
    def find_by_id(connection: mysql.connector.MySQLConnection, id: int) -> Optional['Produit']:
        """
        Recherche un produit par son ID
        
        Args:
            connection: Connexion à la bdd
            id: ID du produit
            
        Returns:
            Produit ou None si non trouvé
        """
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                'SELECT * FROM `produit` WHERE id_p = %s',
                (id,)
            )
            result = cursor.fetchone()
            
            if result:
                return Produit(
                    id_p=result["id_p"],
                    type_p=result["type_p"],
                    designation_p=result["designation_p"],
                    prix_ht=result["prix_ht"],
                    date_in=result.get("date_in"), # Utilisation de get pour éviter KeyError (si la clé n'existe pas)
                    timeS_in=result.get("timeS_in"),
                    stock_p=result["stock_p"]
                )
            return None
        except Error as e:
            print(f"Erreur MySQL lors de la recherche par ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
                
    @staticmethod
    def find_all(connection: mysql.connector.MySQLConnection) -> list['Produit']:
        """
        Récupère tous les produits
        
        Args:
            connection: Connexion à la bdd
            
        Returns:
            Liste de produits
        """
        cursor = None
        produits = []
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM `produit`')
            results = cursor.fetchall()
            
            for result in results:
                produits.append(Produit(
                    id_p=result["id_p"],
                    type_p=result["type_p"],
                    designation_p=result["designation_p"],
                    prix_ht=result["prix_ht"],
                    date_in=result.get("date_in"),
                    timeS_in=result.get("timeS_in"),
                    stock_p=result["stock_p"]
                ))
            return produits
        except Error as e:
            print(f"Erreur MySQL lors de la récupération de tous les produits: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
                
    @staticmethod
    def find_by_type(connection: mysql.connector.MySQLConnection, type_p: str) -> list['Produit']:
        """
        Recherche des produits par leur type
        
        Args:
            connection: Connexion à la bdd
            type_p: Type de produit
            
        Returns:
            Liste de produits correspondant au type
        """
        cursor = None
        produits = []
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                'SELECT * FROM `produit` WHERE type_p = %s',
                (type_p,)
            )
            results = cursor.fetchall()
            
            for result in results:
                produits.append(Produit(
                    id_p=result["id_p"],
                    type_p=result["type_p"],
                    designation_p=result["designation_p"],
                    prix_ht=result["prix_ht"],
                    date_in=result.get("date_in"),
                    timeS_in=result.get("timeS_in"),
                    stock_p=result["stock_p"]
                ))
            return produits
        except Error as e:
            print(f"Erreur MySQL lors de la recherche par type: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
                
    def save(self, connection: mysql.connector.MySQLConnection) -> bool:
        """
        Sauvegarde le produit en base de données MySQL
        
        Args:
            connection: Connexion à la base de données MySQL
            
        Returns:
            True si la sauvegarde a réussi, False sinon
        """
        cursor = None
        
        try:
            cursor = connection.cursor(dictionary=True)
            if self.id_p is None:
                # Créer un nouveau produit
                cursor.execute(
                    'INSERT INTO `produit` (type_p, designation_p, prix_ht, date_in, stock_p) VALUES (%s, %s, %s, %s, %s)',
                    (self.type_p, self.designation_p, self.prix_ht, self.date_in, self.stock_p)
                )
                
                if cursor.rowcount > 0:
                    self.id_p = cursor.lastrowid
                    connection.commit()
                    return True
                return False
            else:
                # Mettre à jour un produit existant
                cursor.execute(
                    'UPDATE `produit` SET type_p = %s, designation_p = %s, prix_ht = %s, date_in = %s, stock_p = %s WHERE id_p = %s',
                    (self.type_p, self.designation_p, self.prix_ht, self.date_in, self.stock_p, self.id_p)
                )
                connection.commit()
                return True
            
        except Error as e:
            print(f"Erreur MySQL lors de la sauvegarde: {e}")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
                
    @staticmethod
    def delete_by_id(connection: mysql.connector.MySQLConnection, id: int) -> bool:
        """
        Supprime un produit par son ID
        
        Args:
            connection: Connexion à la bdd
            id: ID du produit à supprimer
            
        Returns:
            True si la suppression a réussi, False sinon
        """
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute(
                'DELETE FROM `produit` WHERE id_p = %s',
                (id,)
            )
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Erreur MySQL lors de la suppression: {e}")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit l'objet Produit en dictionnaire
        
        Returns:
            Dictionnaire représentant le produit
        """
        return {
            "id_p": self.id_p,
            "type_p": self.type_p,
            "designation_p": self.designation_p,
            "prix_ht": self.prix_ht,
            "date_in": self.date_in,
            "timeS_in": self.timeS_in,
            "stock_p": self.stock_p
        }
        
    def __repr__(self) -> str:
        """Représentation string du produit"""
        return f"Produit(id={self.id_p}, type='{self.type_p}', designation='{self.designation_p}', prix_ht={self.prix_ht}, stock={self.stock_p})"