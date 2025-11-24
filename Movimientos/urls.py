from django.urls import path
from .views import *

urlpatterns = [
    path("listado_movimientos/", listado_movimientos, name="listado_movimientos"),
    path("ingreso/", ingreso, name="ingreso"),
    path("movimiento_ingreso/<int:ingreso_id>/", movimiento_ingreso, name="movimiento_ingreso"),
    path("salida/", salida, name="salida"),
    path("movimiento_salida/", movimiento_salida, name="movimiento_salida"),
    path("detalle_movimiento_ingreso/<int:ingreso_id>/", detalle_movimiento_ingreso, name="detalle_movimiento_ingreso"),
    path("detalle_movimiento_salida/<int:salida_id>/", detalle_movimiento_salida, name="detalle_movimiento_salida"),
]
