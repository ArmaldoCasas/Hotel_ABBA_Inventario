from django import forms
from .models import Producto, Proveedor, ProveedorProducto, Categoria, Ubicacion, ProductoUbicacion

class ProductoForm(forms.ModelForm):
    proveedores_seleccionados = forms.ModelMultipleChoiceField(
        queryset=Proveedor.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Proveedores",
        required=False
    )
    ubicaciones_seleccionados = forms.ModelMultipleChoiceField(
        queryset=Ubicacion.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Ubicaciones",
        required=False
    )
    
    class Meta:
        model = Producto
        fields = ['nombre', 'contenido', 'unidad', 'precio', 'umbral', 'stock', 'categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'contenido': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidad': forms.Select(attrs={'class': 'form-select'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'umbral': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def save(self, commit=True):
        # 1. Guardar la instancia del Producto 
        producto = super().save(commit=False)
        if commit:
            producto.save()
        if commit:
            # 2. Guardar la relación Muchos a Muchos con Proveedores manualmente
            proveedores = self.cleaned_data.get('proveedores_seleccionados')
            
            # Limpiamos relaciones anteriores de proveedores
            ProveedorProducto.objects.filter(producto=producto).delete()

            # Creamos las nuevas relaciones con proveedores
            if proveedores:
                for proveedor in proveedores:
                    ProveedorProducto.objects.create(
                        producto=producto,
                        proveedor=proveedor
                    )
            
            # 3. Guardar la relación Muchos a Muchos con Ubicaciones manualmente
            ubicaciones = self.cleaned_data.get('ubicaciones_seleccionados')
            
            # Limpiamos relaciones anteriores de ubicaciones
            ProductoUbicacion.objects.filter(producto=producto).delete()

            # Creamos las nuevas relaciones con ubicaciones
            if ubicaciones:
                for ubicacion in ubicaciones:
                    ProductoUbicacion.objects.create(
                        producto=producto,
                        ubicacion=ubicacion
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

class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ubicación'}),
        }