import { Router } from  "express";
import { crearUsuario,
         login,
         confirmarCuenta,
         perfil
        } from "../controllers/usuarios.controllers.js";
        import { verificarToken } from "../utils/validador.js"

export const usuarioRouter = Router();

usuarioRouter.post("/registro", crearUsuario);
usuarioRouter.post("/login", login);
usuarioRouter.post("/confirmar-cuenta", confirmarCuenta);
usuarioRouter.get("/perfil", verificarToken, perfil);