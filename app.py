from flask import Flask, render_template, request
from flask_restful import Api
from controllers.usuarios import (RegistroController, 
                                    LoginController,
                                    ResetPasswordController) 
from config import validador, conexion
from os import environ
from dotenv import load_dotenv
from flask_cors import CORS
from dtos.registro_dto import UsuarioResponseDTO
from flask_jwt import JWT, jwt_required, current_identity
from models.usuarios import Usuario
from seguridad import autenticador, identificador
from datetime import timedelta
from seed import categoriaSeed
from controllers.movimientos import MovimientoController
from cryptography.fernet import Fernet
from datetime import datetime
import json

load_dotenv()

app = Flask(__name__)
CORS(app=app)
app.config['SECRET_KEY']= environ.get('JWT_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

@app.before_first_request
def seed():
    categoriaSeed()

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

@app.route('/status')
def estado():
    return {
        'status': True,
        'hora_del_servidor': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }, 200

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

@app.route('/validar-token',methods=['POST'])
def validar_token():
    # TODO: agregar el dto para solamente recibir la token en el body, la token tiene que ser un string
    body = request.get_json()
    token = body.get('token')
    fernet = Fernet(environ.get('FERNET_SECRET_KEY'))
    try:
        data = fernet.decrypt(bytes(token,'utf-8')).decode('utf-8')
        print(data)
        diccionario = json.loads(data)
        fecha_caducidad = datetime.strptime(diccionario.get('fecha_caducidad'),'%Y-%m-%d %H:%M:%S.%f')
        hora_actual = datetime.now()
        if hora_actual <= fecha_caducidad:
         

            print(conexion.session.query(Usuario).with_entities(
                Usuario.correo).filter_by(id=diccionario.get('id_usuario')))            

            #buscar ese usuario en la bd con ese id y retornar al front el nombre del usuario

            usuarioEncontrado = conexion.session.query(Usuario).with_entities(
                Usuario.correo).filter_by(id= diccionario.get('id_usuario')).first()
            if usuarioEncontrado:                
                return {
                    'message': 'Correcto',
                    'content': { 
                        'correo': usuarioEncontrado.correo    
                    }
                }
            else:
                return {
                    'message': 'Usuario no existe'
                }, 400
        else:
            return {
                'message': 'La token caduco'
            }, 400       
    except Exception as e:
        return {
            'message': 'Token incorrecta'
        }, 400

#Falta actualizar la informacion de la tarea
#@app.route('/change-password-token','/')

api.add_resource(RegistroController, '/registro')
api.add_resource(LoginController, '/login')
api.add_resource(MovimientoController,'/movimiento','/movimientos')
api.add_resource(ResetPasswordController, '/reset-password')

if(__name__=='__main__'):
    app.run(debug=True, port=8080)