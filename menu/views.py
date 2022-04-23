from .models import Plato, Stock
from rest_framework.generics import CreateAPIView,ListCreateAPIView
from .serializers import (PedidoSerializer,
                          PlatoSerializer, 
                          StockSerializer, 
                          AgregarDetallePedidoSerializer, 
                          StockCreateSerializer)
from rest_framework.permissions import(AllowAny,IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, SAFE_METHODS)
#AllowAny > Sirve para que el controlador sea publico (no se necesita una token)
from rest_framework.response import Response
from rest_framework.request import Request
from cloudinary import CloudinaryImage
from .permissions import SoloAdminPuedeEscribir, SoloMozoPuedeEscribir
from fact_electr.models import Pedido, DetallePedido
from rest_framework import status
from django.utils import timezone
from django.db import transaction, IntegrityError
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

    def get_serializer_class(self):
        if not self.request.method in SAFE_METHODS:
            return StockCreateSerializer
        return StockSerializer

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
    permission_classes = [IsAuthenticated, SoloMozoPuedeEscribir]

    def post(self, request:Request):
        #1. Valido la data en el serializer
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        #2. Verifico que tenga esa cantidad de productos en stock
        stock: Stock | None = Stock.objects.filter(fecha=timezone.now(),
                                    platoId=data.validated_data.get('platoId'), cantidad__gte=data.validated_data.get('cantidad')).first()
        print(stock)
        if stock is None:
            return Response(data={'message':'No hay stock para ese producto para el dia de hoy'},
                                    status=status.HTTP_400_BAD_REQUEST)
        #Validar si el pedido existe
        pedido: Pedido | None = Pedido.objects.filter(id=data.validated_data.get('pedidoId')).first()

        if pedido is None:
            return Response(data={'message': 'No hay ese pedido'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():
                #Todo lo que  esté dentro de esta definición de atomic() respetará a la creación de la transacción
                #Guardar ese detalle de ese pedido
                #Al agregar un nuevo registro y este tuviese FKs no solamente bastara con poner el Id sino que tendremos que pasar toda la instancia para que django
                #se cerciore que ese registro (FK) sea valida
                nuevoDetalle = DetallePedido(cantidad=data.validated_data.get('cantidad'), stockId=stock, pedidoId=pedido)
                nuevoDetalle.save()
                 #Disminuir el stock de ese plato en la tabla stock
                stock.cantidad = stock.cantidad - nuevoDetalle.cantidad 
                #Guarda las modificaciones en la bd de ese registro
                stock.save()
                #Modifico el total de la cabecera
                pedido.total = pedido.total + (nuevoDetalle.cantidad * stock.precio_diario)
                pedido.save()
                 #si termina este bloque sin ningun error entonces automaticamente se hará un commit a la bd
                
        except IntegrityError:
            return Response(data={'message': 'Error al crear el pedido, todo quedó en nada'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # información que se envía al front
        #{
        #    "cantidad":2,
        #    "plato":1,
        #    "pedido_id":2
        #}
        #verificar que en el stock este en base al dia de hoy esa actividad
        #3. Agrego el detalle con su respectivo pedido
        
        return Response(data={'message':'Detalle agregado exitosamente'})