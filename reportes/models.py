from django.db import models

# Create your models here.
class Reporte(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)
    productos = models.ManyToManyField('Productos.Producto')
        

