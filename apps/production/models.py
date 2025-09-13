from django.db import models
from django.core.exceptions import ValidationError

class OrdenProduccion(models.Model):
    """Modelo para órdenes de producción."""
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    fecha_creacion = models.DateField(default=None, null=True, blank=True)
    solicitado_por = models.CharField(max_length=100, blank=True, null=True)
    responsable_produccion = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada')
    ], default='pendiente')
    
    # Campos adicionales para compatibilidad con frontend
    descripcion = models.TextField(blank=True, null=True, help_text="Descripción de la orden de producción")
    fecha_inicio = models.DateField(blank=True, null=True, help_text="Fecha de inicio de producción")
    fecha_entrega = models.DateField(blank=True, null=True, help_text="Fecha de entrega estimada")
    prioridad = models.CharField(max_length=20, choices=[
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente')
    ], default='media', help_text="Prioridad de la orden")
    observaciones = models.TextField(blank=True, null=True, help_text="Observaciones adicionales")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'orden_produccion'

    def __str__(self):
        return f"Orden {self.id} - {self.fecha_creacion}"
    
    @property
    def numero_orden(self):
        return f"ORD-{self.id:04d}"


class DetalleOrden(models.Model):
    """Modelo para detalles de órdenes de producción."""
    id = models.AutoField(primary_key=True)
    orden = models.ForeignKey('production.OrdenProduccion', on_delete=models.CASCADE, db_column='orden_id', null=True)
    varilla = models.ForeignKey('inventory.Varilla', on_delete=models.CASCADE, db_column='varilla_id', default=1)
    cant_varilla_plan = models.IntegerField(default=0)
    cant_cuadros_plan = models.IntegerField(default=0)
    cant_varilla_usada = models.IntegerField(default=0)
    cant_cuadros_prod = models.IntegerField(default=0)
    merma = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'detalle_orden'

    def __str__(self):
        return f"Detalle Orden {self.orden_id} - Varilla {self.varilla_id}"
    
    @property
    def cantidad_planificada(self):
        return self.cant_varilla_plan
    
    @property
    def cantidad_usada(self):
        return self.cant_varilla_usada
    
    @property
    def cantidad_merma(self):
        return self.merma


class Cuadro(models.Model):
    """Modelo para cuadros producidos."""
    id = models.AutoField(primary_key=True)
    orden = models.ForeignKey('production.OrdenProduccion', on_delete=models.SET_NULL, null=True, db_column='orden_id')
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[
        ('en_produccion', 'En Producción'),
        ('terminado', 'Terminado'),
        ('en_almacen', 'En Almacén'),
        ('en_tienda', 'En Tienda'),
        ('entregado', 'Entregado'),
        ('vendido', 'Vendido')
    ], default='en_produccion')
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'cuadro'

    def __str__(self):
        return f"Cuadro {self.id} - {self.descripcion[:50] if self.descripcion else 'Sin descripción'}"
    
    @property
    def nombre(self):
        return f"Cuadro {self.id}"
    
    @property
    def precio_venta(self):
        return self.precio


class MovimientoInventario(models.Model):
    """Modelo para movimientos de inventario en producción."""
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    material_type = models.CharField(max_length=25, choices=[
        ('varilla', 'varilla'),
        ('pintura_acabado', 'pintura_acabado'),
        ('material_impresion', 'material_impresion'),
        ('material_recordatorio', 'material_recordatorio'),
        ('software_equipo', 'software_equipo'),
        ('material_pintura', 'material_pintura'),
        ('material_diseno', 'material_diseno'),
        ('producto_terminado', 'producto_terminado')
    ])
    material_id = models.IntegerField()
    tipo_movimiento = models.CharField(max_length=20, choices=[
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('ajuste', 'Ajuste'),
        ('transferencia', 'Transferencia'),
        ('merma', 'Merma'),
        ('uso_produccion', 'Uso en Producción')
    ])
    cantidad = models.IntegerField()
    motivo = models.CharField(max_length=255, blank=True, null=True)
    orden_produccion = models.ForeignKey('production.OrdenProduccion', on_delete=models.SET_NULL, null=True, db_column='orden_produccion_id', related_name='production_movimientos')
    usuario = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'production_movimiento_inventario'

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.cantidad} {self.material_type}"
