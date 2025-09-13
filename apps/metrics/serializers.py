"""
Serializers para el sistema de métricas.
"""

from rest_framework import serializers
from .models import Metric, KPIDefinition, MetricAlert


class MetricSerializer(serializers.ModelSerializer):
    """Serializer para métricas."""
    
    class Meta:
        model = Metric
        fields = [
            'id', 'tenant_id', 'name', 'metric_type', 'description',
            'value', 'unit', 'period_start', 'period_end', 'calculated_at',
            'is_active', 'is_system'
        ]
        read_only_fields = ('id', 'calculated_at')


class KPIDefinitionSerializer(serializers.ModelSerializer):
    """Serializer para definiciones de KPIs."""
    
    class Meta:
        model = KPIDefinition
        fields = [
            'id', 'tenant_id', 'name', 'category', 'description',
            'calculation_formula', 'target_value', 'warning_threshold',
            'critical_threshold', 'is_active', 'is_system',
            'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')


class MetricAlertSerializer(serializers.ModelSerializer):
    """Serializer para alertas de métricas."""
    
    class Meta:
        model = MetricAlert
        fields = [
            'id', 'tenant_id', 'metric_id', 'kpi_definition_id',
            'alert_level', 'message', 'current_value', 'threshold_value',
            'is_resolved', 'resolved_at', 'resolved_by', 'created_at'
        ]
        read_only_fields = ('id', 'created_at')
