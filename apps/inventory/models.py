from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from apps.tenants.models import Tenant


class Inventario(models.Model):
    """
    Modelo principal para control de inventario.
    
    Compatible con la estructura esperada por el frontend.
    """
    
    CATEGORIA_CHOICES = [
        ('Enmarcado', 'Enmarcado'),
        ('Minilab', 'Minilab'),
        ('Pintura', 'Pintura'),
        ('Diseño', 'Diseño'),
        ('Restauración Digital', 'Restauración Digital'),
        ('Recordatorios', 'Recordatorios'),
    ]
    
    TIPO_CHOICES = [
        # Enmarcado
        ('Molduras', 'Molduras'),
        ('Pinturas', 'Pinturas'),
        ('Pinceles', 'Pinceles'),
        ('Barnices', 'Barnices'),
        # Minilab
        ('Papel', 'Papel'),
        ('Químicos', 'Químicos'),
        ('Insumos', 'Insumos'),
        # Pintura
        ('Óleos', 'Óleos'),
        ('Acrílicos', 'Acrílicos'),
        ('Lienzos', 'Lienzos'),
        # Diseño
        ('Plantillas', 'Plantillas'),
        ('Fuentes', 'Fuentes'),
        ('Gráficos', 'Gráficos'),
        # Restauración Digital
        ('Software', 'Software'),
        ('Hardware', 'Hardware'),
        # Recordatorios
        ('Materiales', 'Materiales'),
        ('Herramientas', 'Herramientas'),
    ]
    
    UNIDAD_CHOICES = [
        ('unidades', 'Unidades'),
        ('Hojas', 'Hojas'),
        ('L', 'Litros'),
        ('rollos', 'Rollos'),
        ('kg', 'Kilogramos'),
    ]
    
    # ID personalizado para compatibilidad con frontend
    id = models.CharField(max_length=10, primary_key=True, verbose_name="ID Inventario")
    
    # Información básica
    nombre = models.CharField(max_length=200, default="", verbose_name="Nombre del Producto")
    categoria = models.CharField(
        max_length=50, 
        choices=CATEGORIA_CHOICES, 
        default='Enmarcado',
        verbose_name="Categoría"
    )
    tipo = models.CharField(
        max_length=50, 
        choices=TIPO_CHOICES, 
        default='Molduras',
        verbose_name="Tipo"
    )
    
    # Control de stock
    stock = models.IntegerField(default=0, verbose_name="Stock Actual")
    stockMinimo = models.IntegerField(default=0, verbose_name="Stock Mínimo")
    unidad = models.CharField(
        max_length=20, 
        choices=UNIDAD_CHOICES, 
        default='unidades',
        verbose_name="Unidad"
    )
    
    # Información comercial
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Precio Unitario")
    proveedor = models.CharField(max_length=200, blank=True, null=True, verbose_name="Proveedor")
    
    # Metadatos
    fechaIngreso = models.DateField(auto_now_add=True, verbose_name="Fecha de Ingreso")
    ultimaVenta = models.DateField(blank=True, null=True, verbose_name="Última Venta")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relaciones
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='inventario')
    created_by = models.ForeignKey('users.Users', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
        ordering = ['-fechaIngreso']
        unique_together = ['id', 'tenant']
        db_table = 'inventario'
    
    def __str__(self):
        return f"{self.nombre} ({self.tipo})"
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Generar ID automático si no se proporciona
            last_item = Inventario.objects.filter(tenant=self.tenant).order_by('-id').first()
            if last_item and last_item.id.startswith('INV'):
                try:
                    last_num = int(last_item.id[3:])
                    self.id = f"INV{str(last_num + 1).zfill(3)}"
                except ValueError:
                    self.id = "INV001"
            else:
                self.id = "INV001"
        super().save(*args, **kwargs)
    
    @property
    def is_low_stock(self):
        """Verifica si el stock está por debajo del mínimo."""
        return self.stock <= self.stockMinimo


class Varilla(models.Model):
    """Modelo para varillas y molduras de enmarcado."""
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    nombre = models.CharField(max_length=100)
    longitud = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    minimo = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'varilla'

    def __str__(self):
        return f"{self.nombre} - {self.longitud}"
    
    @property
    def is_low_stock(self):
        return self.stock <= self.minimo
    
    @property
    def stock_actual(self):
        return self.stock
    
    @property
    def stock_minimo(self):
        return self.minimo
    
    @property
    def precio_unitario(self):
        return self.precio


class PinturaAcabado(models.Model):
    """Modelo para pinturas y acabados de enmarcado."""
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)  # barniz, laca, esmalte, etc.
    color = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    minimo = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'inventory_pintura_acabado'

    def __str__(self):
        return f"{self.nombre} - {self.tipo}"
    
    @property
    def is_low_stock(self):
        return self.stock <= self.minimo
    
    @property
    def stock_actual(self):
        return self.stock
    
    @property
    def stock_minimo(self):
        return self.minimo
    
    @property
    def precio_unitario(self):
        return self.precio


class MaterialImpresion(models.Model):
    """Modelo para materiales de impresión (minilab)."""
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)  # papel, químico, tinta, etc.
    especificaciones = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    minimo = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'inventory_material_impresion'

    def __str__(self):
        return f"{self.nombre} - {self.tipo}"
    
    @property
    def is_low_stock(self):
        return self.stock <= self.minimo
    
    @property
    def stock_actual(self):
        return self.stock
    
    @property
    def stock_minimo(self):
        return self.minimo
    
    @property
    def precio_unitario(self):
        return self.precio


class MaterialRecordatorio(models.Model):
    """Modelo para materiales de recordatorio (escolares)."""
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)  # papel, tinta, pegamento, etc.
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    minimo = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'inventory_material_recordatorio'

    def __str__(self):
        return f"{self.nombre} - {self.tipo}"
    
    @property
    def is_low_stock(self):
        return self.stock <= self.minimo
    
    @property
    def stock_actual(self):
        return self.stock
    
    @property
    def stock_minimo(self):
        return self.minimo
    
    @property
    def precio_unitario(self):
        return self.precio


class SoftwareEquipo(models.Model):
    """Modelo para software y equipos (restauración digital)."""
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)  # software, hardware, licencia
    version = models.CharField(max_length=50, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    minimo = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'inventory_software_equipo'

    def __str__(self):
        return f"{self.nombre} - {self.tipo}"
    
    @property
    def is_low_stock(self):
        return self.stock <= self.minimo
    
    @property
    def stock_actual(self):
        return self.stock
    
    @property
    def stock_minimo(self):
        return self.minimo
    
    @property
    def precio_unitario(self):
        return self.precio


class MaterialPintura(models.Model):
    """Modelo para materiales de pintura al óleo."""
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)  # óleo, acrílico, pincel, lienzo, etc.
    color = models.CharField(max_length=50, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    minimo = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'inventory_material_pintura'

    def __str__(self):
        return f"{self.nombre} - {self.tipo}"
    
    @property
    def is_low_stock(self):
        return self.stock <= self.minimo
    
    @property
    def stock_actual(self):
        return self.stock
    
    @property
    def stock_minimo(self):
        return self.minimo
    
    @property
    def precio_unitario(self):
        return self.precio


class MaterialDiseno(models.Model):
    """Modelo para materiales de diseño (edición gráfica)."""
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)  # plantilla, fuente, gráfico, etc.
    especificaciones = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    minimo = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'inventory_material_diseno'

    def __str__(self):
        return f"{self.nombre} - {self.tipo}"
    
    @property
    def is_low_stock(self):
        return self.stock <= self.minimo
    
    @property
    def stock_actual(self):
        return self.stock
    
    @property
    def stock_minimo(self):
        return self.minimo
    
    @property
    def precio_unitario(self):
        return self.precio


class ProductoTerminado(models.Model):
    """Modelo para productos terminados."""
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=50)  # cuadro, impresión, recordatorio, etc.
    estado = models.CharField(max_length=20, choices=[
        ('en_produccion', 'En Producción'),
        ('en_almacen', 'En Almacén'),
        ('en_tienda', 'En Tienda'),
        ('vendido', 'Vendido')
    ], default='en_produccion')
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    fecha_creacion = models.DateField()
    orden_produccion = models.ForeignKey('production.OrdenProduccion', on_delete=models.SET_NULL, null=True, blank=True, db_column='orden_produccion_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'inventory_producto_terminado'

    def __str__(self):
        return f"{self.nombre} - {self.estado}"


class MovimientoInventario(models.Model):
    """Modelo para movimientos de inventario."""
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    varilla = models.ForeignKey('inventory.Varilla', on_delete=models.CASCADE, db_column='varilla_id', default=1)
    tipo = models.CharField(max_length=20, choices=[
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('ajuste', 'Ajuste'),
        ('transferencia', 'Transferencia'),
        ('merma', 'Merma')
    ])
    cantidad = models.IntegerField()
    motivo = models.CharField(max_length=255, blank=True, null=True)
    orden = models.ForeignKey('production.OrdenProduccion', on_delete=models.SET_NULL, null=True, blank=True, db_column='orden_id', related_name='inventory_movimientos')
    usuario = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'movimiento_inventario'

    def __str__(self):
        return f"{self.tipo} - {self.cantidad} varilla_id:{self.varilla_id}"