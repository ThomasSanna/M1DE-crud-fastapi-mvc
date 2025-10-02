-- Création de la base de données MySQL (si elle n'existe pas)
CREATE DATABASE IF NOT EXISTS `2025_M1` 
DEFAULT CHARACTER SET utf8mb4 
DEFAULT COLLATE utf8mb4_unicode_ci;

USE `2025_M1`;

-- Création de la table user avec syntaxe MySQL correcte
CREATE TABLE IF NOT EXISTS `user` (
    `user_id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_login` VARCHAR(255) NOT NULL UNIQUE,
    `user_password` TEXT NOT NULL,
    `user_compte_id` INT NOT NULL UNIQUE,
    `user_mail` VARCHAR(320) NOT NULL UNIQUE,
    `user_date_new` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `user_date_login` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Index pour optimiser les recherches
    INDEX `idx_user_login` (`user_login`),
    INDEX `idx_user_mail` (`user_mail`),
    
    -- Contrainte unique nommée
    CONSTRAINT `uk_user_compte_id` UNIQUE (`user_compte_id`)
) ENGINE=InnoDB 
DEFAULT CHARSET=utf8mb4 
COLLATE=utf8mb4_unicode_ci; 