import { Prisma } from  "../prisma.js";

export const crearProducto = async (req, res) => {
    console.log("Yo me ejecuto primero");

    try {       
        const nuevoProducto = await Prisma.producto.create({ data: req.body});
        console.log(nuevoProducto);
        console.log("Yo me ejecuto al último");

        return res.json({
            message: "Producto agregado exitosamente",
            content: nuevoProducto,
        });

    } catch (e) {
        console.log(e);
        return res.json({
            message: "Error al crear el producto",
        });
    }    
};

export const listarProductos = async (req, res) => {
    const productos = await Prisma.producto.findMany({});

    return res.json({
        content: productos,
    });
};

export const actualizarProducto = async (req, res) => {
    const { id } = req.params;
    try{    
        const productoEncontrado = await Prisma.producto.findUnique({
            where: { id: +id },
            rejectOnNotFound: true,
    });
    console.log(productoEncontrado);

    const productoActualizado = await Prisma.producto.update({ 
        data: req.body,
        where: { id: productoEncontrado.id},
    });

    return res.json({
        message: "Producto actualizado exitosamente",
        content: productoActualizado,
    });
    } catch (e){
        console.log(e);
        return res.json({
            message: "Error al actualizar el producto",
        });
    }
};

export const eliminarProducto = async (req, res) => {
    const { id } = req.params;

    try {
        const productoEncontrado = await Prisma.producto.findUnique({ 
            where: { id: Number(id) },
            select: { id: true },
        });

        await Prisma.producto.delete({ where: { id: productoEncontrado.id } });
        
        return res.json({
            message: "Producto eliminado exitosamente",
        });
    } catch (error) {
        return res.json({
            message: "Error al eliminar el producto",
        });
    }
};