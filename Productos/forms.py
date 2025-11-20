from django import forms
from .models import Producto, Proveedor, ProveedorProducto,Categoria


class ProductoForm(forms.ModelForm):
    proveedores_seleccionados = forms.ModelMultipleChoiceField(
        queryset=Proveedor.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Proveedores"
    )
    class Meta:
        model = Producto
        fields = ['nombre', 'unidad', 'precio', 'umbral', 'stock', 'ubicacion', 'categoria']

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Bebidas"}),
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'telefono', 'email', 'direccion', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Empresa'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56912345678'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'contacto@empresa.com'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'rows':2, 'placeholder': 'Descripcion'}),
        }