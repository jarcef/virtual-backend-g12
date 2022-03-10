from flask import Flask, request
from datetime import datetime
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app=app, origins=['http://127.0.0.1:5500','http://127.0.0.1:5501','https://miapp.vercel.app'], methods='*', allow_headers=['Content-Type'])

clientes = [
    {
    "nombre": "Eduardo",
    "pais": "Perú",
    "edad": 29,
    "organos": True,
    "casado": False
    }
]

def buscar_usuario(id):

    for posicion in range(0,len(clientes)):
        cliente = clientes[posicion]
        if cliente.get('id')==id:
            return (cliente,posicion)
    

@app.route('/')
def estado():
    hora_del_servidor = datetime.now()
    return{
        'status': True,
        'hour': hora_del_servidor.strftime('%Y/%m/%d %H:%M:%S')
    }

@app.route('/clientes', methods=['POST','GET'])
@cross_origin(origins=['http://127.0.0.1:7000','http://mipagina.com'])
def obtener_clientes():
    print(request.method)
    print(request.get_json())

    if request.method == 'POST':
        data = request.get_json()
        data['id'] = len(clientes) + 1
     
        clientes.append(data)
        data['nombre']
        return{
            'message': 'Cliente agregado exitosamente',
            'client': data
        }
    else:
        return{
            'message': 'La lista de clientes',
            'clients': clientes
        }

@app.route('/cliente/<int:id>', methods=['GET','PUT','DELETE'])
def gestion_usuario(id):
    print(id)

    if request.method == 'GET':
        resultado = buscar_usuario(id)
        if resultado:
            return resultado[0]
        else:
            return {
                'message': ' el usuario a buscar no se encontro'
            },404

    elif request.method == 'PUT':
        resultado = buscar_usuario(id)
        if resultado is not None:
            [cliente, posicion] = resultado
            data = request.get_json()
            data['id'] = id
         #   posicion = resultado[1]
            clientes[posicion] = data
            return clientes[posicion]           
        else:
            return {
                'message': 'El usuario a buscar no se encontro'
            },404
  
    elif request.method == 'DELETE':
        resultado = buscar_usuario(id)
        if resultado:
            [cliente,posicion] = resultado
            cliente_eliminado = clientes.pop(posicion)
            return {
                'message': 'Cliente eliminado exitosamente',
                'cliente': cliente_eliminado
            }
        else:
            return {
                'message': 'El cliente a eliminar no se encontró'
            }


        #Eliminar ese cliente luego de validar si existe o no usando el metodo validar usuario(id) sino existe indicar lo mismo 'Cliente no existe'

app.run(debug=True)