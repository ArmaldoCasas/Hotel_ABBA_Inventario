from django.db import models


# Create your models here.
class Reporte(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey('login.Usuarios', on_delete=models.SET_NULL, null=True, blank=True)

        
