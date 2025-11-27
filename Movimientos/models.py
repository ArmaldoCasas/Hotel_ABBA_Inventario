from django.db import models
from Productos.models import *
from django.core.validators import RegexValidator, MinValueValidator

class Ingreso(models.Model):
    proveedor = models.ForeignKey('Productos.Proveedor', on_delete=models.PROTECT,verbose_name="Proveedor")
    usuario = models.ForeignKey('login.Usuarios', on_delete=models.PROTECT, verbose_name="Usuario", null=True, blank=True)
    TIPO_DOCUMENTO_CHOICES = [
        ('FACTURA', 'Factura'),
        ('BOLETA', 'Boleta'),
    ]
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOCUMENTO_CHOICES)
    numero_documento = models.CharField(
        max_length=8,
        unique=True,
        validators=[RegexValidator(
                regex=r'^\d{8}$',
                message='El número de documento debe tener exactamente 8 dígitos numéricos.')])
    fecha = models.DateTimeField(auto_now_add=True)
    productos = models.ManyToManyField('Productos.Producto',through='MovimientoIngreso',related_name='ingresos')
    def __str__(self):
        return f"Ingreso #{self.id} - {self.numero_documento}"

class MovimientoIngreso(models.Model):
    ingreso = models.ForeignKey(Ingreso, on_delete=models.CASCADE)
    producto = models.ForeignKey('Productos.Producto', on_delete=models.PROTECT)
    # Se mantiene DecimalField para mayor precisión en cantidades y precios
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
    
class Salida(models.Model):
    usuario = models.ForeignKey('login.Usuarios', on_delete=models.PROTECT, verbose_name="Usuario", null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField() 
    productos = models.ManyToManyField('Productos.Producto',through='MovimientoSalida',related_name='salidas')
    def __str__(self):
        return f"Salida #{self.id} ({self.fecha.date()})"


class MovimientoSalida(models.Model):
    salida = models.ForeignKey("Salida", on_delete=models.CASCADE)
    producto = models.ForeignKey('Productos.Producto', on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"