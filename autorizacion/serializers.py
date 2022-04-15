from  rest_framework import serializers
from .models import Usuario

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    
    def save(self):
        #Crea una instancia 
        nuevoUsuario= Usuario(**self.validated_data)

        nuevoUsuario.set_password(self.validated_data.get('password'))

        nuevoUsuario.save()

        return nuevoUsuario
    
    class Meta:
        model = Usuario
        exclude = ['groups','user_permissions']

       #fields = '__all__'

        extra_kwargs = {
            'password':{
                'write_only': True
            },
            'id':{
                'read_only': True
            }
        }
