from django.shortcuts import render, redirect, get_object_or_404
from .models import Ingreso, MovimientoIngreso, Salida, MovimientoSalida
from .forms import IngresoForm, MovimientoIngresoForm, SalidaForm, MovimientoSalidaForm
from Productos.models import Producto

def listado_movimientos(request):
    Movimientos_Ingreso = Ingreso.objects.all()
    Movimientos_Salida = Salida.objects.all()
    return render(request, "movimientos/listado_movimientos.html", {
        "titulo":"Listado de Movimientos",
        "Movimientos_Ingreso": Movimientos_Ingreso,
        "Movimientos_Salida": Movimientos_Salida
    })

def ingreso(request, ingreso_id=None):
    # Inicializar datos temporales de movimientos en sesión
    if 'movimientos_temp' not in request.session:
        request.session['movimientos_temp'] = []

    movimientos_temp = request.session.get('movimientos_temp', [])

    if request.method == 'POST':
        if 'guardar_ingreso' in request.POST:
            # Guardar ingreso y movimientos en DB
            ingreso_id = request.session.get('ingreso_id')
            if ingreso_id:
                ingreso = Ingreso.objects.get(id=ingreso_id)
            else:
                return redirect('ingreso')  # No ingreso_id, algo salió mal, regresar

            for mov in movimientos_temp:
                movimiento = MovimientoIngreso()
                movimiento.ingreso = ingreso
                movimiento.producto_id = mov['producto_id']
                movimiento.cantidad = mov['cantidad']
                movimiento.precio_unitario = mov['precio_unitario']
                movimiento.save()
                # Actualizar stock Producto
                producto = Producto.objects.get(id=mov['producto_id'])
                producto.stock += mov['cantidad']
                producto.save()
            # Limpiar session
            request.session['movimientos_temp'] = []
            request.session['ingreso_id'] = None
            return redirect('listado_movimientos')

        elif 'guardar_datos_ingreso' in request.POST:
            # Crear y guardar ingreso en DB para obtener ingreso_id inmediato
            form_ingreso = IngresoForm(request.POST)
            if form_ingreso.is_valid():
                ingreso = form_ingreso.save()
                request.session['ingreso_id'] = ingreso.id
                request.session.modified = True
                return redirect('movimiento_ingreso', ingreso_id=ingreso.id)
        else:
            form_ingreso = IngresoForm()
    else:
        ingreso_id = request.session.get('ingreso_id')
        if ingreso_id:
            try:
                ingreso_instance = Ingreso.objects.get(id=ingreso_id)
                form_ingreso = IngresoForm(instance=ingreso_instance)
            except Ingreso.DoesNotExist:
                form_ingreso = IngresoForm()
        else:
            form_ingreso = IngresoForm()

    return render(request, 'movimientos/ingresos/ingreso.html', {
        'form_ingreso': form_ingreso,
        'movimientos': movimientos_temp,
        'ingreso_id': request.session.get('ingreso_id'),
    })

def movimiento_ingreso(request, ingreso_id):
    # Limpiar session previa movimientos para evitar Decimal no serializable
    if 'movimientos_temp' not in request.session or not request.session['movimientos_temp']:
        request.session['movimientos_temp'] = []
    else:
        # Asegurar convertir precios a float en movimientos ya guardados
        movimientos_temp = request.session.get('movimientos_temp', [])
        for mov in movimientos_temp:
            if isinstance(mov.get('precio_unitario'), float):
                continue
            mov['precio_unitario'] = float(mov.get('precio_unitario'))
        request.session['movimientos_temp'] = movimientos_temp
        request.session.modified = True

    if request.method == 'POST':
        form_movimiento = MovimientoIngresoForm(request.POST)
        if form_movimiento.is_valid():
            movimiento_data = {
                'producto_id': form_movimiento.cleaned_data['producto'].id,
                'producto_nombre': str(form_movimiento.cleaned_data['producto']),
                'cantidad': float(form_movimiento.cleaned_data['cantidad']),
                'precio_unitario': float(form_movimiento.cleaned_data['precio_unitario']),
            }
            movimientos_temp = request.session.get('movimientos_temp', [])
            movimientos_temp.append(movimiento_data)
            request.session['movimientos_temp'] = movimientos_temp
            request.session.modified = True
            return redirect('ingreso')
    else:
        form_movimiento = MovimientoIngresoForm()
    return render(request, 'movimientos/ingresos/movimiento_ingreso.html', {
        'form_movimiento': form_movimiento,
    })


def salida(request):
    # Inicializar datos temporales de movimientos en sesión
    if 'movimientos_salida_temp' not in request.session:
        request.session['movimientos_salida_temp'] = []

    movimientos_salida_temp = request.session.get('movimientos_salida_temp', [])

    if request.method == 'POST':
        if 'guardar_salida' in request.POST:
            salida_id = request.session.get('salida_id')
            if salida_id:
                salida = Salida.objects.get(id=salida_id)
            else:
                return redirect('salida')
            
            for mov in movimientos_salida_temp:
                movimiento = MovimientoSalida()
                movimiento.salida = salida
                movimiento.producto_id = mov['producto_id']
                movimiento.cantidad = mov['cantidad']
                movimiento.save()
                # Actualizar stock Producto
                producto = Producto.objects.get(id=mov['producto_id'])
                producto.stock -= mov['cantidad']
                producto.save()

            # Limpiar session
            request.session['movimientos_salida_temp'] = []
            request.session['salida_id'] = None
            return redirect('listado_movimientos')

        elif 'guardar_datos_salida' in request.POST:
            form_salida = SalidaForm(request.POST)
            if form_salida.is_valid():
                salida = form_salida.save()
                request.session['salida_id'] = salida.id
                request.session.modified = True
                return redirect('movimiento_salida')
        else:
            form_salida = SalidaForm()
    else:
        salida_id = request.session.get('salida_id')
        if salida_id:
            try:
                salida_instance = Salida.objects.get(id=salida_id)
                form_salida = SalidaForm(instance=salida_instance)
            except Salida.DoesNotExist:
                form_salida = SalidaForm()
        else:
            form_salida = SalidaForm()

    return render(request, "movimientos/salidas/salida.html", {
        'form_salida': form_salida,
        'movimientos': movimientos_salida_temp,
        'salida_id': request.session.get('salida_id'),
    })

def movimiento_salida(request):
    if 'movimientos_salida_temp' not in request.session:
        request.session['movimientos_salida_temp'] = []
    else:
        movimientos_salida_temp = request.session.get('movimientos_salida_temp', [])
        request.session['movimientos_salida_temp'] = movimientos_salida_temp
        request.session.modified = True

    if request.method == 'POST':
        form_movimiento = MovimientoSalidaForm(request.POST)
        if form_movimiento.is_valid():
            movimiento_data = {
                'producto_id': form_movimiento.cleaned_data['producto'].id,
                'producto_nombre': str(form_movimiento.cleaned_data['producto']),
                'cantidad': float(form_movimiento.cleaned_data['cantidad']),
            }
            movimientos_salida_temp = request.session.get('movimientos_salida_temp', [])
            movimientos_salida_temp.append(movimiento_data)
            request.session['movimientos_salida_temp'] = movimientos_salida_temp
            request.session.modified = True
            return redirect('salida')
    else:
        form_movimiento = MovimientoSalidaForm()

    return render(request, "movimientos/salidas/movimiento_salida.html", {
        'form_movimiento': form_movimiento,
    })

def detalle_movimiento_ingreso(request, ingreso_id):
    ingreso = get_object_or_404(Ingreso, id=ingreso_id)
    movimientos_qs = ingreso.movimientoingreso_set.all()
    movimientos = []
    for movimiento in movimientos_qs:
        mov_dict = {
            'producto': movimiento.producto,
            'cantidad': movimiento.cantidad,
            'precio_unitario': movimiento.precio_unitario,
            'subtotal': movimiento.cantidad * movimiento.precio_unitario,
        }
        movimientos.append(mov_dict)
    return render(request, "movimientos/ingresos/detalle_movimiento_ingreso.html", {
        "ingreso": ingreso,
        "movimientos": movimientos
    })

def detalle_movimiento_salida(request, salida_id):
    salida = get_object_or_404(Salida, id=salida_id)
    movimientos_qs = salida.movimientosalida_set.all()
    movimientos = []
    for movimiento in movimientos_qs:
        mov_dict = {
            'producto': movimiento.producto,
            'cantidad': movimiento.cantidad,
        }
        movimientos.append(mov_dict)
    return render(request, "movimientos/salidas/detalle_movimiento_salida.html", {
        "salida": salida,
        "movimientos": movimientos
    })

###