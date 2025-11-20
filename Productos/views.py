from django.shortcuts import render, redirect
from .models import Producto, Categoria, Proveedor
from .forms import ProductoForm, CategoriaForm, ProveedorForm
# Create your views here.
def Agregar_Productos(request):
    if request.method == "POST":
        formulario_productos = ProductoForm(request.POST)
        if formulario_productos.is_valid():
            formulario_productos.save()
            return redirect("agregar_productos")    
    else:
        formulario_productos=ProductoForm()
    return render(request, "Productos/agregar_productos.html", {"formulario_productos":formulario_productos})
def listado_productos(request):
    Productos = Producto.objects.all() 
    return render(request,"Productos/listado_productos.html",{
        "titulo":"Listado de Productos",
        "Productos": Productos 
    })


def agregar_categorias(request):
    if request.method == 'POST':
        formulario_categorias = CategoriaForm(request.POST)
        if formulario_categorias.is_valid():
            formulario_categorias.save()
            return redirect("agregar_categorias") 
    else:
        formulario_categorias = CategoriaForm()
    
    return render(request, 'Productos/agregar_categorias.html', {'formulario_categorias': formulario_categorias})
def listado_categorias(request):
    Categorias = Categoria.objects.all() 
    return render(request,"Productos/listado_categorias.html",{
        "titulo":"Listado de Productos",
        "Categorias": Categorias 
    })

def agregar_proveedores(request):
    if request.method == 'POST':
        formulario_proveedores = ProveedorForm(request.POST)
        if formulario_proveedores.is_valid():
            formulario_proveedores.save()
            return redirect('agregar_proveedores') 
    else:
        formulario_proveedores = ProveedorForm()
    
    return render(request, 'Productos/agregar_proveedores.html', {'formulario_proveedores': formulario_proveedores})
def listado_proveedores(request):
    Proveedores = Proveedor.objects.all() 
    return render(request,"Productos/listado_proveedores.html",{
        "titulo":"Listado de Productos",
        "Proveedor": Proveedores 
    })
