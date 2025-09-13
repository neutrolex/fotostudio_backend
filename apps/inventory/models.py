from django.db import models
from django.core.exceptions import ValidationError

class Inventario(models.Model):
    """Modelo base para control de stock por categorías."""
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    item_type = models.CharField(max_length=25, choices=[
        ('varilla', 'varilla'),
        ('pintura_acabado', 'pintura_acabado'),
        ('material_impresion', 'material_impresion'),
        ('material_recordatorio', 'material_recordatorio'),
        ('software_equipo', 'software_equipo'),
        ('material_pintura', 'material_pintura'),
        ('material_diseno', 'material_diseno'),
        ('producto_terminado', 'producto_terminado')
    ])
    item_id = models.IntegerField()
    stock_actual = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=0)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'inventario'

    def __str__(self):
        return f"{self.item_type} - ID: {self.item_id}"
    
    @property
    def is_low_stock(self):
        """Verifica si el stock está por debajo del mínimo."""
        return self.stock_actual <= self.stock_minimo


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