from flask_restful import Resource, request
from models.recetas import Receta
from dtos.receta_dto import  (RecetaRequestDTO, 
                                RecetaResponseDTO, 
                                BuscarRecetaRequestDTO, 
                                RecetaPreparacionesResponseDTO)
from dtos.paginacion_dto import PaginacionRequestDTO
from config import conexion
from math import ceil

class RecetasController(Resource):
    def post(self):
        body = request.get_json()
        try:
            data = RecetaRequestDTO().load(body)
            nuevaReceta = Receta(
                nombre = data.get('nombre'), 
                estado = data.get('estado'), 
                comensales = data.get('comensales'), 
                duracion = data.get('duracion'),
                dificultad = data.get('dificultad')
            )
            
            conexion.session.add(nuevaReceta)
            conexion.session.commit()
            respuesta = RecetaResponseDTO().dump(nuevaReceta)
            return {
                'message': 'Receta creada exitosamente',
                'content': respuesta
            }, 201
        except Exception as e:
            conexion.session.rollback()
            return {
                'message': 'Error al crear la receta',
                'content': e.args
            }
    
    def get(self):
        query_params = request.args
        paginacion = PaginacionRequestDTO().load(query_params)
        perPage = paginacion.get('perPage')
        page = paginacion.get('page')

        if(perPage < 1 or page < 1):
            return {
                'message': 'Los parametros no pueden recibir valores negativos'
            },400

        skip = perPage * (page - 1)
        recetas = conexion.session.query(Receta).limit(perPage).offset(skip).all()
        total = conexion.session.query(Receta).count()

        itemsXPage= perPage if total >= perPage else total
        totalPages = ceil(total / itemsXPage) if itemsXPage > 0 else None
        prevPage = page - 1 if page > 1 and page <= totalPages else None
        nextPage = page + 1 if totalPages > 1 and page < totalPages else None
      
        respuesta = RecetaResponseDTO(many=True).dump(recetas)
        return {
            'message': 'Las recetas son:',
            'pagination':{
                'total': total,
                'itemsXPage': itemsXPage,
                'totalPages': totalPages,
                'prevPage': prevPage,
                'nextPage': nextPage
            },
            'content': respuesta
        }

class BuscarRecetaController(Resource):
    def get(self):
        query_params = request.args
        try:
       # print(query_params.get('nombre'))
     #   nombre_a_buscar = query_params.get('nombre')
      #  if nombre_a_buscar:        
            parametros = BuscarRecetaRequestDTO().load(query_params)
         #   print(parametros)
            recetas2 = conexion.session.query(Receta).filter(Receta.nombre =='a',Receta.estado==True).all()
        #    print(recetas2)
            nombre = parametros.get('nombre','')

            if parametros.get('nombre') is not None:
                del parametros['nombre']
                
            recetas = conexion.session.query(Receta).filter(Receta.nombre.like('%{}%'.format(nombre))).filter_by(**parametros).all()
            resultado = RecetaResponseDTO(many=True).dump(recetas)
         #   print(recetas)
            return {
                'message':'',
                'content': resultado
            }
        except Exception as e:
            return {
                'message': 'Error al hacer la busqueda',
                'content': e.args
            },400

        
class RecetaController(Resource):
    def get(self, id):
        #buscar la receta segun su id 
        #si no hay la receta devolver un mensaje:'Receta no encontrada' con un estado NOT FOUND
        #Si hay la re ceta devolver message:  'Receta encontrada' con un estado OK
        receta: Receta | None = conexion.session.query(Receta).filter(Receta.id == id).first()
        if receta is None:
            return{
                'message': 'Receta no encontrada'
            },404
        else:
            print(receta.preparaciones)
            respuesta = RecetaPreparacionesResponseDTO().dump(receta)
            return {
                'message': 'Receta encontrada',
                'content': respuesta
            }, 200