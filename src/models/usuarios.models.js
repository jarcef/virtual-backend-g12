import bcryptjs from "bcryptjs";
import mongoose from "mongoose";
//Toda la configuración que estamos haciendo es solamente a nivel de mongoose, osea si agregamos un usuario de frente a la bd no hará caso a ninguna de estas caracteristicas

const libroSchema = new mongoose.Schema({
    nombre: {
       type: mongoose.Schema.Types.String,
       required: true,       
    },
    
    avance: {
        type: mongoose.Schema.Types.String,
        enum: ["COMPLETO", "INCOMPLETO"],
        required: true,
    }, // completo o incompleto
    numPagina: {
        type: mongoose.Schema.Types.Number,
        min: 1,
        name: 'num_pagina', //en la bd la columna se llama de esa manera mientras que en mongoose se llama como el nombre de la llave
    },
},
{
 //   _id: false, //sirve para indicar que en este schema no se creará automaticamente el _id (primary key)
    timestamps: {
        updatedAt: "fecha_actualizacion", // true > solo creare el update | string > creara esa columna pero con ese nombre
    },// creará las columnas de auditoria (created_at y el updated_at)
}

)

const usuarioSchema = new mongoose.Schema({
    correo: {
       type:  mongoose.Schema.Types.String,
       required: true,
       unique: true,
       lowercase: true,
       maxlength: 100,
    },

    nombre: {},

    nombre: mongoose.Schema.Types.String,

    telefono: {
        type: mongoose.Schema.Types.Number,
        required: false,
    },
    password: {
        type: mongoose.Schema.Types.String,
        set: (valorActual) => bcryptjs.hashSync(valorActual, 10),
    },
    //asi seria una relación de 1:1 en la cual un usuario solo puede tener un libro y un libro le pertenece a un usuario
    //libro: libroSchema
    //asi sería una relacion de 1:n un usuario puede tener varios libros pero ese libro solo le perteneceria a un usuaruio

    libros: {
        //[libroSchema]
        type: [libroSchema],
    },

});
//aca indicamos que crearemos una colección en la bd
export const Usuario = mongoose.model("usuarios", usuarioSchema);