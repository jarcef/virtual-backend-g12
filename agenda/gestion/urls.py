from django.urls import path
from .views import inicio

#seran todas las rutas de esta aplicacion las tendremos que registrar aca y solamente
urlpatterns = [
    path('inicio',inicio)
]