from config import validador
from models.usuarios import Usuario
from marshmallow_sqlalchemy import auto_field
from marshmallow import validate, fields
class RegistroDTO(validador.SQLAlchemyAutoSchema):
    correo = auto_field(validate = validate.Email())
    class Meta:
        model = Usuario

class UsuarioResponseDTO(validador.SQLAlchemyAutoSchema):
    password = auto_field(load_only=True)
    class Meta:
        model = Usuario

class LoginDTO(validador.Schema):
    correo = fields.Email()
    password = fields.String()