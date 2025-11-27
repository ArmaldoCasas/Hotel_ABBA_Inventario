from django.test import TestCase
from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Producto, Categoria, Proveedor, ProveedorProducto, Ubicacion

class CategoriaModelTest(TestCase):
    def setUp(self):
        print("\n--- Configurando CategoriaModelTest ---")
        self.categoria = Categoria.objects.create(nombre="Lácteos")
        print(f"Categoría creada en setUp: {self.categoria.nombre}")

    def test_crear_categoria(self):
        """Verifica que la categoría se crea con el nombre correcto."""
        print("Ejecutando test_crear_categoria...")
        self.assertEqual(self.categoria.nombre, "Lácteos")
        print("Verificación de nombre exitosa.")
    
    def test_str_categoria(self):
        """Verifica que el método __str__ devuelve el nombre."""
        print("Ejecutando test_str_categoria...")
        self.assertEqual(str(self.categoria), "Lácteos")
        print(f"__str__ retorno correcto: {str(self.categoria)}")

    def test_categoria_nombre_vacio(self):
        """Verifica que no se puede crear una categoría con nombre vacío."""
        print("Ejecutando test_categoria_nombre_vacio...")
        with self.assertRaises(ValidationError):
            categoria_vacia = Categoria(nombre="")
            categoria_vacia.full_clean()
        print("ValidationError levantado correctamente para nombre vacío.")

    def test_categoria_nombre_duplicado(self):
        """Verifica que no se pueden crear categorías con nombres duplicados."""
        print("Ejecutando test_categoria_nombre_duplicado...")
        with self.assertRaises(ValidationError):
            categoria_duplicada = Categoria(nombre="Lácteos")
            categoria_duplicada.full_clean()
        print("ValidationError levantado correctamente para nombre duplicado.")


class ProveedorModelTest(TestCase):
    def setUp(self):
        print("\n--- Configurando ProveedorModelTest ---")
        self.proveedor = Proveedor.objects.create(
            nombre="Distribuidora Sur",
            telefono="+56912345678",
            email="contacto@distsur.cl",
            direccion="Calle Falsa 123",
            descripcion="Proveedor de lácteos y abarrotes"
        )
        print(f"Proveedor creado en setUp: {self.proveedor.nombre}")

    def test_crear_proveedor(self):
        """Verifica la creación correcta de un proveedor."""
        print("Ejecutando test_crear_proveedor...")
        self.assertEqual(self.proveedor.nombre, "Distribuidora Sur")
        self.assertEqual(self.proveedor.email, "contacto@distsur.cl")
        print("Datos del proveedor verificados correctamente.")

    def test_str_proveedor(self):
        print("Ejecutando test_str_proveedor...")
        self.assertEqual(str(self.proveedor), "Distribuidora Sur")
        print(f"__str__ retorno correcto: {str(self.proveedor)}")

    def test_proveedor_email_invalido(self):
        """Verifica que un email inválido cause ValidationError."""
        print("Ejecutando test_proveedor_email_invalido...")
        with self.assertRaises(ValidationError):
            proveedor_invalido = Proveedor(nombre="Test", email="emailinvalido")
            proveedor_invalido.full_clean()
        print("ValidationError levantado correctamente para email inválido.")

    def test_proveedor_telefono_formato_invalido(self):
        """Verifica que un teléfono con formato inválido cause ValidationError (si hay validación)."""
        print("Ejecutando test_proveedor_telefono_formato_invalido...")
        with self.assertRaises(ValidationError):
            proveedor_invalido = Proveedor(nombre="Test", telefono="123")
            proveedor_invalido.full_clean()
        print("ValidationError levantado correctamente para teléfono inválido.")


class ProductoModelTest(TestCase):
    def setUp(self):
        print("\n--- Configurando ProductoModelTest ---")
        # Creamos objetos necesarios para las FK
        self.categoria = Categoria.objects.create(nombre="Bebidas")
        self.ubicacion = Ubicacion.objects.create(nombre="Pasillo 1")
        
        self.producto = Producto.objects.create(
            nombre="Jugo de Naranja",
            unidad="lt",
            precio=1500,
            umbral=10.0,
            stock=50.0,
            ubicacion=self.ubicacion,
            categoria=self.categoria
        )
        print(f"Producto creado en setUp: {self.producto.nombre}")

    def test_crear_producto(self):
        """Verifica que el producto se guarda con los datos correctos."""
        print("Ejecutando test_crear_producto...")
        self.assertEqual(self.producto.nombre, "Jugo de Naranja")
        self.assertEqual(self.producto.stock, 50.0)
        self.assertEqual(self.producto.categoria, self.categoria)
        print("Datos del producto verificados correctamente.")

    def test_valores_por_defecto(self):
        """Verifica que los valores por defecto (stock=0, precio=0) funcionan."""
        print("Ejecutando test_valores_por_defecto...")
        producto_nuevo = Producto.objects.create(nombre="Pan")
        self.assertEqual(producto_nuevo.stock, 0)
        self.assertEqual(producto_nuevo.precio, 0)
        self.assertEqual(producto_nuevo.unidad, 'kg') # Default definido en modelo
        print("Valores por defecto verificados correctamente.")

    def test_str_producto(self):
        print("Ejecutando test_str_producto...")
        self.assertEqual(str(self.producto), "Jugo de Naranja")
        print(f"__str__ retorno correcto: {str(self.producto)}")

    def test_producto_precio_negativo(self):
        """Verifica que el precio no puede ser negativo."""
        print("Ejecutando test_producto_precio_negativo...")
        with self.assertRaises(ValidationError):
            producto_negativo = Producto(
                nombre="Producto Malo",
                precio=-100,
                stock=10,
                umbral=5,
                ubicacion=self.ubicacion,
                categoria=self.categoria
            )
            producto_negativo.full_clean()
        print("ValidationError levantado correctamente para precio negativo.")

    def test_producto_stock_negativo(self):
        """Verifica que el stock no puede ser negativo."""
        print("Ejecutando test_producto_stock_negativo...")
        with self.assertRaises(ValidationError):
            producto_negativo = Producto(
                nombre="Producto Malo 2",
                precio=100,
                stock=-10,
                umbral=5,
                ubicacion=self.ubicacion,
                categoria=self.categoria
            )
            producto_negativo.full_clean()
        print("ValidationError levantado correctamente para stock negativo.")

    def test_producto_umbral_negativo(self):
        """Verifica que el umbral no puede ser negativo."""
        print("Ejecutando test_producto_umbral_negativo...")
        with self.assertRaises(ValidationError):
            producto_negativo = Producto(
                nombre="Producto Malo 3",
                precio=100,
                stock=10,
                umbral=-5,
                ubicacion=self.ubicacion,
                categoria=self.categoria
            )
            producto_negativo.full_clean()
        print("ValidationError levantado correctamente para umbral negativo.")

    def test_producto_nombre_vacio(self):
        """Verifica que el nombre del producto no puede ser vacío."""
        print("Ejecutando test_producto_nombre_vacio...")
        with self.assertRaises(ValidationError):
            producto_vacio = Producto(nombre="")
            producto_vacio.full_clean()
        print("ValidationError levantado correctamente para nombre vacío.")

    def test_producto_sin_ubicacion_o_categoria_opcional(self):
        """Verifica que un producto puede crearse sin ubicación o categoría si son opcionales."""
        print("Ejecutando test_producto_sin_ubicacion_o_categoria_opcional...")
        producto_sin_fk = Producto.objects.create(nombre="Producto sin FK", precio=100)
        self.assertIsNone(producto_sin_fk.ubicacion)
        self.assertIsNone(producto_sin_fk.categoria)
        print("Producto creado sin FK opcionales correctamente.")


class RelacionProductoProveedorTest(TestCase):
    def setUp(self):
        print("\n--- Configurando RelacionProductoProveedorTest ---")
        # Configuración inicial
        self.prod = Producto.objects.create(nombre="Arroz Grado 2")
        self.prov1 = Proveedor.objects.create(nombre="Arrocera A")
        self.prov2 = Proveedor.objects.create(nombre="Arrocera B")
        print(f"Producto '{self.prod.nombre}' y proveedores '{self.prov1.nombre}', '{self.prov2.nombre}' creados.")

    def test_asignar_proveedores(self):
        """
        Prueba la relación Muchos a Muchos usando la tabla intermedia.
        """
        print("Ejecutando test_asignar_proveedores...")
        # Crear relaciones manualmente (como lo haces en tu form)
        r1 = ProveedorProducto.objects.create(producto=self.prod, proveedor=self.prov1)
        r2 = ProveedorProducto.objects.create(producto=self.prod, proveedor=self.prov2)
        print("Relaciones creadas.")

        # Verificar que el producto tiene 2 proveedores asociados
        self.assertEqual(self.prod.proveedores.count(), 2)
        
        # Verificar que los proveedores son los correctos
        nombres_proveedores = list(self.prod.proveedores.values_list('nombre', flat=True))
        self.assertIn("Arrocera A", nombres_proveedores)
        self.assertIn("Arrocera B", nombres_proveedores)
        print(f"Proveedores asociados verificados: {nombres_proveedores}")

    def test_eliminar_producto_borra_relacion(self):
        """
        Verifica que si se borra un producto, la relación en la tabla intermedia desaparece (CASCADE).
        """
        print("Ejecutando test_eliminar_producto_borra_relacion...")
        ProveedorProducto.objects.create(producto=self.prod, proveedor=self.prov1)
        print("Relación inicial creada.")
        
        # Borramos el producto
        self.prod.delete()
        print("Producto eliminado.")
        
        # La relación no debe existir
        existe_relacion = ProveedorProducto.objects.filter(proveedor=self.prov1).exists()
        self.assertFalse(existe_relacion)
        print("Verificado: La relación ya no existe.")
        
        # Pero el proveedor SÍ debe seguir existiendo
        self.assertTrue(Proveedor.objects.filter(nombre="Arrocera A").exists())
        print("Verificado: El proveedor sigue existiendo.")

    
    def test_eliminar_proveedor_borra_relacion(self):
        """
        Verifica que si se borra un proveedor, la relación en la tabla intermedia desaparece (CASCADE).
        """
        print("Ejecutando test_eliminar_proveedor_borra_relacion...")
        ProveedorProducto.objects.create(producto=self.prod, proveedor=self.prov1)
        self.assertEqual(ProveedorProducto.objects.count(), 1)
        print("Relación inicial creada.")
        
        self.prov1.delete()
        print("Proveedor eliminado.")
        
        # La relación no debe existir
        self.assertEqual(ProveedorProducto.objects.count(), 0)
        print("Verificado: La relación ya no existe.")
        
        # Pero el producto SÍ debe seguir existiendo
        self.assertTrue(Producto.objects.filter(nombre="Arroz Grado 2").exists())
        print("Verificado: El producto sigue existiendo.")
# Create your tests here.
