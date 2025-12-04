from django import forms
from django.core.validators import RegexValidator
from .models import Ingreso, MovimientoIngreso, Salida, MovimientoSalida
from Productos.models import Proveedor, Producto
from decimal import Decimal


class IngresoForm(forms.ModelForm):
    numero_documento = forms.CharField(
        max_length=30,
        validators=[RegexValidator(regex=r'^\d+$', message='El número de documento solo puede tener valores numéricos')],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de documento'})
    )
    class Meta:
        model = Ingreso
        fields = ['proveedor', 'tipo_documento', 'numero_documento']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            # 'numero_documento' widget definido en el campo explícito arriba
        }

    def clean_numero_documento(self):
        valor = self.cleaned_data.get('numero_documento')
        if valor is None:
            return valor

        # Ya validado por regex: exactamente 8 dígitos; ahora comprobar valor numérico > 0
        try:
            num = int(valor)
        except (TypeError, ValueError):
            raise forms.ValidationError('El número de documento debe contener sólo dígitos.')

        if num <= 0:
            raise forms.ValidationError('El número de documento debe ser mayor que 0.')

        return valor

class MovimientoIngresoForm(forms.ModelForm):
    class Meta:
        model = MovimientoIngreso
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio unitario'}),
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad in (None, ''):
            return cantidad

        # Si viene como Decimal (campo del modelo), convertir a Decimal para la comprobación
        try:
            cantidad_val = Decimal(str(cantidad))
        except Exception:
            raise forms.ValidationError('Ingrese un número válido para la cantidad.')

        if cantidad_val <= 0:
            raise forms.ValidationError('La cantidad debe ser un número positivo mayor que 0.')

        return cantidad

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

    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        cantidad = cleaned_data.get('cantidad')

        if producto is None or cantidad is None:
            return cleaned_data

        try:
            # Asegurarse que comparamos números (float)
            cantidad_val = float(cantidad)
        except (TypeError, ValueError):
            return cleaned_data

        if cantidad_val > producto.stock:
            self.add_error('cantidad', forms.ValidationError(
                f"La cantidad solicitada ({cantidad_val}) supera el stock disponible ({producto.stock})."
            ))

        return cleaned_data
