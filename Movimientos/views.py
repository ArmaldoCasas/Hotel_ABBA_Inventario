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
                    'datos_guardados': bool(request.session.get('ingreso_temp')),
                    'error': 'Debe agregar al menos 1 producto antes de guardar el ingreso.',
                })
            
            # verificar permisos antes de guardar ingreso
            if 14 not in request.session.get('permisos', []):
                return redirect('listado_movimientos')
            
            # Obtener datos de sesión
            ingreso_temp = request.session.get('ingreso_temp')
            if not ingreso_temp:
                return redirect('ingreso')  # No hay datos, algo salió mal
            
            # Crear ingreso con datos de sesión
            ingreso = Ingreso(
                proveedor_id=ingreso_temp['proveedor_id'],
                tipo_documento=ingreso_temp['tipo_documento'],
                numero_documento=ingreso_temp['numero_documento']
            )
            # Asignar el usuario logueado
            user_id = request.session.get('user_id')
            if user_id:
                try:
                    usuario = Usuarios.objects.get(id=user_id)
                    ingreso.usuario = usuario
                except Usuarios.DoesNotExist:
                    pass
            ingreso.save()
            
            # Crear movimientos
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
            del request.session['ingreso_temp']
            request.session.modified = True
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
            error_edicion = None
            
            if indice and cantidad and precio_unitario:
                try:
                    movimientos_temp = request.session.get('movimientos_temp', [])
                    indice_int = int(indice)
                    cantidad_float = float(cantidad)
                    precio_float = float(precio_unitario)
                    
                    # Validar que los valores sean positivos
                    if cantidad_float <= 0:
                        error_edicion = 'La cantidad debe ser un número positivo mayor que 0.'
                    elif precio_float <= 0:
                        error_edicion = 'El precio unitario debe ser un número positivo mayor que 0.'
                    else:
                        # Si son válidos, actualizar
                        movimientos_temp[indice_int]['cantidad'] = cantidad_float
                        movimientos_temp[indice_int]['precio_unitario'] = precio_float
                        request.session['movimientos_temp'] = movimientos_temp
                        request.session.modified = True
                        return redirect('ingreso')
                except (IndexError, ValueError):
                    error_edicion = 'Error al procesar la edición. Intente nuevamente.'
            
            # Si hay error, mostrar la página con el error
            if error_edicion:
                ingreso_temp = request.session.get('ingreso_temp')
                return render(request, 'movimientos/ingresos/ingreso.html', {
                    'form_ingreso': IngresoForm(initial={
                        'proveedor': ingreso_temp.get('proveedor_id'),
                        'tipo_documento': ingreso_temp.get('tipo_documento'),
                        'numero_documento': ingreso_temp.get('numero_documento'),
                    }) if ingreso_temp else IngresoForm(),
                    'movimientos': movimientos_temp,
                    'datos_guardados': bool(request.session.get('ingreso_temp')),
                    'error': error_edicion,
                })
            return redirect('ingreso')

        elif 'guardar_datos_ingreso' in request.POST:
            # Validar y guardar datos temporales en sesión
            form_ingreso = IngresoForm(request.POST)
            if form_ingreso.is_valid():
                # Guardar solo IDs en sesión (son serializables)
                request.session['ingreso_temp'] = {
                    'proveedor_id': form_ingreso.cleaned_data['proveedor'].id,
                    'tipo_documento': form_ingreso.cleaned_data['tipo_documento'],
                    'numero_documento': form_ingreso.cleaned_data['numero_documento'],
                }
                request.session.modified = True
                return redirect('movimiento_ingreso')
            else:
                # Si no válido, render con errores
                return render(request, 'movimientos/ingresos/ingreso.html', {
                    'form_ingreso': form_ingreso,
                    'movimientos': movimientos_temp,
                    'datos_guardados': bool(request.session.get('ingreso_temp')),
                    'error': None,
                })
        else:
            form_ingreso = IngresoForm()
    else:
        ingreso_temp = request.session.get('ingreso_temp')
        if ingreso_temp:
            # Reconstruir form con datos de sesión
            form_ingreso = IngresoForm(initial={
                'proveedor': ingreso_temp.get('proveedor_id'),
                'tipo_documento': ingreso_temp.get('tipo_documento'),
                'numero_documento': ingreso_temp.get('numero_documento'),
            })
        else:
            form_ingreso = IngresoForm()

    return render(request, 'movimientos/ingresos/ingreso.html', {
        'form_ingreso': form_ingreso,
        'movimientos': movimientos_temp,
        'datos_guardados': bool(request.session.get('ingreso_temp')),
        'error': None,
    })

def movimiento_ingreso(request):
    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')
    # verificar que el usuario tenga permisos
    if 14 not in request.session.get('permisos', []):
        return redirect('listado_movimientos')
    
    try:
        # Si no hay ingreso_temp en sesión, regresar a ingreso
        ingreso_temp = request.session.get('ingreso_temp')
        if not ingreso_temp:
            return redirect('ingreso')
        
        # Obtener el proveedor_id de la sesión
        proveedor_id = ingreso_temp.get('proveedor_id')
        print(f"DEBUG: proveedor_id = {proveedor_id}")
        print(f"DEBUG: ingreso_temp = {ingreso_temp}")
        
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
            form_movimiento = MovimientoIngresoForm(request.POST, proveedor_id=proveedor_id)
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
            # Si no válido, continúa al render con el form que tiene errores
        else:
            form_movimiento = MovimientoIngresoForm(proveedor_id=proveedor_id)
            # Debug: mostrar cantidad de productos en el queryset
            print(f"DEBUG: Total productos en queryset = {form_movimiento.fields['producto'].queryset.count()}")
        
        return render(request, 'movimientos/ingresos/movimiento_ingreso.html', {
            'form_movimiento': form_movimiento,
        })
    except Exception as e:
        # Si ocurre cualquier error, redirigir a ingreso
        print(f"Error en movimiento_ingreso: {str(e)}")
        import traceback
        traceback.print_exc()
        return redirect('ingreso')


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
            
            # Obtener datos de sesión
            salida_temp = request.session.get('salida_temp')
            if not salida_temp:
                return redirect('salida')  # No hay datos, algo salió mal
            
            # Crear salida con datos de sesión
            salida = Salida(
                motivo=salida_temp['motivo']
            )
            # Asignar el usuario logueado
            user_id = request.session.get('user_id')
            if user_id:
                try:
                    usuario = Usuarios.objects.get(id=user_id)
                    salida.usuario = usuario
                except Usuarios.DoesNotExist:
                    pass
            salida.save()
            
            # Crear movimientos
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
            del request.session['salida_temp']
            request.session.modified = True
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
            error_edicion = None
            
            if indice and cantidad:
                try:
                    movimientos_salida_temp = request.session.get('movimientos_salida_temp', [])
                    indice_int = int(indice)
                    cantidad_float = float(cantidad)
                    
                    # Validar que la cantidad sea un entero
                    if cantidad_float != int(cantidad_float):
                        error_edicion = 'La cantidad debe ser un número entero.'
                    # Validar que la cantidad sea positiva
                    elif cantidad_float <= 0:
                        error_edicion = 'La cantidad debe ser un número positivo mayor que 0.'
                    else:
                        # Obtener el producto de la sesión
                        movimiento = movimientos_salida_temp[indice_int]
                        producto = Producto.objects.get(id=movimiento['producto_id'])
                        
                        # Validar stock disponible
                        if cantidad_float > producto.stock:
                            error_edicion = f'La cantidad solicitada ({int(cantidad_float)}) supera el stock disponible ({producto.stock}) del producto {producto.nombre}.'
                        else:
                            # Si es válido, actualizar
                            movimientos_salida_temp[indice_int]['cantidad'] = int(cantidad_float)
                            request.session['movimientos_salida_temp'] = movimientos_salida_temp
                            request.session.modified = True
                            return redirect('salida')
                except (IndexError, ValueError):
                    error_edicion = 'Error al procesar la edición. Intente nuevamente.'
                except Producto.DoesNotExist:
                    error_edicion = 'El producto no existe. Intente nuevamente.'
            
            # Si hay error, mostrar la página con el error
            if error_edicion:
                return render(request, 'movimientos/salidas/salida.html', {
                    'form_salida': SalidaForm(initial={
                        'motivo': request.session.get('salida_temp', {}).get('motivo', ''),
                    }) if request.session.get('salida_temp') else SalidaForm(),
                    'movimientos': movimientos_salida_temp,
                    'datos_guardados': bool(request.session.get('salida_temp')),
                    'error': error_edicion,
                })
            return redirect('salida')

        elif 'guardar_datos_salida' in request.POST:
            # Validar y guardar datos temporales en sesión
            form_salida = SalidaForm(request.POST)
            if form_salida.is_valid():
                # Guardar motivo en sesión
                request.session['salida_temp'] = {
                    'motivo': form_salida.cleaned_data['motivo'],
                }
                request.session.modified = True
                return redirect('movimiento_salida')
            else:
                # Si no válido, render con errores
                return render(request, 'movimientos/salidas/salida.html', {
                    'form_salida': form_salida,
                    'movimientos': movimientos_salida_temp,
                    'datos_guardados': bool(request.session.get('salida_temp')),
                    'error': None,
                })
        else:
            form_salida = SalidaForm()
    else:
        salida_temp = request.session.get('salida_temp')
        if salida_temp:
            form_salida = SalidaForm(initial={
                'motivo': salida_temp.get('motivo'),
            })
        else:
            form_salida = SalidaForm()

    return render(request, "movimientos/salidas/salida.html", {
        'form_salida': form_salida,
        'movimientos': movimientos_salida_temp,
        'datos_guardados': bool(request.session.get('salida_temp')),
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

            # Validar que la cantidad sea un entero
            if cantidad_val != int(cantidad_val):
                form_movimiento.add_error('cantidad', 'La cantidad debe ser un número entero.')
            # Verificar si ya existe un movimiento para este producto en la salida actual
            elif any(mov.get('producto_id') == producto.id for mov in request.session.get('movimientos_salida_temp', [])):
                form_movimiento.add_error('producto', 'Ya existe un movimiento para este producto en la salida actual.')
            else:
                movimiento_data = {
                    'producto_id': producto.id,
                    'producto_nombre': str(producto),
                    'cantidad': int(cantidad_val),
                }
                movimientos_salida_temp = request.session.get('movimientos_salida_temp', [])
                movimientos_salida_temp.append(movimiento_data)
                request.session['movimientos_salida_temp'] = movimientos_salida_temp
                request.session.modified = True
                return redirect('salida')
        # Si no válido, continúa al render con el form que tiene errores
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
