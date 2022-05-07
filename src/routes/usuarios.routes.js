import { Router } from "express";
import { registrarUsuario,
         login
         } from  "../controllers/usuarios.controllers.js"; 

export const usuariosRouter = Router();

usuariosRouter.post("/registro", registrarUsuario);
usuariosRouter.post("/login", login)