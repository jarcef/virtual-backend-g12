from django.urls import path
from .views import EtiquetasApiView, inicio, PruebaApiView, TareasApiView, TareaApiView, ArchivosApiView, EliminarArchivoApiView


#seran todas las rutas de esta aplicacion las tendremos que registrar aca y solamente
urlpatterns = [
    path('inicio',inicio),
    path('prueba',PruebaApiView.as_view()),
    path('tareas',TareasApiView.as_view()),
    path('etiquetas', EtiquetasApiView.as_view()),
    path('tarea/<int:pk>', TareaApiView.as_view()),
    path('subir-imagen', ArchivosApiView.as_view()),
    path('eliminar-imagen', EliminarArchivoApiView.as_view()),
]