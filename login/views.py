from login.models import Usuarios, Roles
from Productos.models import Producto
from Movimientos.models import Ingreso, Salida
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

def create_user_view(request):
    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')
    # verificar que el usuario tenga permisos
    if not 9 in request.session.get('permisos'):
        return redirect('inicio')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Evitar duplicados: comprobar si ya existe el usuario para que no de error de pagina
        if Usuarios.objects.filter(nombre=username).exists():
            messages.error(request, 'El nombre de usuario ya existe')
            return redirect('registrar')

        user = Usuarios(nombre=username)
        user.set_password(password)
        user.save()
        messages.success(request, 'Usuario creado exitosamente')
        return redirect('login')
        
    return render(request, 'login/registrar.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Autenticación manual usando el modelo Usuarios
        try:
            user = Usuarios.objects.get(nombre=username)
        except Usuarios.DoesNotExist:
            user = None

        if user and user.check_password(password):
            # guardar los permisos del usuario en la sesion
            if user.rol:
                request.session['permisos'] = user.rol.permisos

            # Guardar el id del usuario en la sesión
            if user.id:
                request.session['user_id'] = user.id
            else:
                request.session['user_id'] = None
            
            # Guardar el nombre del usuario en la sesión
            if user.nombre:
                request.session['user_name'] = user.nombre
            else:
                request.session['user_name'] = None

            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request,"login/login.html")

def logout_view(request):
    request.session.flush()
    return redirect('login')

def dashboard_view(request):
    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')
    # verificar que el usuario tenga permisos
    if not 1 in request.session.get('permisos'):
        return redirect('inicio')    
    Productos = Producto.objects.all()
    ultimos_ingresos = Ingreso.objects.all().order_by('-fecha')[:5]
    ultimos_salidas = Salida.objects.all().order_by('-fecha')[:5]
    return render(request, 'login/dashboard.html',{
        "Productos": Productos,
        "user_name": request.session.get('user_name'),
        "ultimos_ingresos": ultimos_ingresos,
        "ultimos_salidas": ultimos_salidas
    })

def inicio_view(request):
    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')
    return render(request, 'inicio.html')

def listado_usuarios(request):
    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')
    # verificar que el usuario tenga permisos
    if not 8 in request.session.get('permisos'):
        return redirect('inicio')
    
    usuarios = Usuarios.objects.all()
    return render(request, 'login/listado_usuarios.html', {'usuarios': usuarios})

def gestionar_roles(request):
    if not request.session.get('user_id'):
        return redirect('login')
    
    # Validar permiso de administrador (asumiendo que 9 es crear usuarios/gestionar usuarios)
    if not 10 in request.session.get('permisos', []):
        messages.error(request, 'No tienes permisos para gestionar roles')
        return redirect('listado_usuarios')

    if request.method == 'POST':
        rol_id = request.POST.get('rol_id')
        permisos_seleccionados = request.POST.getlist('permisos')
        
        # Convertir a enteros
        permisos_ints = [int(p) for p in permisos_seleccionados]
        
        try:
            rol = Roles.objects.get(id=rol_id)
            
            # Protección para el rol de Administrador
            if rol.nombre_rol == 'Administrador':
                messages.error(request, 'No se pueden modificar los permisos del Administrador')
                return redirect('gestionar_roles')
                
            rol.permisos = permisos_ints
            rol.save()
            messages.success(request, f'Permisos actualizados para {rol.nombre_rol}')
        except Roles.DoesNotExist:
            messages.error(request, 'Rol no encontrado')
            
        return redirect('gestionar_roles')

    roles = Roles.objects.all()
    
    
    # Diccionario de permisos basado en permisos_referencia.txt
    permisos_dict = {
        1: 'Dashboard',
        2: 'Listado de productos',
        3: 'Agregar nuevos productos',
        4: 'Listado de categorías',
        5: 'Agregar nuevas categorías',
        6: 'Listado de proveedores',
        7: 'Agregar nuevos proveedores',
        8: 'Listado de usuarios',
        9: 'Crear usuarios',
        10: 'Editar usuarios y gestionar roles',
        11: 'Listado de reportes',
        12: 'Listado de ubicaciones',
        13: 'Agregar nuevas ubicaciones',
    }
    
    return render(request, 'login/gestionar_roles.html', {
        'roles': roles,
        'permisos_dict': permisos_dict
    })

def editar_usuario(request, user_id):
    if not request.session.get('user_id'):
        return redirect('login')
        
    if not 10 in request.session.get('permisos', []):
        messages.error(request, 'No tienes permisos para editar usuarios')
        return redirect('listado_usuarios')

    try:
        usuario = Usuarios.objects.get(id=user_id)
    except Usuarios.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')
        return redirect('listado_usuarios')

    if request.method == 'POST':
        rol_id = request.POST.get('rol')
        if rol_id:
            try:
                rol = Roles.objects.get(id=rol_id)
                usuario.rol = rol
                usuario.save()
                messages.success(request, 'Rol de usuario actualizado')
            except Roles.DoesNotExist:
                messages.error(request, 'Rol no válido')
        else:
            usuario.rol = None
            usuario.save()
            messages.success(request, 'Rol removido del usuario')
            
        return redirect('listado_usuarios')

    roles = Roles.objects.all()
    return render(request, 'login/editar_usuario.html', {
        'usuario': usuario,
        'roles': roles
    })
