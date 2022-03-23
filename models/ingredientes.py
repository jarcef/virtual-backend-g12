from operator import le
from config import conexion
from sqlalchemy import Column, types

class Ingrediente(conexion.Model):
    id = Column(type_=types.Integer, primary_key=True, autoincrement=True)
    nombre= Column(type_=types.String(length=45), nullable=False, unique=True)
    
    __tablename__ = 'Ingredientes'