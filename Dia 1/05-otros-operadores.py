#Operadores de comparacion
numero1, numero2 = 10, 20
#NOTA: en python no tenemos  el triple igual de
# #===
#Igual que
print(numero1==numero2)
#Mayor que | Mayor igual que
print(numero1 > numero2)
print(numero1 >= numero2)
#;empr qie | Menor igual que
print(numero1 < numero2)
print(numero1 <= numero2)
#Diferente de
print(numero1 != numero2)
#Operadores lógicos
#sirve para comparar varias comparaciones
#en JS se utiliza && en python se utiliza la palabra and
#en JS se utiliza || en python se utiliza la palabra or


#Operadores de identidad
#is
#is not
#sirve para ver si estan apuntando a la misma direccion de memoria
verduras=['apio','lechuga','zapallo']
verduras2=verduras
verduras3=['apio','lechuga','zapallo']
#NOTA: Las colecciones de datos son variables mutables (que cuando cambio su contenido este se vera reflejado en todas las copias de dicha variable
verduras2[0] = 'perejil'
verduras[1] ='manzana'



nombre ='eduardo'
nombre2= nombre
print(nombre2 is nombre)


#Validar si el nombre del usuario es eduardo y que sea peruano o colombiano
nombre='eduardo'
nacionalidad ='cubano'
print(nombre =='eduardo' and nacionalidad ='peruano' or nacionalidad == 'colombiano')