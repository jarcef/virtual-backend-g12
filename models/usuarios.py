from config import conexion
from sqlalchemy import Column, types
from bcrypt import hashpw, gensalt

class Usuario(conexion.Model):
    __tablename__ = 'usuarios'
    id = Column(type_= types.Integer, primary_key=True, autoincrement=True)
    nombre = Column(type_=types.String(length=45))
    apellido = Column(type_=types.String(length=45))
    correo = Column(type_=types.String(length=45), nullable=False, unique=True)
    password = Column(type_=types.Text(), nullable=False)

    def encriptar_pwd(self):
        password_bytes = bytes(self.password,'utf-8')

        salt = gensalt(rounds=10)
        hash_password = hashpw(password_bytes, salt)

        hash_pwd_string = hash_password.decode('utf-8')

        self.password = hash_pwd_string

        