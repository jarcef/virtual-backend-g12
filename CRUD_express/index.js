
//usando ECMAScript
import express from 'express'
import cors from "cors";
//Usando CommandJs
//import express = require('express')

const servidor = express()
//Midleware intermediario que permite visualizar información adicional, ahora podremos recibir y entender a un formato JSON
servidor.use(express.json())
//Recibir y entender los bodys que sean puro texto
servidor.use(express.raw())
servidor.use(express.urlencoded({extended: true}))
servidor.use(
    cors({
        origin: ["http://127.0.0.1:5500"],
        methods: ["POST","PUT","DELETE"],
        allowedHeaders: ["Content-Type", "Authorization"],
    })
);

const productos = [
    {
        nombre: 'platano',
        precio: 1.80,
        disponible: true
    }
]

servidor.get('/',(req, res)=>{
   return res.status(200).json({
        message: 'Bienvenido a mi API de productos'
    })
})

servidor.post('/productos', (req,res)=>{
    console.log(req.body);
    const data = req.body

    productos.push(data)

    return res.status(201).json({
        message:'Producto agregado exitosamente'
    })
})


servidor.get('/productos',(req,res)=>{
    const data = productos
    return res.json({
        data //que la llave será el mismo nombre que la variable y su valor será el contenido de esa variable
    })
})

servidor
    .route("/producto/:id")
    .get((req,res)=>{
    console.log(req.params);
    const {id} = req.params
    
    if (productos.length < id) {
        return res.status(400).json({
            message: 'El producto no existe'
        })
    }else{
        const data = productos[id-1]

        return res.json({
            data
        })
    }    
})

//PUT
    .put((req, res)=>{
    const {id} = req.params

    if(productos.length < id){
        return res.status(400).json({
            message: 'El producto a actualizar no existe'
        })
    }else{

        productos[id-1] = req.body
        return res.json({
            message:'Producto actualizado exitosamente',
            content: productos[id-1]
        })
    }
    //extraer el id
    //validar si existe esa posición en el arreglo
    //si existe, modificar con el body
    //si no existe, emitir un 400 indicando que el producto a actualizar no existe
})

    .delete((req, res)=> {
        const {id} = req.params;
        if (productos.length < id) {
            return res.json({
                message: "Producto a eliminar no existe",
            });
        } else {
            productos.splice(id - 1, 1);
            return res.json({
                message: "Producto eliminado exitosamente",
            })
        }
    });

servidor.listen(3000, () => {
    console.log("Servidor corriendo exitosamente en el puerto 3000")
})