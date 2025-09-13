"""
Serializers para el sistema de reportes.
"""

from rest_framework import serializers
from .models import Report, ReportTemplate, ExportLog


class ReportSerializer(serializers.ModelSerializer):
    """Serializer para reportes."""
    
    class Meta:
        model = Report
        fields = [
            'id', 'tenant_id', 'name', 'report_type', 'description',
            'date_from', 'date_to', 'filters', 'export_format',
            'include_charts', 'include_summary', 'status',
            'file_path', 'file_size', 'created_by', 'created_at',
            'generated_at', 'expires_at', 'is_expired'
        ]
        read_only_fields = ('id', 'created_at', 'generated_at', 'is_expired')
    
    def validate_date_from(self, value):
        """Validar fecha de inicio."""
        if value and value > timezone.now().date():
            raise serializers.ValidationError("La fecha de inicio no puede ser futura")
        return value
    
    def validate_date_to(self, value):
        """Validar fecha de fin."""
        if value and value > timezone.now().date():
            raise serializers.ValidationError("La fecha de fin no puede ser futura")
        return value
    
    def validate(self, attrs):
        """Validar fechas."""
        date_from = attrs.get('date_from')
        date_to = attrs.get('date_to')
        
        if date_from and date_to and date_from > date_to:
            raise serializers.ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin")
        
        return attrs


class ReportCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear reportes."""
    
    class Meta:
        model = Report
        fields = [
            'name', 'report_type', 'description', 'date_from', 'date_to',
            'filters', 'export_format', 'include_charts', 'include_summary'
        ]
    
    def create(self, validated_data):
        """Crear reporte con datos del usuario."""
        validated_data['tenant_id'] = self.context['request'].user.tenant_id
        validated_data['created_by'] = self.context['request'].user.username
        return super().create(validated_data)


class ReportTemplateSerializer(serializers.ModelSerializer):
    """Serializer para plantillas de reportes."""
    
    class Meta:
        model = ReportTemplate
        fields = [
            'id', 'tenant_id', 'name', 'report_type', 'description',
            'template_config', 'default_filters', 'is_active',
            'is_system', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')


class ExportLogSerializer(serializers.ModelSerializer):
    """Serializer para logs de exportación."""
    
    class Meta:
        model = ExportLog
        fields = [
            'id', 'tenant_id', 'report_id', 'export_format',
            'file_path', 'file_size', 'record_count', 'status',
            'error_message', 'exported_by', 'exported_at'
        ]
        read_only_fields = ('id', 'exported_at')


class ReportGenerationSerializer(serializers.Serializer):
    """Serializer para generar reportes."""
    
    report_type = serializers.ChoiceField(choices=Report.REPORT_TYPES)
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)
    filters = serializers.JSONField(required=False, default=dict)
    export_format = serializers.ChoiceField(choices=Report.EXPORT_FORMATS, default='pdf')
    include_charts = serializers.BooleanField(default=True)
    include_summary = serializers.BooleanField(default=True)
    
    def validate(self, attrs):
        """Validar datos de generación."""
        date_from = attrs.get('date_from')
        date_to = attrs.get('date_to')
        
        if date_from and date_to and date_from > date_to:
            raise serializers.ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin")
        
        return attrs


class ReportFilterSerializer(serializers.Serializer):
    """Serializer para filtros de reportes."""
    
    # Filtros generales
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)
    tenant_id = serializers.IntegerField(required=False)
    
    # Filtros específicos por tipo
    client_type = serializers.CharField(required=False)
    order_status = serializers.CharField(required=False)
    product_type = serializers.CharField(required=False)
    inventory_category = serializers.CharField(required=False)
    
    # Filtros de agrupación
    group_by = serializers.CharField(required=False)
    sort_by = serializers.CharField(required=False)
    sort_order = serializers.ChoiceField(choices=[('asc', 'Ascendente'), ('desc', 'Descendente')], default='asc')
    
    # Paginación
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=50)
