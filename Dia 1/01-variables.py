#Esto es un comentario y sirve para dar contexto de que se hace, se hizo o se hará
#TODO: logica para este controlador

#variables de texto
nombre='eduardo'
apellido = "de'rivero"
#si queremos tener un texto que puedo contener saltos de linea
descripcion = """hola amigos:
como estan?
yo muy bien je je
"""

descripcion2 = '''hola amigos:
como estan?'''

print('a','b','c')
print(descripcion)
print(descripcion2)

#variables numericas
year = 2022

#type() => mostrará el tipo de variable
print(type(year))
print(type(descripcion2))

#Python no se puede crear una variable sin un contenido
#en python None = null | undefined

especialidad = None
#en Python no hace validación del tipo de dato primario (si la variable 'nace' siendo string) normal se puede cambiar su tipo a otro (Boolean, int, float, array, etc)
#En  python no existen las constancias
dni=[12345678]
dni='peruano'
dni=False
#id() > dara la ubicación de esa variable en relación a la memoria del dispositivo
print(id(dni))
print(type(especialidad))
mes, dia = "febrero",28
print(mes)
print(dia)
#del > elimina la variable de la memoria
del mes
#Si queremos usar luego de la eliminación de esa variable no será posible ya que se eliminó
print(mes)

