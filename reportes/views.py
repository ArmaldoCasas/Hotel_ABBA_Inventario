import openpyxl
from django.http import HttpResponse
from django.shortcuts import render
from Productos.models import Producto  # Importamos el modelo de donde sacamos los datos
from .models import Reporte
# Create your views here.
def export_inventory(request):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Stock de Productos'

    # Definir los encabezados de las columnas
    Titulos = ['ID', 'Nombre', "Precio","Umbral", 'Stock', 'Ubicacion', 'Contenido', 'Unidad', 'Categoria', 'Proveedores',"Estado"]
    worksheet.append(Titulos)

    # Obtener los datos de la base de datos
    # Traemos todos los productos para listarlos
    productos = Producto.objects.all()

    # Escribir los datos en la hoja
    for producto in productos:
        ubicacion = producto.ubicacion.nombre if producto.ubicacion else 'N/A'
        categoria = producto.categoria.nombre if producto.categoria else 'N/A'
        proveedores = ', '.join([p.nombre for p in producto.proveedores.all()])
        row = [
            producto.id,
            producto.nombre,
            producto.precio,
            producto.umbral,
            producto.stock,
            ubicacion,
            producto.contenido,
            producto.unidad,
            categoria,
            proveedores,
            producto.esta_activo,
        ]
        worksheet.append(row)
    # Le decimos al navegador que esto es un archivo Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    # Definimos el nombre del archivo que se descargará
    response['Content-Disposition'] = 'attachment; filename="reporte_stock.xlsx"'

    #Guardar el libro en la respuesta
    workbook.save(response)
    
    return response