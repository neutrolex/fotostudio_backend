from django.db import models

# Create your models here.

# Este archivo se mantiene para compatibilidad pero los modelos están en inventory/
# Los modelos de materiales están centralizados en apps/inventory/models.py
# para evitar duplicaciones y mantener consistencia en la base de datos.

class MaterialVarilla(models.Model):
    """Modelo para relacionar materiales con varillas."""
    id = models.AutoField(primary_key=True)
    varilla = models.ForeignKey('inventory.Varilla', on_delete=models.CASCADE, db_column='varilla_id', default=1)
    material_type = models.CharField(max_length=25, choices=[
        ('pintura_acabado', 'pintura_acabado'),
        ('material_impresion', 'material_impresion'),
        ('material_recordatorio', 'material_recordatorio'),
        ('software_equipo', 'software_equipo'),
        ('material_pintura', 'material_pintura'),
        ('material_diseno', 'material_diseno')
    ])
    material_id = models.IntegerField()
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'material_varilla'