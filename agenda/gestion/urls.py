from django.urls import path
from .views import EtiquetasApiView, inicio, PruebaApiView, TareasApiView


#seran todas las rutas de esta aplicacion las tendremos que registrar aca y solamente
urlpatterns = [
    path('inicio',inicio),
    path('prueba',PruebaApiView.as_view()),
    path('tareas',TareasApiView.as_view()),
    path('etiquetas', EtiquetasApiView.as_view()),
]