-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : jeu. 02 oct. 2025 à 15:01
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `2025_m1`
--

-- --------------------------------------------------------

--
-- Structure de la table `produit`
--

CREATE TABLE `produit` (
  `id_p` int(11) NOT NULL,
  `type_p` varchar(100) NOT NULL,
  `designation_p` varchar(255) NOT NULL,
  `prix_ht` decimal(10,2) NOT NULL,
  `date_in` date NOT NULL,
  `timeS_in` timestamp NOT NULL DEFAULT current_timestamp(),
  `stock_p` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `produit`
--

INSERT INTO `produit` (`id_p`, `type_p`, `designation_p`, `prix_ht`, `date_in`, `timeS_in`, `stock_p`) VALUES
(6, 'Électronique', 'Casque audio Bluetooth', 59.99, '2025-10-01', '2025-10-02 12:00:56', 25),
(7, 'Alimentation', 'Café en grains 1kg', 12.50, '2025-09-28', '2025-10-02 12:00:56', 100),
(8, 'Papeterie', 'Carnet A5', 3.20, '2025-09-30', '2025-10-02 12:00:56', 50),
(9, 'Électronique', 'Chargeur USB-C', 19.90, '2025-10-01', '2025-10-02 12:00:56', 40),
(10, 'Meubles', 'Chaise de bureau ergonomique', 89.99, '2025-09-25', '2025-10-02 12:00:56', 15),
(11, 'Électronique', 'Clé USB 64GB', 14.99, '2025-10-02', '2025-10-02 12:00:56', 80),
(12, 'Alimentation', 'Thé vert 100g', 5.50, '2025-09-29', '2025-10-02 12:00:56', 120),
(13, 'Papeterie', 'Stylo bille noir', 1.50, '2025-09-27', '2025-10-02 12:00:56', 200),
(14, 'Électronique', 'Écran LED 24 pouces', 129.99, '2025-10-01', '2025-10-02 12:00:56', 10),
(15, 'Meubles', 'Table basse bois', 149.99, '2025-09-26', '2025-10-02 12:00:56', 8),
(16, 'Alimentation', 'Pâtes 500g', 2.20, '2025-09-30', '2025-10-02 12:00:56', 300),
(17, 'Papeterie', 'Classeur A4', 4.50, '2025-09-28', '2025-10-02 12:00:56', 75),
(18, 'Électronique', 'Souris sans fil', 25.00, '2025-10-02', '2025-10-02 12:00:56', 60),
(19, 'Meubles', 'Fauteuil relax', 199.99, '2025-09-24', '2025-10-02 12:00:56', 5),
(20, 'Alimentation', 'Huile d\'olive 1L', 8.99, '2025-09-29', '2025-10-02 12:00:56', 50),
(21, 'Papeterie', 'Bloc-notes autocollant', 2.50, '2025-09-27', '2025-10-02 12:00:56', 150),
(22, 'Électronique', 'Casque gaming RGB', 89.99, '2025-10-01', '2025-10-02 12:00:56', 30),
(23, 'Meubles', 'Bibliothèque 3 étagères', 129.99, '2025-09-25', '2025-10-02 12:00:56', 12),
(24, 'Alimentation', 'Chocolat noir 200g', 3.99, '2025-09-28', '2025-10-02 12:00:56', 80),
(25, 'Papeterie', 'Marqueurs couleur', 6.50, '2025-09-30', '2025-10-02 12:00:56', 90),
(26, 'Électronique', 'Enceinte Bluetooth', 49.99, '2025-10-02', '2025-10-02 12:00:56', 35),
(27, 'Meubles', 'Lit simple 90x200', 179.99, '2025-09-26', '2025-10-02 12:00:56', 7),
(28, 'Alimentation', 'Jus d\'orange 1L', 2.50, '2025-09-29', '2025-10-02 12:00:56', 100),
(29, 'Papeterie', 'Agrafeuse métallique', 9.99, '2025-09-27', '2025-10-02 12:00:56', 45),
(30, 'Électronique', 'Webcam HD', 39.99, '2025-10-01', '2025-10-02 12:00:56', 20),
(31, 'Meubles', 'Armoire 2 portes', 249.99, '2025-09-24', '2025-10-02 12:00:56', 6);

-- --------------------------------------------------------

--
-- Structure de la table `user`
--

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `user_login` text NOT NULL,
  `user_password` longtext NOT NULL,
  `user_compte_id` int(11) DEFAULT NULL,
  `user_mail` text NOT NULL,
  `user_date_new` timestamp NOT NULL DEFAULT current_timestamp(),
  `user_date_login` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `user`
--

INSERT INTO `user` (`user_id`, `user_login`, `user_password`, `user_compte_id`, `user_mail`, `user_date_new`, `user_date_login`) VALUES
(1, 'mm', '$2y$10$H24g8xOaVuEjbzN6C/hRg.06nddThXBynRWRSrbapZnK21zHY7pvW', NULL, 'mm@gmail.com', '2025-09-23 18:34:28', '2025-09-23 18:34:28'),
(3, 'testest', '$2b$12$EKBe1dEnN4ggMoKV9uVUVugDEyxMV6JjMCj6QDO0p1ay826Xq9IQy', 3, 'test@gmail.com', '2025-10-02 08:35:56', '2025-10-02 12:23:04'),
(7, 'hjddksjdh', '$2b$12$p7tVtno65of8TbICJT4/h.qi7hKkTgvdZotBXGBaU7RrC66.QWFoe', NULL, 'shkj@dshjsdk.com', '2025-10-02 08:54:05', '2025-10-02 08:54:05');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `produit`
--
ALTER TABLE `produit`
  ADD PRIMARY KEY (`id_p`);

--
-- Index pour la table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `cle-etrangere` (`user_compte_id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `produit`
--
ALTER TABLE `produit`
  MODIFY `id_p` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT pour la table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
