from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
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


def editar_Productos(request,producto_id):
    if not request.session.get('user_id'):
        return redirect('login')
     
    if not 3 in request.session.get('permisos'):
        return redirect('inicio')

    producto = get_object_or_404(Producto, pk=producto_id)
    if not producto.esta_activo :
        
        return redirect("listado_productos")

    if request.method == 'POST':
        formulario_productos = ProductoForm(request.POST, instance=producto)    
        if formulario_productos.is_valid():
            formulario_productos.save()
            return redirect('listado_productos')
    else:
        formulario_productos = ProductoForm(
            instance=producto,
            initial={'proveedores_seleccionados': producto.proveedores.all()}
        )


    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.all()
    return render(request, 'productos/agregar_productos.html', {
        'formulario_productos': formulario_productos, 
        'categorias': categorias,
        'proveedores': proveedores,
        'producto': producto,
    })

def cambiar_estado_producto(request,producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)

    producto.esta_activo = not producto.esta_activo
    producto.save()
    return redirect("listado_productos")


def listado_categorias(request):
    # verificar que el usuario este logueado
    if not request.session.get('user_id'):
        return redirect('login')

    # verificar que el usuario tenga permisos
    if not 4 in request.session.get('permisos'):
        return redirect('inicio')

    # Obtener categorías
    Categorias = Categoria.objects.all() 
    return render(request,"productos/listado_categorias.html",{
        "titulo":"Listado de Categorías",
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

    # Obtener proveedores
    Proveedores = Proveedor.objects.all() 
    return render(request,"productos/listado_proveedores.html",{
        "titulo":"Listado de Proveedores",
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

    # Obtener ubicaciones con prefetch de productos
    Ubicaciones = Ubicacion.objects.prefetch_related('producto_set').all() 
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

def eliminar_categoria(request, categoria_id):
    if not request.session.get('user_id'):
        return redirect('login')

    if not 5 in request.session.get('permisos'):  # mismo permiso que agregar
        return redirect('inicio')

    categoria = get_object_or_404(Categoria, pk=categoria_id)
    if categoria.producto_set.exists():
        messages.error(request, f'No se puede eliminar la categoría "{categoria.nombre}" porque tiene productos asociados.')
    else:
        categoria.delete()
        messages.success(request, f'Categoría "{categoria.nombre}" eliminada exitosamente.')
    return redirect('listado_categorias')

def eliminar_proveedor(request, proveedor_id):
    if not request.session.get('user_id'):
        return redirect('login')

    if not 7 in request.session.get('permisos'):  # mismo permiso que agregar
        return redirect('inicio')

    proveedor = get_object_or_404(Proveedor, pk=proveedor_id)
    if proveedor.productos.exists():
        messages.error(request, f'No se puede eliminar el proveedor "{proveedor.nombre}" porque suministra productos.')
    else:
        proveedor.delete()
        messages.success(request, f'Proveedor "{proveedor.nombre}" eliminado exitosamente.')
    return redirect('listado_proveedores')

