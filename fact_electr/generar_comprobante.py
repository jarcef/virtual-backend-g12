from .models import Comprobante, Pedido
from django.db import connection
import requests
from os import environ

def generar_comprobante(tipo_de_comprobante:int, tipo_documento:str, numero_documento: str, pedido_id:int):
    """Sirve para generar un comprobante electrónico ya sea Factura, Boleta o Notas en base a un pedido"""
    pedido = Pedido.objects.filter(id=pedido_id).first()
    if pedido is None:
        raise Exception('Pedido no existe')
    
    if pedido.total > 700:
            raise Exception(
                'El pedido al ser mayor a 700 soles tiene que pertenecer a una persona')

    operacion = 'generar_comprobante'
    tipo= ''
    sunat_transaccion = 1
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
        cliente_tipo_de_documento = tipo_documento
        cliente_numero_de_documento = numero_documento
     
        if tipo_documento == 'RUC':
            respuesta_apiperu = requests.get("https://apiperu.dev/api/ruc/"+numero_documento,
                        headers={'Authorization': 'Bearer'+environ.get('APIPERU_TOKEN')})

            if respuesta_apiperu.json().get('success') == False:
                raise Exception('Datos del cliente no válidos')
            else:
                cliente_denominacion = respuesta_apiperu.json().get(
                    'data').get('nombre_o_razon_social')                


        elif tipo_documento == 'DNI':
            respuesta_apiperu = requests.get("https://apiperu.dev/api/dni/"+numero_documento,
                        headers={'Authorization': 'Bearer'+environ.get('APIPERU_TOKEN')})

            if respuesta_apiperu.json().get('success') == False:
                raise Exception('Datos del cliente no válidos')
            else:
                cliente_denominacion = respuesta_apiperu.json().get('data').get('nombre_completo')