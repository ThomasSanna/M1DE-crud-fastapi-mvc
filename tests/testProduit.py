"""
Tests pour le modèle Produit
Ce module contient tous les tests unitaires pour la classe Produit
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, date
import sys
import os

# Ajouter le répertoire parent au path pour importer les modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.produit_model import Produit
from mysql.connector import Error


class TestProduit(unittest.TestCase):
    """Classe de tests pour le modèle Produit"""
    
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.produit_data = {
            'id_p': 1,
            'type_p': 'Électronique',
            'designation_p': 'Smartphone',
            'prix_ht': 299.99,
            'date_in': date(2025, 10, 2),
            'timeS_in': '2025-10-02 15:30:00',
            'stock_p': 50
        }
        
        self.mock_connection = Mock()
        self.mock_cursor = Mock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        
    def tearDown(self):
        """Nettoyage après chaque test"""
        self.mock_connection.reset_mock()
        self.mock_cursor.reset_mock()


class TestProduitInit(TestProduit):
    """Tests pour l'initialisation de la classe Produit"""
    
    def test_init_with_all_parameters(self):
        """Test d'initialisation avec tous les paramètres"""
        produit = Produit(
            id_p=1,
            type_p="Électronique",
            designation_p="Smartphone",
            prix_ht=299.99,
            date_in=date(2025, 10, 2),
            timeS_in="2025-10-02 15:30:00",
            stock_p=50
        )
        
        self.assertEqual(produit.id_p, 1)
        self.assertEqual(produit.type_p, "Électronique")
        self.assertEqual(produit.designation_p, "Smartphone")
        self.assertEqual(produit.prix_ht, 299.99)
        self.assertEqual(produit.date_in, date(2025, 10, 2))
        self.assertEqual(produit.timeS_in, "2025-10-02 15:30:00")
        self.assertEqual(produit.stock_p, 50)
        
    def test_init_with_default_parameters(self):
        """Test d'initialisation avec les paramètres par défaut"""
        produit = Produit()
        
        self.assertIsNone(produit.id_p)
        self.assertEqual(produit.type_p, "")
        self.assertEqual(produit.designation_p, "")
        self.assertEqual(produit.prix_ht, 0.0)
        self.assertIsNone(produit.date_in)
        self.assertIsNone(produit.timeS_in)
        self.assertEqual(produit.stock_p, 0)
        
    def test_init_partial_parameters(self):
        """Test d'initialisation avec des paramètres partiels"""
        produit = Produit(
            type_p="Livre",
            designation_p="Guide Python",
            prix_ht=29.99
        )
        
        self.assertIsNone(produit.id_p)
        self.assertEqual(produit.type_p, "Livre")
        self.assertEqual(produit.designation_p, "Guide Python")
        self.assertEqual(produit.prix_ht, 29.99)
        self.assertIsNone(produit.date_in)
        self.assertIsNone(produit.timeS_in)
        self.assertEqual(produit.stock_p, 0)


class TestProduitFindById(TestProduit):
    """Tests pour la méthode find_by_id"""
    
    def test_find_by_id_success(self):
        """Test de recherche par ID réussie"""
        # Configuration du mock
        self.mock_cursor.fetchone.return_value = self.produit_data
        
        # Appel de la méthode
        produit = Produit.find_by_id(self.mock_connection, 1)
        
        # Vérifications
        self.assertIsNotNone(produit)
        self.assertEqual(produit.id_p, 1)
        self.assertEqual(produit.type_p, 'Électronique')
        self.assertEqual(produit.designation_p, 'Smartphone')
        self.assertEqual(produit.prix_ht, 299.99)
        
        # Vérification des appels
        self.mock_connection.cursor.assert_called_once_with(dictionary=True)
        self.mock_cursor.execute.assert_called_once_with(
            'SELECT * FROM `produit` WHERE id_p = %s',
            (1,)
        )
        self.mock_cursor.close.assert_called_once()
        
    def test_find_by_id_not_found(self):
        """Test de recherche par ID non trouvé"""
        # Configuration du mock
        self.mock_cursor.fetchone.return_value = None
        
        # Appel de la méthode
        produit = Produit.find_by_id(self.mock_connection, 999)
        
        # Vérifications
        self.assertIsNone(produit)
        self.mock_cursor.close.assert_called_once()
        
    def test_find_by_id_database_error(self):
        """Test de gestion d'erreur de base de données"""
        # Configuration du mock pour lever une exception
        self.mock_cursor.execute.side_effect = Error("Erreur de connexion")
        
        # Appel de la méthode
        with patch('builtins.print') as mock_print:
            produit = Produit.find_by_id(self.mock_connection, 1)
            
        # Vérifications
        self.assertIsNone(produit)
        mock_print.assert_called_once()
        self.mock_cursor.close.assert_called_once()
        
    def test_find_by_id_missing_optional_fields(self):
        """Test avec des champs optionnels manquants"""
        data_without_optional = {
            'id_p': 1,
            'type_p': 'Électronique',
            'designation_p': 'Smartphone',
            'prix_ht': 299.99,
            'stock_p': 50
            # date_in et timeS_in manquants
        }
        
        self.mock_cursor.fetchone.return_value = data_without_optional
        
        produit = Produit.find_by_id(self.mock_connection, 1)
        
        self.assertIsNotNone(produit)
        self.assertIsNone(produit.date_in)
        self.assertIsNone(produit.timeS_in)


class TestProduitFindAll(TestProduit):
    """Tests pour la méthode find_all"""
    
    def test_find_all_success(self):
        """Test de récupération de tous les produits"""
        # Configuration du mock
        produits_data = [
            self.produit_data,
            {
                'id_p': 2,
                'type_p': 'Livre',
                'designation_p': 'Guide Python',
                'prix_ht': 29.99,
                'date_in': date(2025, 10, 1),
                'timeS_in': '2025-10-01 10:00:00',
                'stock_p': 20
            }
        ]
        self.mock_cursor.fetchall.return_value = produits_data
        
        # Appel de la méthode
        produits = Produit.find_all(self.mock_connection)
        
        # Vérifications
        self.assertEqual(len(produits), 2)
        self.assertEqual(produits[0].id_p, 1)
        self.assertEqual(produits[1].id_p, 2)
        self.assertEqual(produits[0].type_p, 'Électronique')
        self.assertEqual(produits[1].type_p, 'Livre')
        
        # Vérification des appels
        self.mock_cursor.execute.assert_called_once_with('SELECT * FROM `produit`')
        self.mock_cursor.close.assert_called_once()
        
    def test_find_all_empty_result(self):
        """Test avec aucun produit en base"""
        # Configuration du mock
        self.mock_cursor.fetchall.return_value = []
        
        # Appel de la méthode
        produits = Produit.find_all(self.mock_connection)
        
        # Vérifications
        self.assertEqual(len(produits), 0)
        self.assertIsInstance(produits, list)
        
    def test_find_all_database_error(self):
        """Test de gestion d'erreur de base de données"""
        # Configuration du mock pour lever une exception
        self.mock_cursor.execute.side_effect = Error("Erreur de connexion")
        
        # Appel de la méthode
        with patch('builtins.print') as mock_print:
            produits = Produit.find_all(self.mock_connection)
            
        # Vérifications
        self.assertEqual(len(produits), 0)
        mock_print.assert_called_once()
        self.mock_cursor.close.assert_called_once()


class TestProduitFindByType(TestProduit):
    """Tests pour la méthode find_by_type"""
    
    def test_find_by_type_success(self):
        """Test de recherche par type réussie"""
        # Configuration du mock
        produits_electronique = [
            self.produit_data,
            {
                'id_p': 3,
                'type_p': 'Électronique',
                'designation_p': 'Casque audio',
                'prix_ht': 59.99,
                'date_in': date(2025, 10, 1),
                'timeS_in': '2025-10-01 14:00:00',
                'stock_p': 30
            }
        ]
        self.mock_cursor.fetchall.return_value = produits_electronique
        
        # Appel de la méthode
        produits = Produit.find_by_type(self.mock_connection, 'Électronique')
        
        # Vérifications
        self.assertEqual(len(produits), 2)
        for produit in produits:
            self.assertEqual(produit.type_p, 'Électronique')
            
        # Vérification des appels
        self.mock_cursor.execute.assert_called_once_with(
            'SELECT * FROM `produit` WHERE type_p = %s',
            ('Électronique',)
        )
        
    def test_find_by_type_no_results(self):
        """Test de recherche par type sans résultats"""
        # Configuration du mock
        self.mock_cursor.fetchall.return_value = []
        
        # Appel de la méthode
        produits = Produit.find_by_type(self.mock_connection, 'TypeInexistant')
        
        # Vérifications
        self.assertEqual(len(produits), 0)
        
    def test_find_by_type_database_error(self):
        """Test de gestion d'erreur de base de données"""
        # Configuration du mock pour lever une exception
        self.mock_cursor.execute.side_effect = Error("Erreur de connexion")
        
        # Appel de la méthode
        with patch('builtins.print') as mock_print:
            produits = Produit.find_by_type(self.mock_connection, 'Électronique')
            
        # Vérifications
        self.assertEqual(len(produits), 0)
        mock_print.assert_called_once()


class TestProduitSave(TestProduit):
    """Tests pour la méthode save"""
    
    def test_save_new_produit_success(self):
        """Test de sauvegarde d'un nouveau produit"""
        # Configuration du mock
        self.mock_cursor.rowcount = 1
        self.mock_cursor.lastrowid = 42
        
        # Création d'un nouveau produit
        produit = Produit(
            type_p="Livre",
            designation_p="Guide Python",
            prix_ht=29.99,
            date_in=date(2025, 10, 2),
            stock_p=10
        )
        
        # Appel de la méthode
        result = produit.save(self.mock_connection)
        
        # Vérifications
        self.assertTrue(result)
        self.assertEqual(produit.id_p, 42)  # L'ID doit être assigné
        
        # Vérification des appels
        self.mock_cursor.execute.assert_called_once_with(
            'INSERT INTO `produit` (type_p, designation_p, prix_ht, date_in, stock_p) VALUES (%s, %s, %s, %s, %s)',
            ("Livre", "Guide Python", 29.99, date(2025, 10, 2), 10)
        )
        self.mock_connection.commit.assert_called_once()
        
    def test_save_existing_produit_success(self):
        """Test de mise à jour d'un produit existant"""
        # Création d'un produit existant
        produit = Produit(
            id_p=1,
            type_p="Livre",
            designation_p="Guide Python Avancé",
            prix_ht=39.99,
            date_in=date(2025, 10, 2),
            stock_p=15
        )
        
        # Appel de la méthode
        result = produit.save(self.mock_connection)
        
        # Vérifications
        self.assertTrue(result)
        
        # Vérification des appels
        self.mock_cursor.execute.assert_called_once_with(
            'UPDATE `produit` SET type_p = %s, designation_p = %s, prix_ht = %s, date_in = %s, stock_p = %s WHERE id_p = %s',
            ("Livre", "Guide Python Avancé", 39.99, date(2025, 10, 2), 15, 1)
        )
        self.mock_connection.commit.assert_called_once()
        
    def test_save_new_produit_no_affected_rows(self):
        """Test d'échec de sauvegarde (aucune ligne affectée)"""
        # Configuration du mock
        self.mock_cursor.rowcount = 0
        
        # Création d'un nouveau produit
        produit = Produit(type_p="Test", designation_p="Test", prix_ht=10.0)
        
        # Appel de la méthode
        result = produit.save(self.mock_connection)
        
        # Vérifications
        self.assertFalse(result)
        self.assertIsNone(produit.id_p)  # L'ID ne doit pas être assigné
        
    def test_save_database_error(self):
        """Test de gestion d'erreur de base de données"""
        # Configuration du mock pour lever une exception
        self.mock_cursor.execute.side_effect = Error("Erreur de sauvegarde")
        
        # Création d'un produit
        produit = Produit(type_p="Test", designation_p="Test", prix_ht=10.0)
        
        # Appel de la méthode
        with patch('builtins.print') as mock_print:
            result = produit.save(self.mock_connection)
            
        # Vérifications
        self.assertFalse(result)
        mock_print.assert_called_once()
        self.mock_connection.rollback.assert_called_once()
        self.mock_cursor.close.assert_called_once()


class TestProduitToDict(TestProduit):
    """Tests pour la méthode to_dict"""
    
    def test_to_dict_complete(self):
        """Test de conversion en dictionnaire avec tous les champs"""
        produit = Produit(
            id_p=1,
            type_p="Électronique",
            designation_p="Smartphone",
            prix_ht=299.99,
            date_in=date(2025, 10, 2),
            timeS_in="2025-10-02 15:30:00",
            stock_p=50
        )
        
        expected_dict = {
            "id_p": 1,
            "type_p": "Électronique",
            "designation_p": "Smartphone",
            "prix_ht": 299.99,
            "date_in": date(2025, 10, 2),
            "timeS_in": "2025-10-02 15:30:00",
            "stock_p": 50
        }
        
        result = produit.to_dict()
        self.assertEqual(result, expected_dict)
        
    def test_to_dict_minimal(self):
        """Test de conversion en dictionnaire avec les valeurs par défaut"""
        produit = Produit()
        
        expected_dict = {
            "id_p": None,
            "type_p": "",
            "designation_p": "",
            "prix_ht": 0.0,
            "date_in": None,
            "timeS_in": None,
            "stock_p": 0
        }
        
        result = produit.to_dict()
        self.assertEqual(result, expected_dict)


class TestProduitRepr(TestProduit):
    """Tests pour la méthode __repr__"""
    
    def test_repr_complete(self):
        """Test de la représentation string complète"""
        produit = Produit(
            id_p=1,
            type_p="Électronique",
            designation_p="Smartphone",
            prix_ht=299.99,
            stock_p=50
        )
        
        expected_repr = "Produit(id=1, type='Électronique', designation='Smartphone', prix_ht=299.99, stock=50)"
        result = repr(produit)
        self.assertEqual(result, expected_repr)
        
    def test_repr_minimal(self):
        """Test de la représentation string avec valeurs par défaut"""
        produit = Produit()
        
        expected_repr = "Produit(id=None, type='', designation='', prix_ht=0.0, stock=0)"
        result = repr(produit)
        self.assertEqual(result, expected_repr)


class TestProduitIntegration(TestProduit):
    """Tests d'intégration pour les cas d'usage complets"""
    
    def test_workflow_create_and_save(self):
        """Test du workflow complet de création et sauvegarde"""
        # Configuration du mock pour la sauvegarde
        self.mock_cursor.rowcount = 1
        self.mock_cursor.lastrowid = 100
        
        # Création d'un produit
        produit = Produit(
            type_p="Papeterie",
            designation_p="Cahier A4",
            prix_ht=4.50,
            date_in=date(2025, 10, 2),
            stock_p=25
        )
        
        # Sauvegarde
        save_result = produit.save(self.mock_connection)
        
        # Vérifications
        self.assertTrue(save_result)
        self.assertEqual(produit.id_p, 100)
        
        # Test de conversion en dict après sauvegarde
        dict_result = produit.to_dict()
        self.assertEqual(dict_result['id_p'], 100)
        self.assertEqual(dict_result['type_p'], "Papeterie")
        
    def test_workflow_find_and_update(self):
        """Test du workflow de recherche et mise à jour"""
        # Configuration du mock pour find_by_id
        self.mock_cursor.fetchone.return_value = self.produit_data
        
        # Recherche du produit
        produit = Produit.find_by_id(self.mock_connection, 1)
        self.assertIsNotNone(produit)
        
        # Modification du produit
        produit.stock_p = 75
        produit.prix_ht = 319.99
        
        # Reset du mock pour la sauvegarde
        self.mock_cursor.reset_mock()
        self.mock_connection.reset_mock()
        
        # Sauvegarde des modifications
        save_result = produit.save(self.mock_connection)
        self.assertTrue(save_result)
        
        # Vérification de l'appel de mise à jour
        self.mock_cursor.execute.assert_called_once_with(
            'UPDATE `produit` SET type_p = %s, designation_p = %s, prix_ht = %s, date_in = %s, stock_p = %s WHERE id_p = %s',
            ('Électronique', 'Smartphone', 319.99, date(2025, 10, 2), 75, 1)
        )


# Point d'entrée pour exécuter les tests
if __name__ == '__main__':
    # Configuration pour un affichage détaillé des tests
    unittest.main(verbosity=2)