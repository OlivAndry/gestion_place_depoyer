CREATE DATABASE IF NOT EXISTS invitation;
USE invitation;

CREATE TABLE invitee (
    id_inv INT AUTO_INCREMENT PRIMARY KEY,
    nom_prenoms VARCHAR(255),
    famille VARCHAR(100),
    nb_personnes INT
);

CREATE TABLE table_salle (
    id_table INT AUTO_INCREMENT PRIMARY KEY,
    num_table VARCHAR(50),
    nom_table VARCHAR(50),
    capacite INT,
    localisation VARCHAR(100)
);

CREATE TABLE placement (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_inv INT,
    id_table INT,
    nb_personnes INT,
    place_restant INT,
    FOREIGN KEY (id_inv) REFERENCES invitee(id_inv),
    FOREIGN KEY (id_table) REFERENCES table_salle(id_table)
);

