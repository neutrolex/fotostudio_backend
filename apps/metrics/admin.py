"""
Admin para el sistema de métricas.
"""

from django.contrib import admin
from .models import Metric, KPIDefinition, MetricAlert


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ['name', 'metric_type', 'value', 'unit', 'calculated_at']
    list_filter = ['metric_type', 'is_active', 'is_system']
    search_fields = ['name', 'description']


@admin.register(KPIDefinition)
class KPIDefinitionAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active', 'is_system', 'created_by']
    list_filter = ['category', 'is_active', 'is_system']
    search_fields = ['name', 'description']


@admin.register(MetricAlert)
class MetricAlertAdmin(admin.ModelAdmin):
    list_display = ['metric_id', 'alert_level', 'is_resolved', 'created_at']
    list_filter = ['alert_level', 'is_resolved', 'created_at']
    readonly_fields = ['created_at']