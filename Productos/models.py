from django.db import models
from django.core.validators import MinValueValidator
UNIT_CHOICES = [
    ('ml', 'ml'),
    ('kg', 'kg'),
]

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre

    def get_unidad_display_full(self):
        if self.unidad == 'kg':
            return 'kilogramos'
        elif self.unidad == 'ml':
            return 'litros'
        else:
            return self.unidad

class Proveedor(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    telefono = models.CharField(max_length=50)
    email = models.EmailField(max_length=254) 
    direccion = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    contenido = models.FloatField(default=0, validators=[MinValueValidator(0)])
    unidad = models.CharField(max_length=50, choices=UNIT_CHOICES, default='kg') 
    precio = models.PositiveIntegerField(default=0)
    # Umbral mínimo para alertar bajo stock
    umbral = models.FloatField(default=5, validators=[MinValueValidator(0)])
    stock = models.FloatField(default=0, validators=[MinValueValidator(0)])
    esta_activo = models.BooleanField(default=True)
    ubicacion = models.ForeignKey('Ubicacion', on_delete=models.SET_NULL, null=True)
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

class Ubicacion(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nombre