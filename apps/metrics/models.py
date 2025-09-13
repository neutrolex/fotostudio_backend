"""
Modelos para el sistema de métricas y KPIs.
"""

from django.db import models
from django.utils import timezone


class Metric(models.Model):
    """Modelo para métricas del sistema."""
    
    METRIC_TYPES = [
        ('financial', 'Métrica Financiera'),
        ('operational', 'Métrica Operacional'),
        ('client', 'Métrica de Cliente'),
        ('inventory', 'Métrica de Inventario'),
        ('production', 'Métrica de Producción'),
    ]
    
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    name = models.CharField(max_length=200)
    metric_type = models.CharField(max_length=20, choices=METRIC_TYPES)
    description = models.TextField(blank=True, null=True)
    
    # Valor de la métrica
    value = models.DecimalField(max_digits=15, decimal_places=2)
    unit = models.CharField(max_length=50, blank=True, null=True)
    
    # Metadatos
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    calculated_at = models.DateTimeField(auto_now_add=True)
    
    # Configuración
    is_active = models.BooleanField(default=True)
    is_system = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'metrics'
        ordering = ['-calculated_at']
        unique_together = (('tenant_id', 'name', 'period_start', 'period_end'),)
    
    def __str__(self):
        return f"{self.name} - {self.value} {self.unit or ''}"


class KPIDefinition(models.Model):
    """Definiciones de KPIs del sistema."""
    
    KPI_CATEGORIES = [
        ('financial', 'KPI Financiero'),
        ('operational', 'KPI Operacional'),
        ('client', 'KPI de Cliente'),
        ('inventory', 'KPI de Inventario'),
        ('production', 'KPI de Producción'),
    ]
    
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=KPI_CATEGORIES)
    description = models.TextField(blank=True, null=True)
    
    # Configuración del KPI
    calculation_formula = models.TextField()
    target_value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    warning_threshold = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    critical_threshold = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    
    # Metadatos
    is_active = models.BooleanField(default=True)
    is_system = models.BooleanField(default=False)
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'kpi_definitions'
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"


class MetricAlert(models.Model):
    """Alertas de métricas."""
    
    ALERT_LEVELS = [
        ('info', 'Informativo'),
        ('warning', 'Advertencia'),
        ('critical', 'Crítico'),
    ]
    
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField()
    metric_id = models.IntegerField()
    kpi_definition_id = models.IntegerField(blank=True, null=True)
    
    # Detalles de la alerta
    alert_level = models.CharField(max_length=20, choices=ALERT_LEVELS)
    message = models.TextField()
    current_value = models.DecimalField(max_digits=15, decimal_places=2)
    threshold_value = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Estado
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(blank=True, null=True)
    resolved_by = models.CharField(max_length=100, blank=True, null=True)
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'metric_alerts'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Alerta {self.get_alert_level_display()} - {self.message[:50]}"