#Colección de datos es una variable que puede almacenar varios valores
#Listas (List)
#Ordenadas y que puede ser  modificados
from xml.etree.ElementPath import xpath_tokenizer


nombre=['Pedro','Luis','Danny','Cesar','Magaly']

combinada=['Eduardo',80,False,15.8,[1,2,3]]

#las listas siempre empiezan en la posición 0
print(nombre[0])
#cuando hacemos el uso de valores negativos en una lista internamente python le dará vuelta
print(nombre[-1])
print(nombre)
#si queremos ingresar a una pósicion inexistente nos lanzará un error de indice fuera de rango
#print(nombre[10])
#pop()> remueve el ultimo elemento de la lista y se puede almacenar en otra variable
resultado = nombre.pop()
print(resultado)
print(nombre)
#append()> ingresa un nuevo elemento a la ultima posición de la lista
nombre.append('Juana')
#elimina el contenido de una posición de la lista pero no la podemos almacenar en otra variable
del nombre[0]

print(nombre)
#clear()> limpia toda la lista y la deja como nueva
nombre.clear()
print(nombre)

x=combinada[1:4]
y=combinada
#indicar uan sub seleccion de la lista               
print(combinada[1:4])
#indicando el contenido de la lista y esto es muy util para hacer una copia de la lista sin usar su misma posición de memoria
print(id(x))
print(id(combinada))
print(id(y))

#desde el inicio hasta <2
print(combinada[:2])
#desde la posicion 2 hasta el final
print(combinada[2:])
meses_dscto=['Enero','Marzo','Juli0']
mes = 'Septiembre'
mes2='Enero'

print(mes not in meses_dscto)
#indicar si el valor se encuentra en la lista
print(mes2 in meses_dscto)

seccion_a =['Roxana','Juan']
seccion_b =['Julieta','Martin']
#si hacemos una sumatoria en las listas estas se combinaran en la cual la segunda lista ira despues de la primera
print(seccion_a + seccion_b)
#sirve para esperar un dato ingresado por el usuario
#dato = input('Ingresa tu nombre:')
#print(dato)

#tuplas
#muy similar a la lista a excepcion que no se puede modificar
cursos=('backend','frontend',1,True)
print(cursos)
print(cursos[0])
print(cursos[0:1])
cursos.append('otra cosa')
#cursos[0] = 'mobile design'
#en la tupla solamente no podremos alterar los valores pertenecientes a ella pero si dentro de esta hay una lista u otra colección de datos que si se puede modificar entonces si podremos alterar esta sub colección sin problemas
variada = (1,2,3,[4,5,6])
variada[3][0]='Hola'
print ( 2 in variada )
#creamos una nueva lista a raiz de una tupla llamando a la clase list en la cual en el constructor de esa clase le pasamos los valores que contnndrá la nueva lista
variada_lista = list(variada)
#no se puede crear una lista a raiz de otra lista, eso lanzará un error, solo se puede crear una lista mediante su constructor mediante una tupla
list((1,2,3)) # [1,2,3] 
print(variada_lista)

#para ver la cantidad de elementos que conforman una tupla o una lista
#NOTA: la longitud siempre sera la cantidad de elementos y esta siempre empezará en 1 mientras que la posicion siempre empezará en 0, es por eso que siempre la longitud = posicion + 1
print(len(variada))

#conjuntos (Set)
#Coleccion de datos DESORDENADA, una vez que se crea ya no se puede acceder a las posiciones de sus elementos
estaciones = {'Verano','Otonio','Primavera','Invierno'}
#una vez que se crea se asigna una posición aleatoria pero no cambia cada vez que se manda a llamar a este conjunto
print('Invierno' in estaciones)
#se agrega  de forma aleatoria
estaciones.add('Otro')
#al ser desordenada al momento de retirar el ultimo elemento este sera completamente aleatoria y retirará el ultimo elemento agregada de forma aleatoria
#pop()> quita el ultimo elemento de la colección de datos (list, tuplas, set)
estacion = estaciones.pop()
print(estacion)

#Diccionarios
#una coleccion de datos DESORDENADA pero cada elemento obedece a una llave definida

persona={
    'nombre': 'Eduardo',
    'apellido': 'De Rivero',
    'correo': 'ederiveroman@gmail.com'
}
#hacemos la busqueda de una determinada llave y si no la encuentra nos retornará opcionalmente None
print(persona.get('apellido','No hay no existe'))
#print(personal['apellidos'])

#devuelve todas las llaves de mi diccionario
print(persona.keys())
#devuelve todos los contenidos de mi diccionario
print(persona.values())
#devuelve todas las llaves y su contenido en forma de tupla dentro de una lista
print(persona.items())
#si definimos una llave que no existe, la creará, caso contrario modificará su valor
persona['edad']=28
#NOTA: si la llave no es exactamente igual creará uan nueva (tiene que coincidir minusculas)
persona['Nombre']='Ximena'
print(persona.values())
#eliminar una llave de un diccionario
persona.pop('apellido')

print(persona['apellido'])