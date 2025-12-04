from django.shortcuts import render, redirect, get_object_or_404
from .models import Ingreso, MovimientoIngreso, Salida, MovimientoSalida
from .forms import IngresoForm, MovimientoIngresoForm, SalidaForm, MovimientoSalidaForm
from Productos.models import Producto
from login.models import Usuarios

def listado_movimientos(request):
    if not request.session.get('user_id'):
        return redirect('login')
    if 14 not in request.session.get('permisos', []):
        return redirect('listado_movimientos')
    
    Movimientos_Ingreso = Ingreso.objects.all().order_by('-fecha')[:5]
    Movimientos_Salida = Salida.objects.all().order_by('-fecha')[:5]
    return render(request, "movimientos/listado_movimientos.html", {
        "titulo":"Listado de Movimientos",
        "Movimientos_Ingreso": Movimientos_Ingreso,
        "Movimientos_Salida": Movimientos_Salida
    })

def ingreso(request, ingreso_id=None):
    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')
    # verificar que el usuario tenga permisos
    if 14 not in request.session.get('permisos', []):
        return redirect('listado_movimientos')
    
    # Inicializar datos temporales de movimientos en sesión
    if 'movimientos_temp' not in request.session:
        request.session['movimientos_temp'] = []

    movimientos_temp = request.session.get('movimientos_temp', [])

    if request.method == 'POST':
        if 'guardar_ingreso' in request.POST:
            # Validar que haya al menos 1 producto
            if not movimientos_temp:
                return render(request, 'movimientos/ingresos/ingreso.html', {
                    'form_ingreso': form_ingreso if 'form_ingreso' in locals() else IngresoForm(),
                    'movimientos': movimientos_temp,
                    'ingreso_id': request.session.get('ingreso_id'),
                    'error': 'Debe agregar al menos 1 producto antes de guardar el ingreso.',
                })
            
            # verificar permisos antes de guardar ingreso
            if 14 not in request.session.get('permisos', []):
                return redirect('listado_movimientos')
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

        elif 'eliminar_producto_ingreso' in request.POST:
            # Eliminar producto de la lista temporal
            indice = request.POST.get('indice')
            if indice:
                try:
                    movimientos_temp = request.session.get('movimientos_temp', [])
                    del movimientos_temp[int(indice)]
                    request.session['movimientos_temp'] = movimientos_temp
                    request.session.modified = True
                except (IndexError, ValueError):
                    pass
            return redirect('ingreso')

        elif 'guardar_edicion_ingreso' in request.POST:
            # Editar producto existente en la lista temporal
            indice = request.POST.get('indice')
            cantidad = request.POST.get('cantidad')
            precio_unitario = request.POST.get('precio_unitario')
            if indice and cantidad and precio_unitario:
                try:
                    movimientos_temp = request.session.get('movimientos_temp', [])
                    movimientos_temp[int(indice)]['cantidad'] = float(cantidad)
                    movimientos_temp[int(indice)]['precio_unitario'] = float(precio_unitario)
                    request.session['movimientos_temp'] = movimientos_temp
                    request.session.modified = True
                except (IndexError, ValueError):
                    pass
            return redirect('ingreso')

        elif 'guardar_datos_ingreso' in request.POST:
            # Crear y guardar ingreso en DB para obtener ingreso_id inmediato
            form_ingreso = IngresoForm(request.POST)
            if form_ingreso.is_valid():
                ingreso = form_ingreso.save(commit=False)
                # Asignar el usuario logueado
                user_id = request.session.get('user_id')
                if user_id:
                    try:
                        usuario = Usuarios.objects.get(id=user_id)
                        ingreso.usuario = usuario
                    except Usuarios.DoesNotExist:
                        pass
                ingreso.save()
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
        'error': None,
    })

def movimiento_ingreso(request, ingreso_id):
    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')
    # verificar que el usuario tenga permisos
    if 14 not in request.session.get('permisos', []):
        return redirect('listado_movimientos')
    
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
    
    # Procesar formulario de nuevo movimiento
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

    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')
    # verificar que el usuario tenga permisos
    if 15 not in request.session.get('permisos', []):
        return redirect('listado_movimientos')
    
    # Inicializar datos temporales de movimientos en sesión
    if 'movimientos_salida_temp' not in request.session:
        request.session['movimientos_salida_temp'] = []

    movimientos_salida_temp = request.session.get('movimientos_salida_temp', [])

    if request.method == 'POST':
        if 'guardar_salida' in request.POST:
            # Validar que haya al menos 1 producto
            if not movimientos_salida_temp:
                return render(request, 'movimientos/salidas/salida.html', {
                    'form_salida': form_salida if 'form_salida' in locals() else SalidaForm(),
                    'movimientos': movimientos_salida_temp,
                    'salida_id': request.session.get('salida_id'),
                    'error': 'Debe agregar al menos 1 producto antes de guardar la salida.',
                })
            
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

        elif 'eliminar_producto_salida' in request.POST:
            # Eliminar producto de la lista temporal
            indice = request.POST.get('indice')
            if indice:
                try:
                    movimientos_salida_temp = request.session.get('movimientos_salida_temp', [])
                    del movimientos_salida_temp[int(indice)]
                    request.session['movimientos_salida_temp'] = movimientos_salida_temp
                    request.session.modified = True
                except (IndexError, ValueError):
                    pass
            return redirect('salida')

        elif 'guardar_edicion_salida' in request.POST:
            # Editar producto existente en la lista temporal
            indice = request.POST.get('indice')
            cantidad = request.POST.get('cantidad')
            if indice and cantidad:
                try:
                    movimientos_salida_temp = request.session.get('movimientos_salida_temp', [])
                    movimientos_salida_temp[int(indice)]['cantidad'] = float(cantidad)
                    request.session['movimientos_salida_temp'] = movimientos_salida_temp
                    request.session.modified = True
                except (IndexError, ValueError):
                    pass
            return redirect('salida')

        elif 'guardar_datos_salida' in request.POST:
            form_salida = SalidaForm(request.POST)
            if form_salida.is_valid():
                salida = form_salida.save(commit=False)
                # Asignar el usuario logueado
                user_id = request.session.get('user_id')
                if user_id:
                    try:
                        usuario = Usuarios.objects.get(id=user_id)
                        salida.usuario = usuario
                    except Usuarios.DoesNotExist:
                        pass
                salida.save()
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
        'error': None,
    })

def movimiento_salida(request):
    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')
    # verificar que el usuario tenga permisos
    if 15 not in request.session.get('permisos', []):
        return redirect('listado_movimientos')
    
    # Limpiar session previa movimientos para evitar Decimal no serializable
    if 'movimientos_salida_temp' not in request.session:
        request.session['movimientos_salida_temp'] = []
    else:
        movimientos_salida_temp = request.session.get('movimientos_salida_temp', [])
        request.session['movimientos_salida_temp'] = movimientos_salida_temp
        request.session.modified = True

    if request.method == 'POST':
        form_movimiento = MovimientoSalidaForm(request.POST)
        if form_movimiento.is_valid():
            producto = form_movimiento.cleaned_data['producto']
            cantidad_val = float(form_movimiento.cleaned_data['cantidad'])

            movimientos_salida_temp = request.session.get('movimientos_salida_temp', [])

            # Verificar si ya existe un movimiento para este producto en la salida actual
            if any(mov.get('producto_id') == producto.id for mov in movimientos_salida_temp):
                form_movimiento.add_error('producto', 'Ya existe un movimiento para este producto en la salida actual.')
            else:
                movimiento_data = {
                    'producto_id': producto.id,
                    'producto_nombre': str(producto),
                    'cantidad': cantidad_val,
                }
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
    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')
    # verificar que el usuario tenga permisos
    if 18 not in request.session.get('permisos', []):
        return redirect('listado_movimientos')
    
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
    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')
    # verificar que el usuario tenga permisos
    if 19 not in request.session.get('permisos', []):
        return redirect('listado_movimientos')
    
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

def listado_movimientos_ingreso(request):
    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')
    # verificar que el usuario tenga permisos
    if 16 not in request.session.get('permisos', []):
        return redirect('listado_movimientos')
    
    movimientos_ingreso = Ingreso.objects.all().order_by('-fecha')
    return render(request, "movimientos/ingresos/listado_movimientos_ingreso.html", {
        "movimientos_ingreso": movimientos_ingreso
    })

def listado_movimientos_salida(request):
    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')
    # verificar que el usuario tenga permisos
    if 17 not in request.session.get('permisos', []):
        return redirect('listado_movimientos')
    
    movimientos_salida = Salida.objects.all().order_by('-fecha')
    return render(request, "movimientos/salidas/listado_movimientos_salida.html", {
        "movimientos_salida": movimientos_salida
    })
