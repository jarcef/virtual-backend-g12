import { libroRequestDTO } from "../dtos/libro.request.dto.js";
import { Usuario } from "../models/usuarios.models.js";


export const agregarLibro = async (req, res) => {
    //dto en el cual valido que no envie los campos paora agregar el libro
    try {
        const data = libroRequestDTO(req.body);
     //   console.log(req.user);
        const usuarioActual = req.user;
        usuarioActual.libros.push(data);
        // Internamente cuando hacemos una busqueda a un registro de mongoose se jala algunos datos para poder sobreescribir o 
        //modificar este registro a nivel de base de datos y eso se logra con el metodo save() (es un proceso asincrono)

        await usuarioActual.save();

        return res.json({        
            message:"ok",
            content: usuarioActual.libros,
        });
    } catch (e) {
        return res.status(400).json({ 
            message: "Error al agregar el libro",
            content: e.message,
        });
    }    
};

export const listarLibros = (req, res) => {
     
    return res.json({
        message: " Los libros son:",
        content:  req.user.libros,
    });
};

export const devolverLibro = async (req, res)=>{
    const { _id: id_del_libro } = req.params;
   
    const libroEncontrado = await Usuario.findOne(
        {
           _id: req.user._id, //id del usuario
            "libros._id": id_del_libro,  // id del libro
        },
        { 
            "libros.$": 1,
        }    
    );

    const libro = req.user.libros.filter(
        (libro)=> libro._id.toString() === id_del_libro
    );

    return res.json({
        message: "El libro es:",
        content: libro,
        content2: libroEncontrado,
    });
};