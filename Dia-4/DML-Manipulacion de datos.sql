USE prueba;

INSERT INTO clientes (nombre, documento, tipo_documento, estado) VALUES
					('Eduardo','73500746', 'DNI', true);
                    
INSERT INTO clientes (nombre, documento, tipo_documento, estado) VALUES
					('Estefani','15945675','DNI',true),
                    ('Fabian','1594987896','RUC',false);
                    
select nombre, documento from clientes

select * from clientes

select * from clientes where documento = '73500746' and (nombre = 'Eduardo' or nombre = 'Estefani')
select estado from clientes

select * from clientes where tipo_documento='DNI' and estado = true

SELECT * FROM clientes 	WHERE nombre LIKE 'Edu%o';

UPDATE clientes SET nombre = 'Ramiro', documento = '33333568' where id=1 AND nombre ='Eduardo';

DELETE from clientes where id = 1;
