from django.urls import path
from .views import listado_movimientos, ingreso, movimiento_ingreso, salida, movimiento_salida, detalle_movimiento

urlpatterns = [
    path("listado_movimientos/", listado_movimientos, name="listado_movimientos"),
    path("ingreso/", ingreso, name="ingreso"),
    path("movimiento_ingreso/<int:ingreso_id>/", movimiento_ingreso, name="movimiento_ingreso"),
    path("salida/", salida, name="salida"),
    path("movimiento_salida/", movimiento_salida, name="movimiento_salida"),
    path("detalle_movimiento_ingreso/<int:ingreso_id>/", detalle_movimiento, name="detalle_movimiento_ingreso"),
]
