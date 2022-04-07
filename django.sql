use agenda

select * from django_migrations

SELECT * FROM agenda.django_migrations;

select * from etiquetas

SELECT * FROM etiquetas as e INNER JOIN tareas_etiquetas as te on e.id = te.etiqueta_id INNER JOIN tareas as t on te.tareas_id = t.id;