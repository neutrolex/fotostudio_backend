from django.db import models

# Create your models here.

class Contrato(models.Model):
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    cliente = models.ForeignKey('clients.Cliente', on_delete=models.CASCADE, db_column='cliente_id', default=1)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[('vigente', 'vigente'), ('vencido', 'vencido'), ('rescindido', 'rescindido')], default='vigente')
    monto_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    descripcion = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'contrato'

    def __str__(self):
        return f"Contrato {self.id} - {self.fecha_inicio}"