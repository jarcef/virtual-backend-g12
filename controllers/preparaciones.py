from flask_restful import Resource, request
from models.preparaciones import Preparacion
from dtos.preparacion_dto import PreparacionRequestDTO, PreparacionResponseDTO
from config import conexion

class PreparacionesController(Resource):
    def post(self):
        try:
            body = request.get_json()
            data = PreparacionRequestDTO().load(body)
            print(data)
            nuevaPreparacion = Preparacion(**data)
            conexion.session.add(nuevaPreparacion)
            conexion.session.commit()
            #dump convierte una instancia a un diccionario
            respuesta = PreparacionResponseDTO().dump(nuevaPreparacion)

            return {
                'message': 'Preparacion creada exitosamente',
                'preparacion': respuesta
            }, 201

        except Exception as e:
            conexion.session.rollback()
            return{
                'message': 'Hubo un error al crear la preparación',
                'content': e.args
            }, 400

    def get(self):
        preparacion: Preparacion | None =  conexion.session.query(Preparacion).filter_by(id=1).first()
        print(preparacion)
        print(preparacion.orden)
        # desde ka oreoaracion podemos ingresar mediante su relationship el registro el cual pertenece esta preparacion y luego a los atributos de esa tabla (modelo)
        print(preparacion.receta.nombre)
        print(preparacion.receta_id)
        return {
            'message': 'ok' 
        }