from flask_restful import Resource, request
from dtos.registro_dto import RegistroDTO, UsuarioResponseDTO, LoginDTO
from dtos.usuario_dto import ResetPasswordRequestDTO
from models.usuarios import Usuario
from config import conexion, sendgrid
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from os import environ
#from sendgrid.helpers.mail import Email, To, Content, Mail

class RegistroController(Resource):
    def post(self):
        body = request.get_json()       
        try:
            data = RegistroDTO().load(body)
            nuevoUsuario = Usuario(**data)
            nuevoUsuario.encriptar_pwd()
            conexion.session.add(nuevoUsuario)
            conexion.session.commit()
            respuesta = UsuarioResponseDTO().dump(nuevoUsuario)
            return {
                'message': 'Usuario registrado exitosamente',
                'content': respuesta
            }, 201

        except Exception as e:
            conexion.session.rollback()
            return {
                'message': 'Error al registrar al usuario',
                'content': e.args
            }, 400

class LoginController(Resource):
    def post(self):
        body = request.get_json()
            #Hacer un DTO qe solamente reciba un correo y un password, el correo debe de ser email, no es necesario usar un 
            #SQLAlchemyAutoSchema, solamente un validador  Schema

        try:
            data= LoginDTO().load(body)
            return {
               'message': 'Bienvenido'
            }
        except Exception as e:
            return{
                'message': 'Credenciales incorrectas',
                'content': e.args
            }

class ResetPasswordController(Resource):
    def post(self):
        body = request.get_json()
        mensaje = MIMEMultipart()
        email_emisor = environ.get('EMAIL_EMISOR')
        email_password = environ.get('EMAIL_PASSWORD')
        try:
            data = ResetPasswordRequestDTO().load(body)
            usuarioEncontrado = conexion.session.query(
                Usuario).filter_by(correo=data.get('correo')).first()
            if usuarioEncontrado is not None:
              #  texto = "Hola, es un mensaje de prueba."
                mensaje['Subject'] = 'Reiniciar contraseña Monedero APP'

                html = open('./email_templates/forgot-password.html').read().format(
                    usuarioEncontrado.nombre, usuarioEncontrado.correo, environ.get('URL_FRONT')
                )

                # Si queremos un generador con diseños https://beefree.io/
                # html='''
                # <html>
                #     <body>
                #         <p>                            
                #             Hola {}, has solicitado el reinicio de tu contraseña de tu cuenta {} ?
                #         </p>
                #         <p style="color: #ababab;">
                #             Si has sido tu, entonces dale clic al siguiente enlace: 
                #             <b><a href="{}/reset-password">link</a></b>
                #         </p>
                #         <p>
                #             Si no has sido tu entonces has caso omiso a este mensaje.
                #         </p>
                #         <br>
                #         <h3>
                #             Por favor no responder a este mensaje ya que es automático.
                #         </h3>
                #     </body>
                # </html>                
                # '''.format(usuarioEncontrado.nombre, usuarioEncontrado.correo, environ.get('URL_FRONT'))

               # mensaje.attach(MIMEText(texto,'plain'))
                mensaje.attach(MIMEText(html,'html'))
                # inicio el envio del correo
                # outlook > outlook.office365.com 
                # gmail > smtp.gmail.com 
                # icloud > smtp.mail.me.com 
                # yahoo > smtp.mail.yahoo.com

                emisorSMTP = SMTP('outlook.office365.com',587)
                emisorSMTP.starttls()
                #se hace el login de mi servidor de correo
                emisorSMTP.login(email_emisor, email_password)
                emisorSMTP.sendmail(
                    from_addr=email_emisor, 
                    to_addrs=usuarioEncontrado.correo,
                    msg=mensaje.as_string()
                )
                emisorSMTP.quit()
            return {
                'message': 'Correo enviado exitosamente'
            }
        except Exception as e:
            return {
                'message': 'Error al enviar el correo',
                'content': e.args
            }


        #---- Utilizando la libreria de python de mensajeria --------
        # try:
        #     data = ResetPasswordRequestDTO().load(body)
        #     usuarioEncontrado = conexion.session.query(Usuario).filter_by(correo=data.get('correo')).first()
        #     if usuarioEncontrado is not None:
        #         from_email = Email('juliarcef@gmail.com')
        #         to_email = To(usuarioEncontrado.correo)
        #         subject = 'Reinicia tu contraseña del monedero App'
        #         content = Content(
        #             'text/plain','Hola, has solicitado el reinicio de tu contraseña, has clic en el siguiente link para cambiar, sino has sido tu ignora este mensaje:.....')
        #         mail = Mail(from_email, to_email, subject, content)
        #         envia_correo = sendgrid.client.mail.send.post(
        #             request_body = mail.get())
        #         print(envia_correo.status_code)
        #         print(envia_correo.body)
        #         print(envia_correo._headers)
        #     return {
        #         'message': 'Correo enviado exitosamente'
        #     }
        # except Exception as e:
        #     return {
        #         'message': 'Error al resetear el password',
        #         'content': e.args
        #     }