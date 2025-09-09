from django.db import models

# Create your models here.

class Inventario(models.Model):
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
        managed = False
        db_table = 'Inventario'

    def __str__(self):
        return f"{self.item_type} - ID: {self.item_id}"