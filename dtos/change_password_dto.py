from config import validador
from marshmallow import fields, validate

class ChangePasswordRequestDTO(validador.Schema):
    token = fields.String(required=True)
    #Falta actualizar la información
    password = fields.String()