import jsonwebtoken from "jsonwebtoken";
import { Prisma } from "../prisma.js";

export async function verificarToken(req, res, next) {
    //middleware

    if (!req.headers.authorization) {
        return res.status(401).json({ 
            message: "Se necesita una token para realizar esta petición",
        });
    }
    try {
        //recibiré en el authorization lo siguiente: "Bearer asdaddsffs.afdsfsfsfsf.afasfsfs"
        const token = req.headers.authorization.split(" ")[1];
        // si la pwd es incorrecta, la token caduco o la token está mal formateada emitirá un error

        const payload = jsonwebtoken.verify(token, process.env.JWT_SECRET);

        // Si la token fue verificada correctamente nos devolverá el payload en el cual hemos guardado el id del usuario, ahora buscaremos ese usuario en la bd
        const usuarioEncontrado = await Prisma.usuario.findUnique({
            where: { id: payload.id },
            rejectOnNotFound: true,
        });
        // ahora agregar el json del Request el usuario para que pueda ser utilizada en los demas controladores
        req.user = usuarioEncontrado;
        // ahora le digo que pase el siguiente controlador
        next();
    }catch (error){
        return res.status(400).json({ 
            message: "Token invalida",
            content: error.message,
        });
    }
}