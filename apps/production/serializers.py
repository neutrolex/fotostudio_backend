"""
Serializers para la app de producción.
"""

from rest_framework import serializers
from .models import Cuadro, DetalleOrden, OrdenProduccion, MovimientoInventario


class CuadroSerializer(serializers.ModelSerializer):
    """Serializer para cuadros."""
    nombre = serializers.ReadOnlyField()
    precio_venta = serializers.ReadOnlyField()
    
    class Meta:
        model = Cuadro
        fields = [
            'id', 'orden_id', 'descripcion', 'estado', 'ubicacion', 'precio',
            'fecha_creacion', 'created_at', 'updated_at', 'nombre', 'precio_venta'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at', 'nombre', 'precio_venta')
        extra_kwargs = {
            'orden_id': {'required': False, 'default': 1},
            'descripcion': {'required': False, 'allow_blank': True},
            'estado': {'required': False, 'allow_blank': True},
            'ubicacion': {'required': False, 'allow_blank': True},
            'precio': {'required': False, 'default': 0},
            'fecha_creacion': {'required': False}
        }


class DetalleOrdenSerializer(serializers.ModelSerializer):
    """Serializer para detalles de orden."""
    cantidad_planificada = serializers.ReadOnlyField()
    cantidad_usada = serializers.ReadOnlyField()
    cantidad_merma = serializers.ReadOnlyField()
    
    class Meta:
        model = DetalleOrden
        fields = [
            'id', 'orden_id', 'varilla_id', 'cant_varilla_plan', 'cant_cuadros_plan',
            'cant_varilla_usada', 'cant_cuadros_prod', 'merma', 'created_at', 'updated_at',
            'cantidad_planificada', 'cantidad_usada', 'cantidad_merma'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at', 'cantidad_planificada', 'cantidad_usada', 'cantidad_merma')
        extra_kwargs = {
            'orden_id': {'required': False, 'default': 1},
            'varilla_id': {'required': False, 'default': 1},
            'cant_varilla_plan': {'required': False, 'default': 0},
            'cant_cuadros_plan': {'required': False, 'default': 0},
            'cant_varilla_usada': {'required': False, 'default': 0},
            'cant_cuadros_prod': {'required': False, 'default': 0},
            'merma': {'required': False, 'default': 0}
        }


class OrdenProduccionSerializer(serializers.ModelSerializer):
    """Serializer para órdenes de producción."""
    numero_orden = serializers.ReadOnlyField()
    
    class Meta:
        model = OrdenProduccion
        fields = [
            'id', 'tenant_id', 'fecha_creacion', 'solicitado_por', 'responsable_produccion',
            'estado', 'created_at', 'updated_at', 'numero_orden'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at', 'numero_orden')
        extra_kwargs = {
            'tenant_id': {'required': False, 'default': 1},
            'fecha_creacion': {'required': False},
            'solicitado_por': {'required': False, 'allow_blank': True},
            'responsable_produccion': {'required': False, 'allow_blank': True},
            'estado': {'required': False, 'allow_blank': True}
        }
    
    def create(self, validated_data):
        """Crear orden de producción con fecha por defecto."""
        from datetime import date
        if 'fecha_creacion' not in validated_data or not validated_data['fecha_creacion']:
            validated_data['fecha_creacion'] = date.today()
        if 'tenant_id' not in validated_data:
            validated_data['tenant_id'] = 1
        return super().create(validated_data)


class MovimientoInventarioSerializer(serializers.ModelSerializer):
    """Serializer para movimientos de inventario en producción."""
    
    class Meta:
        model = MovimientoInventario
        fields = [
            'id', 'tenant_id', 'item_type', 'item_id', 'tipo_movimiento',
            'cantidad', 'motivo', 'orden_produccion_id', 'usuario', 'fecha', 'created_at'
        ]
        read_only_fields = ('id', 'fecha', 'created_at')
        extra_kwargs = {
            'tenant_id': {'required': False, 'default': 1},
            'item_type': {'required': False, 'allow_blank': True},
            'item_id': {'required': False, 'default': 1},
            'tipo_movimiento': {'required': False, 'allow_blank': True},
            'cantidad': {'required': False, 'default': 1},
            'motivo': {'required': False, 'allow_blank': True},
            'orden_produccion_id': {'required': False, 'default': None},
            'usuario': {'required': False, 'allow_blank': True}
        }


class ProductionReportSerializer(serializers.Serializer):
    """Serializer para reportes de producción."""
    periodo = serializers.CharField()
    total_ordenes = serializers.IntegerField()
    ordenes_completadas = serializers.IntegerField()
    ordenes_en_proceso = serializers.IntegerField()
    ordenes_canceladas = serializers.IntegerField()
    eficiencia = serializers.DecimalField(max_digits=5, decimal_places=2)
    total_merma = serializers.IntegerField()


class WasteReportSerializer(serializers.Serializer):
    """Serializer para reportes de merma."""
    material_type = serializers.CharField()
    material_id = serializers.IntegerField()
    material_nombre = serializers.CharField()
    cantidad_merma = serializers.IntegerField()
    porcentaje_merma = serializers.DecimalField(max_digits=5, decimal_places=2)
    ordenes_afectadas = serializers.IntegerField()


class ProductionEfficiencySerializer(serializers.Serializer):
    """Serializer para eficiencia de producción."""
    orden_id = serializers.IntegerField()
    numero_orden = serializers.CharField()
    fecha_creacion = serializers.DateField()
    fecha_completada = serializers.DateField()
    dias_produccion = serializers.IntegerField()
    materiales_usados = serializers.IntegerField()
    materiales_merma = serializers.IntegerField()
    eficiencia = serializers.DecimalField(max_digits=5, decimal_places=2)
