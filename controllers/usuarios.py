from flask_restful import Resource, request
from dtos.registro_dto import RegistroDTO, UsuarioResponseDTO, LoginDTO
from models.usuarios import Usuario
from config import conexion

class RegistroController(Resource):
    def post(self):
        body = request.get_json()       
        try:
            data = RegistroDTO().load(body)
            nuevoUsuario = Usuario(**data)
            nuevoUsuario.encriptar_pwd()
            conexion.session.add(nuevoUsuario)
            conexion.session.commit()
            respuesta = UsuarioResponseDTO().dump(nuevoUsuario)
            return {
                'message': 'Usuario registrado exitosamente',
                'content': respuesta
            }, 201

        except Exception as e:
            conexion.session.rollback()
            return {
                'message': 'Error al registrar al usuario',
                'content': e.args
            }, 400

class LoginController(Resource):
    def post(self):
        body = request.get_json()
            #Hacer un DTO qe solamente reciba un correo y un password, el correo debe de ser email, no es necesario usar un 
            #SQLAlchemyAutoSchema, solamente un validador  Schema

        try:
            data= LoginDTO().load(body)
            return {
               'message': 'Bienvenido'
            }
        except Exception as e:
            return{
                'message': 'Credenciales incorrectas',
                'content': e.args
            }