from .models import Plato
from rest_framework.generics import CreateAPIView,ListCreateAPIView
from .serializers import PlatoSerializer
from rest_framework.permissions import(AllowAny,IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser)
#AllowAny > Sirve para que el controlador sea publico (no se necesita una token)
from rest_framework.response import Response
from rest_framework.request import Request
from cloudinary import CloudinaryImage
class PlatoApiView(ListCreateAPIView):
    serializer_class = PlatoSerializer
    queryset = Plato.objects.all()
    #sirve para indicar que tipos de permisos necesita el cliente para poder realizar la petición
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: Request):
        data = self.serializer_class(instance=self.get_queryset(),many=True)
        #Hacer una iteracion para modificar la foto de cada plato y devolver el link de la foto
        print(data.data[2].get('foto'))
        #del contenido de la foto solamente extraer el nombre del archivo o si esta en una carpeta extraer la carpeta y el archivo
        link = CloudinaryImage('plato/lx0bkezk8slcqftunnyc.jpg').image(secure=True)

        print(link)
        return Response(data=data.data)
