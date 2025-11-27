import datetime
import os
import time
import openpyxl
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import redirect, render
from Productos.models import Producto
from .models import Reporte

# Create your views here.

def listado_reportes(request):
    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')
    # verificar que el usuario tenga permisos
    if not 11 in request.session.get('permisos'):
        return redirect('error')
    reportes = Reporte.objects.all()
    return render(request, 'reportes/listado_reportes.html', {'reportes': reportes})

def export_inventory(request):
    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')

    # verificar que el usuario tenga permisos
    if not 11 in request.session.get('permisos'):
        return redirect('error')
    
    #verificar que hayan productos
    if not Producto.objects.exists():
        return redirect('inicio')
    
    # Evitar doble inserción (debounce de 5 segundos)
    current_time = time.time()
    last_export = request.session.get('last_export_time', 0)
    if current_time - last_export < 5:
        return redirect('listado_productos')

    #actualizar la fecha de la ultima exportacion
    request.session['last_export_time'] = current_time
    
    fecha_actual = datetime.datetime.now()

    #creamos el reporte
    reporte = Reporte.objects.create(
        nombre='Reporte de Stock',
        fecha=fecha_actual,
        usuario_id=request.session['user_id']
    )
    #creamos el archivo
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Stock de Productos'

    # Definir los encabezados de las columnas
    Titulos = ['ID', 'Nombre', "Precio","Umbral", 'Stock', 'Ubicacion', 'Contenido', 'Unidad', 'Categoria', 'Proveedores',"Estado"]
    worksheet.append(Titulos)

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
    #sacar numero de id reportes
    reporte_id = reporte.id
    
    # Asegurarse de que el directorio media exista
    if not os.path.exists('media'):
        os.makedirs('media')

    # Nombre del archivo
    filename = f'media/reporte_stock_{reporte_id}.xlsx'
    
    #guardar el reporte dentro de una carpeta dentro de media 
    workbook.save(filename)

    return response

def descargar_reporte(request, reporte_id):
    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')
    # verificar que el usuario tenga permisos
    if not 11 in request.session.get('permisos'):
        return redirect('error')
    
    filename = f'media/reporte_stock_{reporte_id}.xlsx'
    
    # verificar que el archivo existe
    if os.path.exists(filename):
        return FileResponse(open(filename, 'rb'), as_attachment=True, filename=f'reporte_stock_{reporte_id}.xlsx')
    else:
        raise Http404("El reporte no existe")