import {Usuario} from '../models/usuarios.models.js';
import bcryptjs from "bcryptjs";
import jwt from "jsonwebtoken";

export const registrarUsuario =  async (req, res) => {
    const data = req.body;
    try{
        const nuevoUsuario = await Usuario.create(data);

        console.log(nuevoUsuario.toJSON());
        console.log(Object.keys(nuevoUsuario));

        const result = nuevoUsuario.toJSON();
        delete result["password"];
        delete nuevoUsuario["_doc"]["password"];

        return res.status(201).json({
            message: "Usuario creado exitosamente",
            content: result,
        });
    }catch (e) {
        return res.status(400).json({
            message: "Error al crear el usuario",
            content: e.message,
        });
    }
};

export const login = async (req, res)=> {
    const data = req.body
    const usuarioEncontrado = await Usuario.findOne({correo: data.correo})

    if(!usuarioEncontrado){
        return res.status(400).json({
            message:'Credenciales incorrectas'
        });
    }
    //valida su password
    if(bcryptjs.compareSync(data.password, usuarioEncontrado.password)) {
        const token = jwt.sign(
            { _id: usuarioEncontrado._id },
            process.env.JWT_SECRET,
            {
                expiresIn: "1h",
            }
        );
        return res.json({
            message: "Bienvenido",
            content: token,
        });
    }else {
        return res.status(400).json({
            message: "Credenciales incorrectas",
        });
    }
};