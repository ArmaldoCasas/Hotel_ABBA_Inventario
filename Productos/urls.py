from django.urls import path
from .views import *

urlpatterns = [
    path('agregar_productos/', Agregar_Productos,name='agregar_productos'),
    path("listado_productos/",listado_productos,name="listado_productos"),
    path("listado_proveedores/",listado_proveedores,name="listado_proveedores"),
    path("listado_categorias/",listado_categorias,name="listado_categorias"),
    path('agregar_categorias/', agregar_categorias, name='agregar_categorias'),
    path('agregar_proveedores/', agregar_proveedores, name='agregar_proveedores'),]
