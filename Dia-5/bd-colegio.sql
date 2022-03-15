CREATE DATABASE colegios;

USE colegios;

CREATE TABLE IF NOT EXISTS alumnos(
	id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) not null,
    apellido_paterno VARCHAR(45),
    apellido_materno VARCHAR(45),
    correo VARCHAR(45),
    numero_emergencia VARCHAR(20) not null
);

CREATE TABLE IF NOT EXISTS niveles(
	id INT PRIMARY KEY AUTO_INCREMENT,
    seccion VARCHAR(45) not null,
    ubicacion VARCHAR(45),
    nombre VARCHAR(45) not null
);

CREATE TABLE IF NOT EXISTS alumnos_niveles(
	id INT PRIMARY KEY AUTO_INCREMENT,
    fecha_cursada year,
    alumno_id int,
    foreign key (alumno_id) REFERENCES alumnos(id),
    nivel_id int,
    foreign key (nivel_id) REFERENCES niveles(id)
);