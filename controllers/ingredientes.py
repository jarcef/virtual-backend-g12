from flask_restful import Resource, request
from config import conexion
from models.ingredientes import Ingrediente
from dtos.dto_prueba import ValidadorPrueba, ValidadorUsuarioPrueba
from dtos.ingrediente_dto import IngredienteRequestDTO, IngredienteResponseDTO
from marshmallow.exceptions import ValidationError

class IngredientesController(Resource):
    def get(self):
        resultado = conexion.session.query(Ingrediente).all()
        print(resultado)
        ingredientesSerializados = IngredienteResponseDTO(many=True).dump(resultado)
        return {
            'message':'Yo soy el get de los ingredientes',
            'content': ingredientesSerializados
            }     
        
    def post(self):
        print(request.get_json())
        data = request.get_json()
    #    validacion = ValidadorPrueba().load(data)
    #    print(validacion)
        # registramos un nuevo ingrediente
        try:       
            data_serializada = IngredienteRequestDTO().load(data)
            print(data_serializada)
            nuevoIngrediente = Ingrediente()
            nuevoIngrediente.nombre = data_serializada.get('nombre')
            #guardo la informacioón en la base de datos
            conexion.session.add(nuevoIngrediente)
            conexion.session.commit()
            ingredienteSerializado = IngredienteResponseDTO().dump(nuevoIngrediente)
            #conexion.session.rollback()
            return {
                'message': 'Ingrediente creado exitosamente',
                'ingrediente': {}
            },201

        except ValidationError as e:
            return {
                'message': 'La información es incorrecta',
                'content': e.args
            }, 400

        except Exception as e:
            print(e.args[0][1])
            conexion.session.rollback()
            return {
                'message': 'Hubo un error al crear el ingrediente',
                'content': e.args[0]
            }, 500

class PruebaController(Resource):
    
    def post(self):
        try:            
            data = request.get_json()
            validacion = ValidadorPrueba().load(data)
           # validacionLongitud = validate.Length(max=10)
           # validacionLongitud(validacion.get('nombre'))
            print(validacion)
            return {
                'message': 'ok',
                'data': validacion
            }
        except Exception as e:
            print(e.args)
            return {
                'message': 'error al recibir los datos',
                'content': e.args
            }

    def get(self):
        usuario = {
            'nombre': 'Eduardo',
            'apellido':'Manrique',
            'nacionalidad': 'Peru',
            'password': 'Mimamamemima123'
        }
        resultado = ValidadorUsuarioPrueba().dump(usuario)
        return {
            'message': 'El usuario es',
            'content': usuario,
            'resultado': resultado
        
        }

class IngredienteController(Resource):
    def get(self,id):
        ingrediente = conexion.session.query(Ingrediente).filter_by(id=id).first()
        print(ingrediente)
        if IngredienteRequestDTO:
            resultado = IngredienteResponseDTO().dump(ingrediente)
            return {
                'id': id,
                'result': resultado
            }
        else:
            return {
                'message': 'El ingrediente a buscar no existe'
            },404
    
    def put(self, id):
        ingrediente = conexion.session.query(Ingrediente).filter_by(id=id).first()
        try:

            if ingrediente:            
                body = request.get_json()
                data_validada = IngredienteResponseDTO().load(body)
                ingrediente.nombre = data_validada.get('nombre')
                conexion.session.commit()
                resultado = IngredienteResponseDTO.dump(ingrediente)
                return {
                    'message': 'Ingrediente actualizado exitosamente',
                    'content': resultado
                }
            else:
                return {
                    'message': 'Ingrediente a actualizar no existe'
                },404
        except Exception as e:
            return {
                'message': 'Error al actualizar el ingrediente',
                'content': e.args
            }, 404

