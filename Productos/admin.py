from django.contrib import admin
from .models import Categoria, Proveedor, Producto, ProveedorProducto,Ubicacion
# Register your models here.
admin.site.register(Categoria)
admin.site.register(ProveedorProducto)
admin.site.register(Proveedor)
admin.site.register(Producto)
admin.site.register(Ubicacion)