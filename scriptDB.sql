DROP DATABASE IF EXISTS bd_api_persons;
CREATE DATABASE bd_api_persons CHARSET utf8mb4;
USE bd_api_persons;

CREATE TABLE DocumentType (
    documentTypeId INT PRIMARY KEY,
    documentTypeName VARCHAR(50) NOT NULL
);

CREATE TABLE Person (
    personId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    documentTypeId INT,
    documentNumber VARCHAR(12) NOT NULL,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    secondLastName VARCHAR(50),
    gender ENUM('MALE', 'FEMALE', 'OTHER') NOT NULL,
    maritalStatus ENUM('SINGLE', 'MARRIED', 'DIVORCED', 'WIDOW') NOT NULL,
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
    addressDescription VARCHAR(255),
    PRIMARY KEY (personId, addressTypeCode),
    FOREIGN KEY (personId) REFERENCES Person(personId)
);

CREATE TABLE Email (
    personId INT,
    email VARCHAR(255),
    FOREIGN KEY (personId) REFERENCES Person(personId)
);

-- Insertar tipos de documentos para personas naturales
INSERT INTO DocumentType (documentTypeId, documentTypeName) VALUES (1, 'Singapore National Identity Card (NRIC)');
INSERT INTO DocumentType (documentTypeId, documentTypeName) VALUES (2, 'Singaporean Passport');

-- Insertar tipos de documentos para empresas
INSERT INTO DocumentType (documentTypeId, documentTypeName) VALUES (3, 'Certificate of Incorporation');
INSERT INTO DocumentType (documentTypeId, documentTypeName) VALUES (4, 'Unique Entity Number (UEN)');
INSERT INTO DocumentType (documentTypeId, documentTypeName) VALUES (5, 'Goods and Services Tax Identification (GST)');
commit;
