-- Création de la base de données
CREATE DATABASE MariagesDB;
\c MariagesDB; -- Se connecter à la base

-- Table des Départements
CREATE TABLE Departements (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL
);

-- Table des Communes
CREATE TABLE Communes (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    id_departement INTEGER REFERENCES Departements(id) ON DELETE SET NULL
);

-- Table des Personnes
CREATE TABLE Personnes (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    prenom VARCHAR(255) NOT NULL,
    id_pere INTEGER REFERENCES Personnes(id) ON DELETE SET NULL,
    id_mere INTEGER REFERENCES Personnes(id) ON DELETE SET NULL
);

-- Table des Actes
CREATE TABLE Actes (
    id SERIAL PRIMARY KEY,
    id_personneA INTEGER REFERENCES Personnes(id) ON DELETE CASCADE,
    id_personneB INTEGER REFERENCES Personnes(id) ON DELETE CASCADE,
    id_commune INTEGER REFERENCES Communes(id) ON DELETE SET NULL,
    type VARCHAR(255) NOT NULL,
    date DATE,
    num_vue VARCHAR(50)
);
