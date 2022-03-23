from config import validador
from marshmallow import fields, validate

class ValidadorPrueba(validador.Schema):
    nombre = fields.Str(validate=validate.Length(max=10))
    apellido = fields.Str()
    edad = fields.Int()
    soltero = fields.Bool()

  #  class Meta:
        #es una clase que va hacer para poder pasar parametros a la metadata del padre (de la clase de
        # de la cual estamos heredando), definimos atributos que van a ser a la clase Schema
   #     fields = ['nombre','apellido']
class ValidadorUsuarioPrueba(validador.Schema):
    nombre = fields.Str()
    apellido = fields.Str()