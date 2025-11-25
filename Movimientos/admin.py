from django.contrib import admin
from .models import Ingreso, MovimientoIngreso, Salida,MovimientoSalida

admin.site.register(Ingreso)
admin.site.register(MovimientoIngreso)
admin.site.register(Salida)
admin.site.register(MovimientoSalida)
# Register your models here.
