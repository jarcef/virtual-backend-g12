import { Router } from "express";
import {
    eliminarProducto,
    actualizarProducto,
    crearProducto,
    listarProductos,
} from "../controllers/productos.controller.js";
import { validarAdmin, verificarToken } from "../utils/validador.js";

export const productosRouter = Router();

productosRouter
    .route("/productos")
    .post(verificarToken, validarAdmin, crearProducto)
    .get(listarProductos);


productosRouter 
    .route("/producto/:id")
    .all(verificarToken, validarAdmin)
    .put(actualizarProducto)
    .delete(eliminarProducto);