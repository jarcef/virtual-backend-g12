from .models import Comprobante, Pedido, DetallePedido
from menu.models import Plato, Stock
from django.db import connection
import requests
from os import environ
from datetime import datetime

def generar_comprobante(tipo_de_comprobante:int, tipo_documento:str, numero_documento: str, pedido_id:int):
    """Sirve para generar un comprobante electrónico ya sea Factura, Boleta o Notas en base a un pedido"""
    pedido = Pedido.objects.filter(id=pedido_id).first()

    validacionComprobante = Comprobante.objects.filter(pedido=pedido.id).first()

    if validacionComprobante is not None:
        raise Exception('Este pedido ya tiene un comprobante')

    if pedido is None:
        raise Exception('Pedido no existe')
    
    if pedido.total > 700:
            raise Exception(
                'El pedido al ser mayor a 700 soles tiene que pertenecer a una persona')

    operacion = 'generar_comprobante'
    tipo= ''
    sunat_transaction = 1
    if tipo_de_comprobante == 1:
        #esta serie se deberia de guardar en la bd en una tabla de series para que cuando el contador desee cambiar de serie se modifique en esa tabla
        serie = 'FFF1'
        tipo = 'FACTURA'
    elif tipo_de_comprobante == 2:
        serie = 'BBB1'
        tipo = 'Boleta'
    elif tipo_de_comprobante == 3 or tipo_de_comprobante == 4:
        serie == '0001'
        tipo = 'NOTA'
    #Lo sacaremos del último comprobante almacenado en la base de datos

    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM vista_prueba')
        print(cursor.fetchall())
    ultimoComprobante = Comprobante.objects.values_list('numero', 'serie').filter(
        tipo=tipo).order_by('-numero').first()

    if ultimoComprobante is None:
        numero = 1
    else:
        numero = int(ultimoComprobante[0]) + 1
    
    if tipo_documento is None:
        cliente_tipo_de_documento = '-'
        cliente_numero_de_documento = None
    else:
        if tipo_documento == 'RUC':
            cliente_tipo_de_documento = 6
        elif tipo_documento == 'DNI':
            cliente_tipo_de_documento = 1

        cliente_numero_de_documento = numero_documento
     
        if tipo_documento == 'RUC':
            respuesta_apiperu = requests.get("https://apiperu.dev/api/ruc/"+numero_documento,
                        headers={'Authorization': 'Bearer '+environ.get('APIPERU_TOKEN')})

            if respuesta_apiperu.json().get('success') == False:
                raise Exception('Datos del cliente no válidos')
            else:
                cliente_denominacion = respuesta_apiperu.json().get(
                    'data').get('nombre_o_razon_social')
                cliente_direccion = respuesta_apiperu.json().get('data').get('direccion_completa')
                
        elif tipo_documento == 'DNI':
            respuesta_apiperu = requests.get("https://apiperu.dev/api/dni/"+numero_documento,
                        headers={'Authorization': 'Bearer '+environ.get('APIPERU_TOKEN')})

            if respuesta_apiperu.json().get('success') == False:
                raise Exception('Datos del cliente no válidos')
            else:
                cliente_denominacion = respuesta_apiperu.json().get('data').get('nombre_completo')
                cliente_direccion = ''
    
    cliente_email = 'juliarcef@gmail.com'
    fecha_de_emision = datetime.now().strftime("%d-%m-%Y")
    moneda = 1
    porcentaje_de_igv = 18.00
    total = float(pedido.total)
    total_gravada = total / 1.18
    total_igv = total - total_gravada
    enviar_automaticamente_a_la_sunat = True
    enviar_automaticamente_al_cliente = True
    formato_de_pdf = "TICKET" # A4 | A5 | TICKET
    
    detalle_pedido: list[DetallePedido] = pedido.detalle_pedidos.all()

    detraccion = False

    items = []
    for detalle in detalle_pedido:        

        stock: Stock = detalle.stockId
        plato: Plato = stock.platoId
        unidad_de_medida ="NIU"
        codigo = plato.id
        descripcion = plato.nombre
        cantidad = detalle.cantidad

        precio_unitario = float(stock.precio_diario)
        valor_unitario = precio_unitario / 1.18

        subtotal = valor_unitario * cantidad
        tipo_de_igv = 1
        igv = subtotal * 0.18
        total_producto = precio_unitario * cantidad

        item = {
            'unidad_de_medida': unidad_de_medida,
            'codigo': codigo,
            'descripcion': descripcion,
            'cantidad': cantidad,
            'valor_unitario': valor_unitario,
            'precio_unitario': precio_unitario,
            'subtotal': subtotal,
            'tipo_de_igv': tipo_de_igv,
            'igv': igv,
            'total': total_producto,
            'anticipo_regularizacion': False
        }

        items.append(item)

    comprobante_body = {
        'operacion': operacion,
        'tipo_de_comprobante': tipo_de_comprobante,
        'serie': serie,
        'numero': numero,
        'sunat_trasaction': sunat_transaction,
        'cliente_tipo_de_documento': cliente_tipo_de_documento,
        'cliente_numero_de_documento': cliente_numero_de_documento,
        'cliente_denominacion': cliente_denominacion,
        'cliente_direccion': cliente_direccion,
        'cliente_email': cliente_email,
        'fecha_de_emision': fecha_de_emision,
        'moneda': moneda,
        'porcentaje_de_igv': porcentaje_de_igv,
        'total_gravada': total_gravada,
        'total_igv': total_igv,
        'total': total,
        'detraccion': detraccion,
        'observaciones': '',
        'enviar_automaticamente_a_la_sunat':enviar_automaticamente_a_la_sunat,
        'enviar_automaticamente_al_cliente':enviar_automaticamente_al_cliente,
        'medio_de_pago': 'EFECTIVO',
        'formato_de_pdf': formato_de_pdf,
        'items':items
    }
   
    url_nubefact = environ.get('NUBEFACT_URL')

    headers_nubefact = {
        'Authorization': environ.get('NUBEFACT_TOKEN'),
        'Content-Type': 'application/json'
    }

    respuestaNubefact = requests.post(url_nubefact, headers=headers_nubefact, json=comprobante_body)
        
    if respuestaNubefact.json().get('errors'):
        raise Exception(respuestaNubefact.json().get('errors'))

    else:
        nuevoComprobante = Comprobante(
            serie=serie,
            numero=numero,
            pdf=respuestaNubefact.json().get('enlace_del_pdf'),
            cdr=respuestaNubefact.json().get('enlace_del_cdr'),
            xml=respuestaNubefact.json().get('enlace_del_xml'),
            tipo=tipo,
            pedido=pedido)
        nuevoComprobante.save()
        return nuevoComprobante
        
    