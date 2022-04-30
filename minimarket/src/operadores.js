const POST = process.env.PORT ?? 3000;

const persona = {
    nombre: "eduardo",
    apellido: "de Rivero",
};

let actividades = persona.actividades && persona.actividades[0];
actividades = false;
actividades = 10.2;
actividades = new Date();
actividades = undefined;

// Operador OR ||
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Logical_OR
// en JS el 0 significa False y el 1 y los demas numeros significan True
const numero1 = false;
// si la primera condicion es verdadera entonces devuelvo esa sino devolvere la segunda
const resultado = numero1 || 10;
// si el primero resultado no es null o undefined lo devolvere caso contrario devolver el segundo valor
const resultado2 = numero1 ?? 10;
console.log(resultado);
console.log(resultado2);
