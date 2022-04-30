import { Prisma } from  "../prisma.js";
import { usuarioRequestDTO, loginRequestDTO } from "../dtos/usuarios.dto.js";
import { hashSync } from "bcrypt";
import { compareSync } from "bcrypt";
import jsonwebtoken from "jsonwebtoken";
import {enviarCorreoValidacion} from "../utils/sendMail.js";
import cryptojs from "crypto-js";

export const crearUsuario = async (req, res) => {
    try{
        const data = usuarioRequestDTO(req.body)
        const password = hashSync(data.password,10)

        const nuevoUsuario = await Prisma.usuario.create({
            data: {...data, password},
            select: {
                id: true,
                nombre: true,
                email: true,
                rol: true,
                validado: true,
            },
        });
        //crear un texto encriptado
        const hash = cryptojs.AES.encrypt(
            JSON.stringify({ 
                nombre: nuevoUsuario.nombre, 
                email: nuevoUsuario.email,
            }),
            process.env.LLAVE_ENCRIPTACION
            ).toString();
        
        await enviarCorreoValidacion({
            destinatario: nuevoUsuario.email,
            hash,
        });

        return res.status(201).json(nuevoUsuario);
    }catch (error) {
        // La clase error tiene el atributo messagen
        // Yo valida si una instancia es de una clase o no
        if (error instanceof Error){
            return res.status(400).json({
                message: "Error al crear el usuario",
                content: error.message,
            });
        }        
    }
};

export const login = async (req, res) => {
    try {
        const data = loginRequestDTO(req.body)
        const  usuarioEncontrado = await Prisma.usuario.findUnique({
            where: { email: data.email },
            rejectOnNotFound: true,
        });

        if (compareSync(data.password, usuarioEncontrado.password)) {
            const token = jsonwebtoken.sign(
                {
                    id: usuarioEncontrado.id,
                    mensaje: "API de Minimarket",
                },
                process.env.JWT_SECRET,
                { expiresIn: "1h"}
            );
            return res.json({
                message: "Bienvenido",
                content: token
            });
        } else {
            throw new Error("Credenciales incorrectas");
        }
    }catch (error) {
        if (error instanceof Error) {
            return res.status(400).json({
                message: "Error al hacer el inicio de sesion",
                content: error.message,
            });
        }
    }
};

export const confirmarCuenta = async (req, res) => {
    //TODO crear el DTO de la confirmación de la cuenta
    // const data = confirmarCuentaRequestDTO(req.body)

    try {
        const data = req.body;
        const informacion = JSON.parse(
            cryptojs.AES.decrypt(data.hash, process.env.LLAVE_ENCRIPTACION).toString(
            cryptojs.enc.Utf8
            )
        );

        console.log(informacion);

         //De acuerdo a esa información:
        // 1. Buscar el usuario en la bd con su correo y que su "validado" sea false, si es true indicar que el usuario ya validó su cuenta (400)
        const usuarioEncontrado = Prisma.usuario.findFirst({
            where: { 
                email: informacion.email,
                validado: False,
        },
        select: { 
            id: true,
        },
        });

        if (!usuarioEncontrado) {
            throw new Error("El usuario ya fue validado");
        }

        // 2. Actualizar el estado validado a true
        await Prisma.usuario.update({
            where: { id: usuarioEncontrado.id },
            data: { validado: true },
        });

        return res.json({
            message: "Cuenta validada correctamente",
        });
    }catch (error) {
        if (error instanceof Error) {
            return res.status(400).json({
                message: "Error al validar la cuenta",
                content: error.message,
            });
        }
    }   
};

//controlador protegido (recibira una JWT)
export const perfil = async (req, res) => {
    console.log(req, res);

    return res.json({
        message: "Bienvenido",
        content: req.user,
    });
};