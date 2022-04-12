from rest_framework import serializers
from .models import Etiqueta, Tareas

class PruebaSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=40, trim_whitespace=True)
    apellido = serializers.CharField()
    correo = serializers.EmailField()
    dni = serializers.RegexField(max_length=8, min_length=8, regex="[0-9]")
  #  dni = serializers.IntegerField(min_value=10000000, max_value=99999999)


class TareasSerializer(serializers.ModelSerializer):

  foto = serializers.CharField(max_length=100)
  class Meta:
    model = Tareas
    fields = '__all__'

    extra_kwargs = {
      'etiquetas': {
          'write_only': True
      }
    }

   
class TareaSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tareas
    fields = '__all__'

    depth = 1

class EtiquetaSerializer(serializers.ModelSerializer):
  tareas = TareaSerializer(many=True, read_only=True)
  class Meta:
    model = Etiqueta
    fields = '__all__'

    extra_kwargs = {
      #'nombre':{
      #      'write_only': True
      #      },
              'id': {
                'read_only': True
                }
            }
    read_only_fields = ['createAt']
    
class TareaPersonalizableSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Tareas
    fields = '__all__'
    extra_kwargs = {
      'nombre': {
          'read_only': True
      }
    }


class ArchivoSerializer(serializers.Serializer):
  archivo = serializers.ImageField(max_length= 100, use_url=True)

#Crear un serializador el cual reciba un nombre que sera un CharField cuya longitud maxima sea
class EliminarArchivoSerializer(serializers.Serializer):
    archivo = serializers.CharField(max_length=100)
   