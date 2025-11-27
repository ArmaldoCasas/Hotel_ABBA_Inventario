from django.urls import path
from .views import *
urlpatterns = [
    path('export_inventory', export_inventory, name='export_inventory'),
    path('listado_reportes', listado_reportes, name='listado_reportes'),
    path('descargar/<int:reporte_id>/', descargar_reporte, name='descargar_reporte'),
]