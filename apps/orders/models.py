from django.db import models

# Create your models here.

class Pedido(models.Model):
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    cliente_id = models.IntegerField()
    fecha_pedido = models.DateField()
    fecha_entrega_estimada = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[('pendiente', 'pendiente'), ('en_proceso', 'en_proceso'), ('entregado', 'entregado'), ('cancelado', 'cancelado')], default='pendiente')
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'Pedido'

    def __str__(self):
        return f"Pedido {self.id} - {self.fecha_pedido}"

class DetallePedido(models.Model):
    id = models.AutoField(primary_key=True)
    pedido_id = models.IntegerField()
    item_type = models.CharField(max_length=25, choices=[
        ('varilla', 'varilla'),
        ('cuadro', 'cuadro'),
        ('producto_terminado', 'producto_terminado'),
        ('material_impresion', 'material_impresion'),
        ('material_recordatorio', 'material_recordatorio'),
        ('material_diseno', 'material_diseno')
    ])
    item_id = models.IntegerField()
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'DetallePedido'

    def __str__(self):
        return f"Detalle {self.id} - {self.item_type}"