-- JOINS
USE prueba;

SELECT * 
FROM VACUNATORIOS INNER JOIN VACUNAS ON VACUNATORIOS.vacuna_id = VACUNAS.id 
WHERE vacuna_id = 1;



SELECT *
FROM VACUNATORIOS LEFT JOIN VACUNAS ON VACUNATORIOS.vacuna_id = VACUNAS.id;

INSERT INTO vacunatorios (nombre, latitud, longitud, direccion, horario_atencion, foto, vacuna_id) VALUES 
('POSTA JOSE GALVEZ', 14.26598, 32.2569, 'AV. EL SOL 755', 'LUN-VIE 15:00 22:00', null, null);

SELECT *
FROM VACUNATORIOS right JOIN VACUNAS ON VACUNATORIOS.vacuna_id = VACUNAS.id;



SELECT *
FROM VACUNATORIOS LEFT JOIN VACUNAS ON VACUNATORIOS.vacuna_id = VACUNAS.id;
UNION
SELECT *
FROM VACUNATORIOS right JOIN VACUNAS ON VACUNATORIOS.vacuna_id = VACUNAS.id;

SELECT vacu.nombre, vac.nombre 
FROM VACUNATORIOS vac JOIN VACUNAS vacu ON vac.vacuna_id = vacu.id
WHERE vacu.nombre = 'Pfizer';


select * from vacunatorios


select * from vacunas

SELECT * FROM VACUNATORIOS vt join VACUNAS vc on vt.vacuna_id = vc.id where vc.nombre = 'SINOPHARM'

SELECT * FROM VACUNATORIOS vt join VACUNAS vc on vt.vacuna_id = vc.id
WHERE vt.latitud between -5.00 and 10.00

SELECT vc.nombre, procedencia FROM VACUNATORIOS vt right join VACUNAS vc on vt.vacuna_id = vc.id
where vacuna_id is null

