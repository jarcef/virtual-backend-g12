def sumar(a,b):
    return a+b

print(sumar(10,5))
print(sumar(a=10, b=5))
parametros = {
    'a':10,
    'b':5
}

print(sumar(**parametros))
print(sumar(*[10,5]))

def restar(**kwargs):
    print(kwargs)

def multiplicar(*args):
    return(args)

print(multiplicar(5,4))
print(restar(x=1,y=2,z=3))
