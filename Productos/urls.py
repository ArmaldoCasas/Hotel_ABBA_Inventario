from django.urls import path
from .views import *

urlpatterns = [
    path('agregar_productos/', Agregar_Productos,name='agregar_productos'),
    path("listado_productos/",listado_productos,name="listado_productos"),
    path("listado_proveedores/",listado_proveedores,name="listado_proveedores"),
    path("listado_categorias/",listado_categorias,name="listado_categorias"),
    path('agregar_categorias/', agregar_categorias, name='agregar_categorias'),
    path('agregar_proveedores/', agregar_proveedores, name='agregar_proveedores'),
    path('agregar_ubicacion/', agregar_ubicacion, name='agregar_ubicacion'),
    path('listado_ubicacion/', listado_ubicacion, name='listado_ubicacion'),
    path('cambiar_estado/<int:producto_id>/', cambiar_estado_producto, name='cambiar_estado_producto'),
    path('editar_productos/<int:producto_id>/', editar_Productos,name="editar_productos"),
    path('eliminar_categoria/<int:categoria_id>/', eliminar_categoria, name='eliminar_categoria'),
    path('eliminar_proveedor/<int:proveedor_id>/', eliminar_proveedor, name='eliminar_proveedor')]
