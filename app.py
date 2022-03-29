from flask import Flask, render_template
from flask_restful import Api
from controllers.usuarios import RegistroController, LoginController, UsuarioResponseDTO
from config import validador, conexion
from os import environ
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt import JWT, jwt_required, current_identity
from seguridad import autenticador, identificador
from datetime import timedelta

load_dotenv()

app = Flask(__name__)
CORS(app=app)
app.config['SECRET_KEY']= 'secreto'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['JWT_AUTH_URL_RULE']='/login-jwt'
app.config['JWT_AUTH_USERNAME_KEY']='correo'
app.config['JWT_AUTH_PASSWORD_KEY']='pass'
app.config['JWT_EXPIRATION_DELTA']= timedelta(hours=1, minutes=5)
app.config['JWT_AUTH_HEADER_PREFIX']='Bearer'

jsonwebtoken = JWT(app=app, authentication_handler=autenticador,identity_handler=identificador)

api = Api(app=app)
validador.init_app(app)
conexion.init_app(app)

conexion.create_all(app=app)

@app.route('/')
def inicio():
    return render_template('inicio.jinja', nombre='Julissa', dia='Jueves', integrantes=[
        'Foca',
        'Lapagol',
        'Ruizdiaz',
        'Paolin',
        'Rayo Advincula'
    ], usuario= {
        'nombre':'Juan',
        'direccion': 'Las piedritas 105',
        'edad':'40'
    }, selecciones = [{
        'nombre': 'Bolivia',
        'clasificado': False
    },{
        'nombre': 'Brasil',
        'clasificado': True
    },{
        'nombre': 'Chile',
        'clasificado': False
    },{
        'nombre': 'Peru',
        'clasificado': True    
    }])

@app.route('/yo')
@jwt_required()
def perfil_usuario():
    print(current_identity)
    #serializar el usuario (current identity)
    # usuarioResponseDTO()
    usuario = UsuarioResponseDTO().dump(current_identity)
    return {
        'message': 'El usuario es',
        'content': usuario
    }

api.add_resource(RegistroController, '/registro')
api.add_resource(LoginController, '/login')

if(__name__=='__main__'):
    app.run(debug=True, port=8080)