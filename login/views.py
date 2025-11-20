from login.models import Usuarios
from Productos.models import Producto
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

def create_user_view(request):
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
            #falta el crear una session
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request,"login/login.html")

def logout_view(request):
    # falta crear algo para cerrar sesión
    return redirect('login')

def dashboard_view(request):
    Productos = Producto.objects.all() 
    return render(request, 'login/dashboard.html',{
        "Productos": Productos 
    })
