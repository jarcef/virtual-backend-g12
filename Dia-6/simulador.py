#factory
from faker import Faker
from random import randint, choice
from faker.providers import internet, person, phone_number

fake = Faker()
#fake.add_provider(internet, person)
#fake.add_provider(internet, phone_number, person)


def generar_alumnos(limite):
    for persona in range(limite):
        nombre = fake.first_name()
        apePat = fake.last_name()
        apeMat = fake.last_name()
        correo = fake.ascii_free_email()
    #telefono = fake.phone_number()
        telefono = fake.bothify(text='9########')
        sql = '''INSERT INTO alumnos (nombre, apellido_paterno, apellido_materno, correo, numero_emergencia) VALUES
                ('%s', '%s', '%s', '%s', '%s');''' % (nombre, apePat, apeMat, correo, telefono)

        '''INSERT INTO alumnos (nombre, apellido_paterno, apellido_materno, correo, numero_emergencia) VALUES
                ('%s', '%s', '%s', '%s', '%s');''' % (nombre, apePat, apeMat, correo, telefono)

        print(sql)

def generar_niveles():
    secciones = ['A','B','C']
    ubicaciones = ['Sotano','Primer Piso','Segundo Piso','Tercer Piso']
    niveles = ['Primero','Segundo','Tercero','Cuarto','Quinto','Sexto']
        #Iterar los niveles y en cada nivel colocar como minimo dos secciones y como maximo 3 (random_int) y luego agregar aleatoriamente la ubicación a ese nivel
        #Primero A Segundo Piso
        #Primero B Tercer Piso
        #Segundo A Sotano

    for nivel in niveles:

        #pos_secciones = fake.random_int(min=2, max=3)
        #for posicion in range(0, pos_secciones):
          #  pos_ubicacion = fake.random_int(min=0, max=3)

          pos_secciones = randint(2,3)
          for posicion in range(0, pos_secciones):
              ubicacion = choice(ubicaciones)
              seccion = secciones[posicion]
              nombre = nivel
              sql = '''INSERT INTO niveles(seccion, ubicacion, nombre) VALUES
                        ('%s','%s','%s');''' % (seccion, ubicacion, nombre)

              print(sql)

         #   print('Nivel', nivel)
         #   print('Seccion', secciones[posicion])
         #   print('Ubicacion', ubicaciones[pos_ubicacion])                
def generar_niveles_alumno():
    #generar un numero aleatorio que sera el id del alumno y el id del nivel y un año de manera en la cual no se puede volver a generar ese mismo alumno con un nivel
    #inferior  pero con año superior
    #ALUMNO_ID   NIVEL_ID   YEAR
    #   1           3       2000  / 3 >  Segundo A
    #   2           



