from django.db import models

# Unidades permitidas para los productos
UNIT_CHOICES = [
    ('ml', 'ml'),
    ('kg', 'kg'),
]
class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    telefono = models.CharField(max_length=50)
    email = models.EmailField(max_length=254) 
    direccion = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    unidad = models.CharField(max_length=50, choices=UNIT_CHOICES, default='kg') 
    precio = models.PositiveIntegerField(default=0)
    # Umbral mínimo para alertar bajo stock
    umbral = models.FloatField(default=5)
    stock = models.FloatField(default=0)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True,)
    proveedores = models.ManyToManyField(
        'Proveedor',
        through='Productos.ProveedorProducto', 
        related_name='productos')

    def __str__(self):
        return self.nombre
    
class ProveedorProducto(models.Model) :
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.proveedor.nombre} suministra {self.producto.nombre}"
