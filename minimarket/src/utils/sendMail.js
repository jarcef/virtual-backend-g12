import nodemailer from "nodemailer";

const trasporter = nodemailer.createTransport({
    host: "smtp.gmail.com",
    port: 587,
    auth: { 
        user: process.env.EMAIL_ACCOUNT,
        pass: process.env.EMAIL_PASSWORD,
    },
});

export const enviarCorreoValidacion = async ({ destinatario, hash }) => {
    const html = `
    <p>
        Hola para comenzar a disfrutar de todas las ofertas en nuestro minimarket, por favor has clic en el siguiente enlace
            <a href="${process.env.FRONTEND_URL}?hash=${hash}">
                Valida mi cuenta
            </a>
    <p>`;
try {
    await trasporter.sendMail({
        from: "juliarcef@gmail.com",
        to: destinatario,
        subject: "Validacion del Correo del Minimarket APP",
        html,
    });
    console.log("Correo enviado exitosamente");
}catch (error) {
    console.log(error);
    return error;
}
};








