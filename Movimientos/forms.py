from django import forms
from .models import Ingreso, MovimientoIngreso, Salida, MovimientoSalida
from Productos.models import Proveedor, Producto


class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = ['proveedor', 'tipo_documento', 'numero_documento']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de documento'}),
        }

class MovimientoIngresoForm(forms.ModelForm):
    class Meta:
        model = MovimientoIngreso
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio unitario'}),
        }

class SalidaForm(forms.ModelForm):
    class Meta:
        model = Salida
        fields = ['motivo']
        widgets = {
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Motivo de la salida'}),
            'fecha': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

class MovimientoSalidaForm(forms.ModelForm):
    class Meta:
        model = MovimientoSalida
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'}),
        }
