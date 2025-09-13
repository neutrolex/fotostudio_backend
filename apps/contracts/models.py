from django.db import models

# Create your models here.

class Contrato(models.Model):
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    cliente = models.ForeignKey('clients.Client', on_delete=models.CASCADE, db_column='cliente_id', default=1)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[('vigente', 'vigente'), ('vencido', 'vencido'), ('rescindido', 'rescindido')], default='vigente')
    monto_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    descripcion = models.TextField(blank=True, null=True)
    
    # CAMPOS COMPATIBLES CON FRONTEND
    servicio = models.CharField(max_length=200, blank=True, null=True, verbose_name="Servicio")
    tipo = models.CharField(max_length=50, choices=[('Anual', 'Anual'), ('Semestral', 'Semestral'), ('Mensual', 'Mensual')], default='Anual', verbose_name="Tipo")
    valor = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Valor Total")
    pagado = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Monto Pagado")
    porcentajePagado = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Porcentaje Pagado")
    estudiantes = models.PositiveIntegerField(default=0, verbose_name="Número de Estudiantes")
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    clausulas = models.JSONField(default=list, blank=True, verbose_name="Cláusulas")
    fechaCreacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación", null=True, blank=True)
    responsable = models.CharField(max_length=100, blank=True, null=True, verbose_name="Responsable")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'contrato'

    def __str__(self):
        return f"Contrato {self.id} - {self.fecha_inicio}"
    
    def save(self, *args, **kwargs):
        """Override save para calcular automáticamente el porcentaje pagado."""
        # Calcular porcentaje pagado automáticamente
        if self.valor > 0:
            self.porcentajePagado = (self.pagado / self.valor) * 100
        else:
            self.porcentajePagado = 0.00
        
        # Actualizar estado basado en fechas
        from django.utils import timezone
        today = timezone.now().date()
        
        if self.fecha_fin:
            if today > self.fecha_fin:
                self.estado = 'vencido'
            elif self.porcentajePagado >= 100:
                self.estado = 'vigente'  # Contrato completado pero vigente
        
        super().save(*args, **kwargs)
    
    @property
    def saldo_pendiente(self):
        """Calcula el saldo pendiente del contrato."""
        return float(self.valor - self.pagado)
    
    @property
    def dias_restantes(self):
        """Calcula los días restantes del contrato."""
        if self.fecha_fin:
            from django.utils import timezone
            today = timezone.now().date()
            delta = self.fecha_fin - today
            return delta.days
        return None