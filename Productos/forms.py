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
    def save(self, commit=True):
        # 1. Guardar la instancia del Producto 
        producto = super().save(commit=False)
        if commit:
            producto.save()
        if commit:
            # 2. Guardar la relación Muchos a Muchos manualmente
            proveedores = self.cleaned_data.get('proveedores_seleccionados')
            
            # Limpiamos relaciones anteriores
            ProveedorProducto.objects.filter(producto=producto).delete()

            # Creamos las nuevas relaciones
            if proveedores:
                for proveedor in proveedores:
                    ProveedorProducto.objects.create(
                        producto=producto,
                        proveedor=proveedor
                    )

        return producto

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