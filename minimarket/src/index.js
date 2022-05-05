import express, { json } from "express";
import { pedidosRouter } from "./routes/pedidos.routes.js";
import {productosRouter} from "./routes/productos.routes.js";
import { usuarioRouter } from  "./routes/usuarios.routes.js";
import { detallePedidoRouter } from "./routes/detallePedido.routes.js";
import { pagosRouter } from "./routes/pagos.routes.js";
import mercadopago from  'mercadopago'

const app = express();

mercadopago.configure({
    access_token: process.env.MP_ACCESS_TOKEN,
    integrador_id: process.env.MP_INTEGRATOR_ID,
});

app.use(json());

const PORT = process.env.PORT ?? 3000;

app.get("/", (req, res) =>{
    res.json({ 
        message: "Bienvenido a mi API del minimarket",
    });
});
// agregar un bloque de rutas definidas en otro archivo
app.use(productosRouter);
app.use(usuarioRouter);
app.use(pedidosRouter);
app.use(detallePedidoRouter);
app.use(pagosRouter);

app.listen(PORT , () => {    
    console.log(`Servidor corriendo exitosamente en el puerto ${PORT}`);
});
