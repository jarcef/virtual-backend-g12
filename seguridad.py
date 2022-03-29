from bcrypt import checkpw
from config import conexion
from models.usuarios import Usuario


def autenticador(username, password):
    """Funcion encaargada de validar si las credenciales son correctas o no, si no son no pasara pero si los son retornara una JWT"""
    #Primero valido si los parametros son correctos

    if username and password:
        #buscaré el usuario en la bd
        usuarioEncontrado = conexion.session.query(
            Usuario).filter_by(correo=username).first()
        if usuarioEncontrado:
            validacion = checkpw(bytes(password,'utf-8'), 
                                bytes(usuarioEncontrado.password,'utf-8'))
            if validacion is True:
                print('si es la contraseña')
                return usuarioEncontrado
            else:
                return None
        else:
            return None
    else:
        return None

def identificador(payload):
    """Sirve para validar al usuario previamente autenticado"""
    # en el payload obtendremos la parte intermedia de la JWT que  es la información que se puede visualizar sin la necesidad de saber la contraseña de la token
    # identity > la identificación del usuario por lo general viene a ser el id o uuid del mismo
    # SELECT * from  USUARIOS WHERE ID ......
    usuarioEncontrado : Usuario | None = conexion.session.query(
        Usuario).filter_by(id = payload['identity']).first()
    if usuarioEncontrado:
        #Esta información me servirá para cuando quiera acceder al usuario actual de la petición
        return {
            'id': usuarioEncontrado.id,
            'nombre': usuarioEncontrado.nombre,
            'correo': usuarioEncontrado.correo
        }
    else:
        return None