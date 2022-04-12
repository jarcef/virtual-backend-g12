from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import (ListAPIView, 
                                     ListCreateAPIView, 
                                     RetrieveUpdateDestroyAPIView, 
                                     CreateAPIView,
                                     DestroyAPIView)
from .serializers import (PruebaSerializer, TareaSerializer, EtiquetaSerializer, TareasSerializer, TareaPersonalizableSerializer, ArchivoSerializer, EliminarArchivoSerializer)
from .models import Tareas, Etiqueta
from rest_framework import status
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from os import remove
from django.conf import settings

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
    serializer_class= TareasSerializer

    def post(self, request: Request):
        serializador = self.serializer_class(data=request.data)

        if serializador.is_valid():
            
            fechaCaducidad = serializador.validated_data.get('fecha_caducidad')
            print(type(serializador.validated_data.get('fecha_caducidad')))

            importancia = serializador.validated_data.get('importancia')
            if importancia < 0 or importancia > 10:
                return Response(data={
                    'message':'La importancia puede ser entre 0 y 10'
                }, status=status.HTTP_400_BAD_REQUEST)

            if timezone.now() > fechaCaducidad:
                return Response(data={
                        'message': 'La fecha no puede ser menor que la fecha actual'
                },status=status.HTTP_400_BAD_REQUEST)
            serializador.save()           
            return Response(data=serializador.data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={
                'message':'La data no es válida',
                'content': serializador.errors},
                status=status.HTTP_400_BAD_REQUEST)
            
class EtiquetasApiView(ListCreateAPIView):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer

class TareaApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = TareaSerializer
    queryset = Tareas.objects.all()


class ArchivosApiView(CreateAPIView):
    serializer_class = ArchivoSerializer
    def post(self, request: Request):
        print(request.FILES)

        queryParams = request.query_params
        carpetaDestino = queryParams.get('carpeta')

        data = self.serializer_class(data=request.FILES)
        if data.is_valid():
            print(data.validated_data.get('archivo'))
            archivo: InMemoryUploadedFile = data.validated_data.get('archivo')
            print(archivo.size)

            if archivo.size > (5 * 1024 * 1024):
                return Response(data={
                    'message':'Archivo muy grande, no puede ser mas de 5Mb'
                }, status=status.HTTP_400_BAD_REQUEST )

            resultado = default_storage.save(
                (carpetaDestino+'/' if carpetaDestino is not None else '') + archivo.name, ContentFile
                (archivo.read()))
            print(resultado)
            return Response(data={
                'message':'archivo guardado exitosamente',
                'content':{
                    'ubicacion': resultado
                }
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data={
                'message':'Error al subir la imagen', 
                'content': data.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class EliminarArchivoApiView(DestroyAPIView):
    serializer_class = EliminarArchivoSerializer
    def delete(self, request: Request):
        data = self.serializer_class(data=request.data)
        try:
            data.is_valid(raise_exception=True)
            ubicacion = data.validated_data.get('archivo')
            remove(settings.MEDIA_ROOT / ubicacion)
            return Response(data={
                'message':'Archivo eliminado exitosamente',
            })
            
        except Exception as e:
            return Response(data={
                'message':'Error al eliminar archivo', 
                'content': e.errors
            }, status=status.HTTP_404_NOT_FOUND)