CREATE DATABASE prueba;
USE prueba

CREATE TABLE clientes(
	id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    documento VARCHAR(10) UNIQUE,
    tipo_documento ENUM('C.E.','DNI','RUC','PASAPORTE','C.M','OTRO'),
    estado BOOL    
);
