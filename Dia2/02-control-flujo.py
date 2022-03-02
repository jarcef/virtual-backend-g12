#IF - ELSE 
#python al no utilizar las llaves para definir bloque de un comportameinto diferente tenemos que utilizar tabulaciones (TAB)

edad = int(input('Ingresa tu edad: '))
if(edad>18):
    #todo lo que se escriba aca adentro
    print('La persona es mayor de edad: ')
    #La alineación nunca debe de variar si estamos en el mismo bloque de codigo
    print('otra impresion')
#se uliliza si la primera condicion fallo pero queremos hacer una segunda condicion
elif edad > 15:
    print('Puedes ingresar a la preparatoria')
elif edad > 10:
    print('Puedes vacunarte con la vacuna')
#el else es completamente opcional y no siempre se debe utilizar con un if
else:
    print('Eres muy niño')
print('Finalizó el programa')
