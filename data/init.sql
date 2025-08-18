CREATE DATABASE cantonese;
ALTER DATABASE cantonese CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE cantonese;

CREATE TABLE lexicon (
    id INT NOT NULL AUTO_INCREMENT,
    `character` NVARCHAR(10) NOT NULL,  -- Chinese character
    pos VARCHAR(30),                     -- part of speech
    romanization NVARCHAR(10),           -- Jyutping romanization
    onset NVARCHAR(5),
    nucleus NVARCHAR(5),
    coda NVARCHAR(5),
    tone NVARCHAR(2),
    eng_tran NVARCHAR(255),              -- English translation
    CONSTRAINT PRIMARY KEY (id)
);
