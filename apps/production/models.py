from django.db import models

# Create your models here.

class OrdenProduccion(models.Model):
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    fecha_creacion = models.DateField()
    solicitado_por = models.CharField(max_length=100, blank=True, null=True)
    responsable_produccion = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[('pendiente', 'pendiente'), ('en_proceso', 'en_proceso'), ('completada', 'completada'), ('cancelada', 'cancelada')], default='pendiente')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'orden_produccion'

    def __str__(self):
        return f"Orden {self.id} - {self.fecha_creacion}"

class Varilla(models.Model):
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
        return self.nombre

class DetalleOrden(models.Model):
    id = models.AutoField(primary_key=True)
    orden_id = models.IntegerField()
    varilla_id = models.IntegerField()
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

class Cuadro(models.Model):
    id = models.AutoField(primary_key=True)
    orden_id = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[('en_produccion', 'en_produccion'), ('terminado', 'terminado'), ('en_almacen', 'en_almacen'), ('entregado', 'entregado')], default='en_produccion')
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'cuadro'

    def __str__(self):
        return f"Cuadro {self.id} - {self.descripcion[:50]}"

class MovimientoInventario(models.Model):
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    varilla_id = models.IntegerField()
    tipo = models.CharField(max_length=20, choices=[('entrada', 'entrada'), ('salida', 'salida'), ('ajuste', 'ajuste'), ('transferencia', 'transferencia')])
    cantidad = models.IntegerField()
    motivo = models.CharField(max_length=255, blank=True, null=True)
    orden_id = models.IntegerField(blank=True, null=True)
    usuario = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'movimiento_inventario'

    def __str__(self):
        return f"{self.tipo} - {self.cantidad} varillas"
