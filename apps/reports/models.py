"""
Modelos para el sistema de reportes del fotostudio.
"""

from django.db import models
from django.utils import timezone


class Report(models.Model):
    """Modelo para reportes generados."""
    
    REPORT_TYPES = [
        ('financial', 'Reporte Financiero'),
        ('inventory', 'Reporte de Inventario'),
        ('production', 'Reporte de Producción'),
        ('clients', 'Reporte de Clientes'),
        ('orders', 'Reporte de Pedidos'),
        ('custom', 'Reporte Personalizado'),
    ]
    
    EXPORT_FORMATS = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
    ]
    
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    description = models.TextField(blank=True, null=True)
    
    # Filtros del reporte
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    filters = models.JSONField(default=dict, blank=True)
    
    # Configuración
    export_format = models.CharField(max_length=10, choices=EXPORT_FORMATS, default='pdf')
    include_charts = models.BooleanField(default=True)
    include_summary = models.BooleanField(default=True)
    
    # Estado y metadatos
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pendiente'),
        ('generating', 'Generando'),
        ('completed', 'Completado'),
        ('failed', 'Fallido'),
    ], default='pending')
    
    file_path = models.CharField(max_length=500, blank=True, null=True)
    file_size = models.BigIntegerField(default=0)
    
    # Usuario y auditoría
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    generated_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'reports'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_report_type_display()}"
    
    @property
    def is_expired(self):
        if not self.expires_at:
            return False
        return timezone.now() > self.expires_at


class ReportTemplate(models.Model):
    """Plantillas de reportes predefinidas."""
    
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=Report.REPORT_TYPES)
    description = models.TextField(blank=True, null=True)
    
    # Configuración de la plantilla
    template_config = models.JSONField(default=dict)
    default_filters = models.JSONField(default=dict, blank=True)
    
    # Metadatos
    is_active = models.BooleanField(default=True)
    is_system = models.BooleanField(default=False)  # Plantillas del sistema
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'report_templates'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.get_report_type_display()}"


class ExportLog(models.Model):
    """Log de exportaciones realizadas."""
    
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    report_id = models.IntegerField()
    export_format = models.CharField(max_length=10, choices=Report.EXPORT_FORMATS)
    
    # Detalles de la exportación
    file_path = models.CharField(max_length=500)
    file_size = models.BigIntegerField()
    record_count = models.IntegerField(default=0)
    
    # Estado
    status = models.CharField(max_length=20, choices=[
        ('success', 'Exitoso'),
        ('failed', 'Fallido'),
        ('partial', 'Parcial'),
    ])
    
    error_message = models.TextField(blank=True, null=True)
    
    # Auditoría
    exported_by = models.CharField(max_length=100)
    exported_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'export_logs'
        ordering = ['-exported_at']
    
    def __str__(self):
        return f"Export {self.id} - {self.export_format.upper()}"