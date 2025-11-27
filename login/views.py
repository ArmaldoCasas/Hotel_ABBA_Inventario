from login.models import Usuarios, Roles
from Productos.models import Producto
from Movimientos.models import Ingreso, Salida
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

def create_user_view(request):
    #if not 9 in request.session.get('permisos'):
    #    messages.error(request, 'No tienes permisos para crear usuarios')
    #    return redirect('inicio')

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
    if not 1 in request.session.get('permisos'):
        messages.error(request, 'No tienes permisos para acceder a esta pagina')
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
    if not request.session.get('user_id'):
        messages.error(request, 'No tienes permisos para acceder a esta pagina')
        return redirect('login')
    
    return render(request, 'inicio.html')

def listado_usuarios(request):
    if not request.session.get('user_id'):
        return redirect('login')
    
    # Aquí podrías agregar validación de permisos si es necesario
    if not 8 in request.session.get('permisos'):
        messages.error(request, 'No tienes permisos para acceder a esta pagina')
        return redirect('inicio')
    
    usuarios = Usuarios.objects.all()
    return render(request, 'login/listado_usuarios.html', {'usuarios': usuarios})
