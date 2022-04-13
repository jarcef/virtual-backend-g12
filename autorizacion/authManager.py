from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, correo, nombre, rol, password):
        """Creación de un usuario sin el comando createsuperuser"""
        if not correo:
            raise ValueError(
                'El usuario deber tener obligatoriamente un correo')

        correo = self.normalize_email(correo)
        nuevoUsuario = self.model(correo=correo, nombre=nombre, rol=rol)
        #set_password > genera un hash de la contraseña usando bcrypt y el algoritmo SHA256
        nuevoUsuario.set_password(password)
        #Sirve para referencia a la base de datos x default en el caso que tengamos varias conexiones a diferentes bases de datos
        nuevoUsuario.save(using=self._db)
        return nuevoUsuario

    def create_superuser(self, correo, nombre, rol, password):
        """Creación de uns super usuario por consola, este metodo mandara a llamar cuando se haga el uso del comando por consola"""
        usuario = self.create_user(correo, nombre, rol, password)
        #is_superuser > indicara que usuarios son super usuarios y podra acceder a todas las funcionalidades del panel administrativo
        usuario.is_superuser = True
        usuario.is_staff = True
        usuario.save(using=self._db)