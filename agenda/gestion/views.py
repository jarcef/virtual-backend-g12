from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import ListAPIView, ListCreateAPIView
from .serializers import PruebaSerializer, TareaSerializer, EtiquetaSerializer
from .models import Tareas, Etiqueta

@api_view(http_method_names=['GET','POST'])
def inicio(request: Request):
    print(request.method)
    print(request)

    if request.method == 'GET':
        return Response(data={
            'message': 'Bienvenido a mi API de agenda'
        })
    
    elif request.method == 'POST':
        return Response(data={
        'message': 'Hiciste un post'
    }, status=201)


class PruebaApiView(ListAPIView):
    serializer_class = PruebaSerializer

    queryset = [{
    'nombre':'Eduardo',
    'apellido':'De Rivero',
    'correo':'ederiv@gmail.com',
    'dni':'73500746',
    'estado_civil':'viudo'},
    {
    'nombre':'Maria',
    'apellido':'Perez',
    'correo':'ederiv@gmail.com',
    'dni':'73501746',
    'estado_civil':'casada'}    
    ]

    def get(self, request: Request):

        informacion = self.queryset
        informacion_serializada = self.serializer_class(data=informacion, many=True)
        informacion_serializada.is_valid(raise_exception=True)
        return Response(data={
            'message':'Hola',
            'content': informacion_serializada.data
            })

class TareasApiView(ListCreateAPIView):
    queryset = Tareas.objects.all() # select * from tareas
    serializer_class= TareaSerializer

class EtiquetasApiView(ListCreateAPIView):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer