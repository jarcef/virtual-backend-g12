from django.db import models

class Etiqueta(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False)
    nombre = models.CharField(max_length=20, unique=True, null=False)

    createAt = models.DateTimeField(auto_now_add=True, db_column='created_at')
    updateAt = models.DateTimeField(auto_now=True, db_column='updated_at')

    class Meta:
        db_table = 'etiquetas'
        ordering = ['-nombre']
