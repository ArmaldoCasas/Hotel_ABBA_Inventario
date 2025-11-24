from django.shortcuts import render, redirect
from .models import Producto, Categoria, Proveedor, Ubicacion
from .forms import ProductoForm, CategoriaForm, ProveedorForm, UbicacionForm

# Create your views here.

def listado_productos(request):

    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')

    # verificar que el usuario tenga permisos
    if not 2 in request.session.get('permisos'):
        return redirect('inicio')

    Productos = Producto.objects.all()
    Categorias = Categoria.objects.all()
    Proveedores = Proveedor.objects.all()
    Ubicaciones = Ubicacion.objects.all()

    # Filtros
    nombre = request.GET.get('nombre')
    categoria_id = request.GET.get('categoria')
    proveedor_id = request.GET.get('proveedor')
    ubicacion_id = request.GET.get('ubicacion')

    if nombre:
        Productos = Productos.filter(nombre__icontains=nombre)
    
    if categoria_id:
        Productos = Productos.filter(categoria_id=categoria_id)
        
    if proveedor_id:
        Productos = Productos.filter(proveedores__id=proveedor_id)

    if ubicacion_id:
        Productos = Productos.filter(ubicacion_id=ubicacion_id)

    return render(request,"productos/listado_productos.html",{
        "titulo":"Listado de Productos",
        "Productos": Productos,
        "Categorias": Categorias,
        "Proveedores": Proveedores,
        "Ubicaciones": Ubicaciones
    })

    
def Agregar_Productos(request):
    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')

    # verificar que el usuario tenga permisos
    if not 3 in request.session.get('permisos'):
        return redirect('inicio')

    if request.method == "POST":
        formulario_productos = ProductoForm(request.POST)
        if formulario_productos.is_valid():
            formulario_productos.save()
            return redirect("agregar_productos")    
    else:
        formulario_productos=ProductoForm()
    return render(request, "productos/agregar_productos.html", {"formulario_productos":formulario_productos})

def listado_categorias(request):
    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')

    # verificar que el usuario tenga permisos
    if not 4 in request.session.get('permisos'):
        return redirect('inicio')

    Categorias = Categoria.objects.all() 
    return render(request,"productos/listado_categorias.html",{
        "titulo":"Listado de Productos",
        "Categorias": Categorias 
    })

def agregar_categorias(request):

    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')

    # verificar que el usuario tenga permisos
    if not 5 in request.session.get('permisos'):
        return redirect('inicio')

    if request.method == 'POST':
        formulario_categorias = CategoriaForm(request.POST)
        if formulario_categorias.is_valid():
            formulario_categorias.save()
            return redirect("agregar_categorias") 
    else:
        formulario_categorias = CategoriaForm()
    
    return render(request, 'productos/agregar_categorias.html', {'formulario_categorias': formulario_categorias})

def listado_proveedores(request):
    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')    

    # verificar que el usuario tenga permisos
    if not 6 in request.session.get('permisos'):
        return redirect('inicio')

    Proveedores = Proveedor.objects.all() 
    return render(request,"productos/listado_proveedores.html",{
        "titulo":"Listado de Productos",
        "Proveedor": Proveedores 
    })

def agregar_proveedores(request):
    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')

    if not 7 in request.session.get('permisos'):
        return redirect('inicio')

    if request.method == 'POST':
        formulario_proveedores = ProveedorForm(request.POST)
        if formulario_proveedores.is_valid():
            formulario_proveedores.save()
            return redirect('agregar_proveedores') 
    else:
        formulario_proveedores = ProveedorForm()
    
    return render(request, 'productos/agregar_proveedores.html', {'formulario_proveedores': formulario_proveedores})

def listado_ubicacion(request):
    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')

    # verificar que el usuario tenga permisos
    if not 8 in request.session.get('permisos'):
        return redirect('inicio')

    Ubicaciones = Ubicacion.objects.all() 
    return render(request,"productos/listado_ubicacion.html",{
        "titulo":"Listado de Ubicaciones",
        "Ubicaciones": Ubicaciones 
    })

def agregar_ubicacion(request):
    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')

    if not 9 in request.session.get('permisos'):
        return redirect('inicio')

    if request.method == 'POST':
        formulario_ubicacion = UbicacionForm(request.POST)
        if formulario_ubicacion.is_valid():
            formulario_ubicacion.save()
            return redirect('agregar_ubicacion') 
    else:
        formulario_ubicacion = UbicacionForm()
    
    return render(request, 'productos/agregar_ubicacion.html', {'formulario_ubicacion': formulario_ubicacion})

