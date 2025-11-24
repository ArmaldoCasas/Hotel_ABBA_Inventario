from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class Roles(models.Model):
    ROLE_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Usuario', 'Usuario'),
        ('Jefe Bodega', 'Jefe Bodega'),
    ]

    nombre_rol = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Usuario', unique=True)
    permisos = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.nombre_rol

class Usuarios(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    contraseña = models.CharField(max_length=128)  # contraseña hasheada
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE, related_name='usuarios', null=True, blank=True)


    def __str__(self):
        return self.nombre

    def set_password(self, raw_password):
        self.contraseña = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.contraseña)
