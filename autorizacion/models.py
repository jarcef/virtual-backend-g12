from django.db import models
#abstractBaseUser > me permite modificar todo el modelo auth_user desde cero
#abstractUser > me permite agregar nuevas columnas de las que ya estaban creadas inicialmente
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .authManager import UserManager

class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    correo = models.EmailField(unique=True, null=False)
    password = models.TextField(null=False)
    nombre= models.CharField(max_length=45, null=False)
    rol = models.CharField(choices=(
        ['ADMINISTRADOR','ADMINISTRADOR'],
        ['MOZO','MOZO']), max_length=40)
    
    #si quieres seguir utilizando el panel administrativo entonces deberas declarar las siguientes columnas
    #is_staff > indicará si el usuario creado puede acceder o no al panel administrativo (es parte del equipo)
    is_staff = models.BooleanField(default=False)
    #is_active > puede realizar operaciones dentro del panel administrativo, si el usuario no está activo podrá loguearse pero no podrá realizar ninguna acción
    is_active = models.BooleanField(default=True)

    createAT = models.DateTimeField(auto_now_add=True, db_column='created_at')
    #comportamiento que tendrá el modelo cuando se realice el comando createsuperuser
    objects = UserManager()
    #sera el campo que pedira aparte de la password en el panel administrativo para hacer el login
    USERNAME_FIELD = 'correo'
    #seran los atributos que me solicitará por la consola al crear el superusuario, no van los campos especificados en el USERNAME_FIELD y el password
    REQUIRED_FIELDS = ['nombre','rol']

    class Meta:
        db_table = 'usuarios'