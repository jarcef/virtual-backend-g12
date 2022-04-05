from email import header
import unittest
from app import app
from datetime import datetime

class TextInicioFlask(unittest.TestCase):
    def setUp(self):
        self.nombre = 'Eduardo'
        self.aplicacion_flask = app.test_client()
    
    @unittest.skip('Los salte por solamente queria ver el funcionamiento del metodo setUp')
    def testNombre(self):
        self.assertEqual(self.nombre, 'Eduardo')

    def testEndpointStatus(self):
        '''deberia retornar la hora del servidor y su estado'''
        respuesta = self.aplicacion_flask.get('/status')
        
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json.get('status'), True)
        self.assertEqual(respuesta.json.get('hora_del_servidor'), 
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def testLoginJWTExitoso(self):
        '''deberia retornar una token para ingresar a las rutas protegidas'''
        #Mocks
        body = {
            'correo': 'juliarcef@gmail.com',
            'pass': 'Welcome123!'
        }
        respuesta = self.aplicacion_flask.post('/login-jwt', json=body)
        print(respuesta.json)
        self.assertEqual(respuesta.status_code, 200)
        self.assertNotEqual(respuesta.json.get('access_token'), None)

    def testLoginJWTCredencialesIncorrectas(self):
        '''deberia retornar un error si las credenciales son incorrectas'''
        body = {
            'correo': 'juliarcef@gmail.com',
            'pass': '12345678asasa'
        }
        respuesta = self.aplicacion_flask.post('/login-jwt', json=body)
        self.assertEqual(respuesta.status_code, 401)
        self.assertEqual(respuesta.json.get('access_token'), None)
        self.assertEqual(respuesta.json.get(
            'description'), 'Invalid credentials'
        )

# una clase por cada endpoint

class TestYo(unittest.TestCase):
    def setUp(self):
        self.aplicacion_flask = app.test_client()
        body = {
            'correo': 'juliarcef@gmail.com',
            'pass': 'Welcome123!'
        }
        respuesta = self.aplicacion_flask.post('/login-jwt', json=body)
        self.token = respuesta.json.get('access_token')
            
    def testNoHayJWT(self):
        # TODO: hacer este test con todas las supusiciones
        pass
    
    def testPerfil(self):
        respuesta = self.aplicacion_flask.get(
            '/yo', headers={'Authorization': 'Bearer {}'.format(self.token)})
        self.assertEqual(respuesta.status_code,200)
        self.assertEqual(respuesta.json.get('message'),'El usuario es')
      
class TestMovimientos(unittest.TestCase):
    #TODO: hacer los test para extraer los movimientos creados del usuario, hacer el caso cuando se pase una JWT, cuando no se pase una token, 
    # cuando no tenga movimientos y cuanto tengo movimientos 
    pass