from .models import Plato, Stock
from rest_framework.generics import CreateAPIView,ListCreateAPIView
from .serializers import PedidoSerializer,PlatoSerializer, StockSerializer, AgregarDetallePedidoSerializer
from rest_framework.permissions import(AllowAny,IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser)
#AllowAny > Sirve para que el controlador sea publico (no se necesita una token)
from rest_framework.response import Response
from rest_framework.request import Request
from cloudinary import CloudinaryImage
from .permissions import SoloAdminPuedeEscribir, SoloMozoPuedeEscribir
from fact_electr.models import Pedido, DetallePedido
from rest_framework import status
from django.utils import timezone
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


class StockApiView(ListCreateAPIView):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
    permission_classes = [IsAuthenticated, SoloAdminPuedeEscribir]

class PedidoApiView(ListCreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated, SoloMozoPuedeEscribir]

    def post(self, request: Request):
        print(request.user)
        request.data['usuarioId'] = request.user.id
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        data.save()
        return Response(data=data.data, status=status.HTTP_201_CREATED)

class AgregarDetallePedidoApiView(CreateAPIView):
    queryset = DetallePedido.objects.all()
    serializer_class = AgregarDetallePedidoSerializer

    def post(self, request:Request):
        #1. Valido la data en el serializer
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        #2. Verifico que tenga esa cantidad de productos en stock
        stock = Stock.objects.filter(fecha=timezone.now(),
                                    platoId=data.validated_data.get('platoId')).first()
        print(stock)
        # información que se envía al front
        #{
        #    "cantidad":2,
        #    "plato":1,
        #    "pedido_id":2
        #}
        #verificar que en el stock este en base al dia de hoy esa actividad
        #3. Agrego el detalle con su respectivo pedido
        return Response(data={'message':'Detalle agregado exitosamente'})