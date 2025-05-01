-- create.sql
-- Password Manager Project – single-user schema for “padlock” DB

CREATE DATABASE IF NOT EXISTS `Padlock`
  DEFAULT CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;
USE `Padlock`;

DROP TABLE IF EXISTS vault_entries;
DROP TABLE IF EXISTS master_credentials;

CREATE TABLE master_credentials (
    id           TINYINT       PRIMARY KEY,         
    master_salt  VARBINARY(16) NOT NULL,            
    master_hash  VARBINARY(64) NOT NULL,            
    created_at   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE vault_entries (
    id             INT            PRIMARY KEY AUTO_INCREMENT,
    site           VARCHAR(255)   NOT NULL,         
    login          VARCHAR(255)   NOT NULL,         
    password_blob  VARBINARY(512) NOT NULL,         
    iv             VARBINARY(16)  NOT NULL,         
    created_at     DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP 
                                         ON UPDATE CURRENT_TIMESTAMP
);
