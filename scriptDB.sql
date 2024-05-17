DROP DATABASE IF EXISTS bd_api_persons;
CREATE DATABASE bd_api_persons CHARSET utf8mb4;
USE bd_api_persons;

CREATE TABLE DocumentType (
    DocumentTypeId INT PRIMARY KEY,
    description VARCHAR(20) NOT NULL
);

CREATE TABLE Person (
    personId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    documentTypeId INT,
    documentNumber VARCHAR(12) NOT NULL,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    secondLastName VARCHAR(50),
    gender ENUM('masculino', 'femenino', 'otros') NOT NULL,
    maritalStatus ENUM('soltero', 'casado', 'divorciado', 'viudo') NOT NULL,
    birthdate DATE NOT NULL,
    isCustomer BOOLEAN,
    FOREIGN KEY (documentTypeId) REFERENCES DocumentType(DocumentTypeId)
);

CREATE TABLE Phone (
    personId INT,
    phoneNumber INT,
    FOREIGN KEY (personId) REFERENCES Person(personId)
);

CREATE TABLE Address (
    personId INT,
    addressTypeCode INT,
    addressTypeDescription VARCHAR(255),
    PRIMARY KEY (personId, addressTypeCode),
    FOREIGN KEY (personId) REFERENCES Person(personId)
);

CREATE TABLE Email (
    personId INT,
    email VARCHAR(255),
    FOREIGN KEY (personId) REFERENCES Person(personId)
);