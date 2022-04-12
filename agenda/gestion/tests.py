from django.test import TestCase
from rest_framework.test import APITestCase


class EtiquetasTestCase(APITestCase):
    def test_crear_etiqueta_success(self):
        request = self.client.post('/gestion/etiquetas', data={
            'nombre':'Frontend'
        })

        self.assertEqual(request.status_code, 201)

        self.assertEqual(1,1)

    def test_listar_etiquetas_success(self):    
        request = self.client.get('/gestion/etiquetas')
        print(request.data)
        self.assertEqual(1,1)