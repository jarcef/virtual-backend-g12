from flask import Flask
from datetime import datetime
from flask_restful import Api
from controllers.ingredientes import (  IngredientesController, 
                                        PruebaController,
                                        IngredienteController )
from controllers.recetas import ( RecetasController, 
                                BuscarRecetaController,
                                RecetaController)
from controllers.preparaciones import PreparacionesController
from controllers.ingredientes_recetas import IngredientesRecetasController
from config import conexion, validador
from dotenv import load_dotenv

from os import environ

# Carga todas las variables definida en el archivo .env para que sean tratadas como variables de entorno
load_dotenv()

print(environ.get('NOMBRE'))

app = Flask(__name__)
#Creamos la instancia de flask_restful.Api y le indicamos que toda la configuracion que haremos se agregue a nuestra instancia de Flask
api = Api(app=app)

#Ahora asignaremos la cadena de conexion a nuestra base de datos
#                                        tipo://usuario:password@dominio:puerto/base_de_datos
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
# Si se establece True entonces SQLALCHEMY rastreara las modificaciones de los objetos (modelos) y emitira señales cuando cambie
#algun modio
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# para jalar la configuración de mi flask y extraer su conexión a la base de datos
conexion.init_app(app)
validador.init_app(app)

conexion.create_all(app=app)

@app.route('/status', methods=['GET'])

def status():
    return {
        'status': True,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

@app.route('/')
def inicio():
    return 'Bienvenido a mi API de recetas'   

# Ahora definimos las rutas que van a ser utulizadas con un determinado controlador
api.add_resource(IngredientesController,'/ingredientes','/ingrediente')
api.add_resource(PruebaController,'/pruebas')
api.add_resource(IngredienteController,'/ingrediente/<int:id>')
api.add_resource(RecetasController,'/recetas','/receta')
api.add_resource(BuscarRecetaController,'/buscar_receta')
api.add_resource(PreparacionesController, '/preparacion')
api.add_resource(RecetaController, '/receta/<int:id>')
api.add_resource(IngredientesRecetasController,'/ingrediente_receta')


# Comprobará que la instancia de la clase Flask se este ejecutando en el archivo principal del proyecto,
# esto se usa para no crear multiples instancias y generar un posible error de Flask
if __name__ == '__main__':
    app.run(debug=True)

print('hola')
