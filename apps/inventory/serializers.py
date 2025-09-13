"""
Serializers para la app de inventario.
"""

from rest_framework import serializers
from .models import (
    Inventario, Varilla, PinturaAcabado, MaterialImpresion, 
    MaterialRecordatorio, SoftwareEquipo, MaterialPintura, 
    MaterialDiseno, ProductoTerminado, MovimientoInventario
)


class InventarioSerializer(serializers.ModelSerializer):
    """
    Serializer para inventario compatible con el frontend.
    """
    is_low_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Inventario
        fields = [
            'id', 'nombre', 'categoria', 'tipo', 'stock', 'stockMinimo', 
            'unidad', 'precio', 'proveedor', 'fechaIngreso', 'ultimaVenta', 'is_low_stock'
        ]
        read_only_fields = ['id', 'fechaIngreso', 'is_low_stock', 'tenant']
    
    def to_representation(self, instance):
        """Formatear la respuesta para compatibilidad con frontend."""
        data = super().to_representation(instance)
        
        # Formatear fechas
        if data.get('fechaIngreso'):
            data['fechaIngreso'] = instance.fechaIngreso.strftime('%Y-%m-%d')
        if data.get('ultimaVenta'):
            data['ultimaVenta'] = instance.ultimaVenta.strftime('%Y-%m-%d')
        
        # Formatear precio
        if data.get('precio'):
            data['precio'] = float(instance.precio)
        
        return data
    
    def validate_stock(self, value):
        """Validar stock no negativo."""
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo")
        return value
    
    def validate_stockMinimo(self, value):
        """Validar stock mínimo no negativo."""
        if value < 0:
            raise serializers.ValidationError("El stock mínimo no puede ser negativo")
        return value


class VarillaSerializer(serializers.ModelSerializer):
    """Serializer para varillas."""
    is_low_stock = serializers.ReadOnlyField()
    stock_actual = serializers.ReadOnlyField()
    stock_minimo = serializers.ReadOnlyField()
    precio_unitario = serializers.ReadOnlyField()
    
    class Meta:
        model = Varilla
        fields = [
            'id', 'tenant_id', 'nombre', 'longitud', 'tipo', 'precio', 
            'stock', 'minimo', 'created_at', 'updated_at',
            'is_low_stock', 'stock_actual', 'stock_minimo', 'precio_unitario'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at', 'is_low_stock', 'stock_actual', 'stock_minimo', 'precio_unitario')
        extra_kwargs = {
            'tenant_id': {'required': False, 'default': 1},
            'nombre': {'required': False, 'allow_blank': True},
            'longitud': {'required': False, 'default': 0},
            'precio': {'required': False, 'default': 0},
            'tipo': {'required': False, 'allow_blank': True},
            'stock': {'required': False, 'default': 0},
            'minimo': {'required': False, 'default': 0}
        }
    
    def validate_stock(self, value):
        """Validar stock no negativo."""
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo")
        return value
    
    def validate_minimo(self, value):
        """Validar stock mínimo no negativo."""
        if value < 0:
            raise serializers.ValidationError("El stock mínimo no puede ser negativo")
        return value


class PinturaAcabadoSerializer(serializers.ModelSerializer):
    """Serializer para pinturas y acabados."""
    is_low_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = PinturaAcabado
        fields = [
            'id', 'tenant_id', 'nombre', 'tipo', 'color', 'precio',
            'stock', 'minimo', 'created_at', 'updated_at', 'is_low_stock',
            'stock_actual', 'stock_minimo', 'precio_unitario'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at', 'is_low_stock')
        extra_kwargs = {
            'tenant_id': {'required': False, 'default': 1},
            'nombre': {'required': False, 'allow_blank': True},
            'tipo': {'required': False, 'allow_blank': True},
            'color': {'required': False, 'allow_blank': True},
            'precio': {'required': False, 'default': 0},
            'stock': {'required': False, 'default': 0},
            'minimo': {'required': False, 'default': 0}
        }
    
    def validate_stock_actual(self, value):
        """Validar stock no negativo."""
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo")
        return value


class MaterialImpresionSerializer(serializers.ModelSerializer):
    """Serializer para materiales de impresión."""
    is_low_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = MaterialImpresion
        fields = [
            'id', 'tenant_id', 'nombre', 'tipo', 'especificaciones', 'precio',
            'stock', 'minimo', 'created_at', 'updated_at', 'is_low_stock',
            'stock_actual', 'stock_minimo', 'precio_unitario'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at', 'is_low_stock')
        extra_kwargs = {
            'tenant_id': {'required': False, 'default': 1},
            'nombre': {'required': False, 'allow_blank': True},
            'tipo': {'required': False, 'allow_blank': True},
            'especificaciones': {'required': False, 'allow_blank': True},
            'precio': {'required': False, 'default': 0},
            'stock': {'required': False, 'default': 0},
            'minimo': {'required': False, 'default': 0}
        }
    
    def validate_stock_actual(self, value):
        """Validar stock no negativo."""
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo")
        return value


class MaterialRecordatorioSerializer(serializers.ModelSerializer):
    """Serializer para materiales de recordatorio."""
    is_low_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = MaterialRecordatorio
        fields = [
            'id', 'tenant_id', 'nombre', 'tipo', 'descripcion', 'precio',
            'stock', 'minimo', 'created_at', 'updated_at', 'is_low_stock',
            'stock_actual', 'stock_minimo', 'precio_unitario'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at', 'is_low_stock')
        extra_kwargs = {
            'tenant_id': {'required': False, 'default': 1},
            'nombre': {'required': False, 'allow_blank': True},
            'tipo': {'required': False, 'allow_blank': True},
            'descripcion': {'required': False, 'allow_blank': True},
            'precio': {'required': False, 'default': 0},
            'stock': {'required': False, 'default': 0},
            'minimo': {'required': False, 'default': 0}
        }
    
    def validate_stock_actual(self, value):
        """Validar stock no negativo."""
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo")
        return value


class SoftwareEquipoSerializer(serializers.ModelSerializer):
    """Serializer para software y equipos."""
    is_low_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = SoftwareEquipo
        fields = [
            'id', 'tenant_id', 'nombre', 'tipo', 'version', 'precio',
            'stock', 'minimo', 'created_at', 'updated_at', 'is_low_stock',
            'stock_actual', 'stock_minimo', 'precio_unitario'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at', 'is_low_stock')
        extra_kwargs = {
            'tenant_id': {'required': False, 'default': 1},
            'nombre': {'required': False, 'allow_blank': True},
            'tipo': {'required': False, 'allow_blank': True},
            'version': {'required': False, 'allow_blank': True},
            'precio': {'required': False, 'default': 0},
            'stock': {'required': False, 'default': 0},
            'minimo': {'required': False, 'default': 0}
        }
    
    def validate_stock_actual(self, value):
        """Validar stock no negativo."""
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo")
        return value


class MaterialPinturaSerializer(serializers.ModelSerializer):
    """Serializer para materiales de pintura."""
    is_low_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = MaterialPintura
        fields = [
            'id', 'tenant_id', 'nombre', 'tipo', 'color', 'precio',
            'stock', 'minimo', 'created_at', 'updated_at', 'is_low_stock',
            'stock_actual', 'stock_minimo', 'precio_unitario'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at', 'is_low_stock')
        extra_kwargs = {
            'tenant_id': {'required': False, 'default': 1},
            'nombre': {'required': False, 'allow_blank': True},
            'tipo': {'required': False, 'allow_blank': True},
            'color': {'required': False, 'allow_blank': True},
            'precio': {'required': False, 'default': 0},
            'stock': {'required': False, 'default': 0},
            'minimo': {'required': False, 'default': 0}
        }
    
    def validate_stock_actual(self, value):
        """Validar stock no negativo."""
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo")
        return value


class MaterialDisenoSerializer(serializers.ModelSerializer):
    """Serializer para materiales de diseño."""
    is_low_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = MaterialDiseno
        fields = [
            'id', 'tenant_id', 'nombre', 'tipo', 'especificaciones', 'precio',
            'stock', 'minimo', 'created_at', 'updated_at', 'is_low_stock',
            'stock_actual', 'stock_minimo', 'precio_unitario'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at', 'is_low_stock')
        extra_kwargs = {
            'tenant_id': {'required': False, 'default': 1},
            'nombre': {'required': False, 'allow_blank': True},
            'tipo': {'required': False, 'allow_blank': True},
            'especificaciones': {'required': False, 'allow_blank': True},
            'precio': {'required': False, 'default': 0},
            'stock': {'required': False, 'default': 0},
            'minimo': {'required': False, 'default': 0}
        }
    
    def validate_stock_actual(self, value):
        """Validar stock no negativo."""
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo")
        return value


class ProductoTerminadoSerializer(serializers.ModelSerializer):
    """Serializer para productos terminados."""
    
    class Meta:
        model = ProductoTerminado
        fields = [
            'id', 'tenant_id', 'nombre', 'descripcion', 'tipo', 'estado',
            'precio_venta', 'ubicacion', 'orden_produccion_id', 'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')
        extra_kwargs = {
            'tenant_id': {'required': False, 'default': 1},
            'nombre': {'required': False, 'allow_blank': True},
            'descripcion': {'required': False, 'allow_blank': True},
            'tipo': {'required': False, 'allow_blank': True},
            'estado': {'required': False, 'allow_blank': True},
            'precio_venta': {'required': False, 'default': 0},
            'ubicacion': {'required': False, 'allow_blank': True},
            'orden_produccion_id': {'required': False, 'default': None}
        }


class MovimientoInventarioSerializer(serializers.ModelSerializer):
    """Serializer para movimientos de inventario."""
    
    class Meta:
        model = MovimientoInventario
        fields = [
            'id', 'tenant_id', 'varilla_id', 'tipo', 'cantidad',
            'motivo', 'orden_id', 'usuario', 'fecha', 'created_at'
        ]
        read_only_fields = ('id', 'fecha', 'created_at')
        extra_kwargs = {
            'tenant_id': {'required': False, 'default': 1},
            'varilla_id': {'required': False, 'default': 1},
            'tipo': {'required': False, 'allow_blank': True},
            'cantidad': {'required': False, 'default': 1},
            'motivo': {'required': False, 'allow_blank': True},
            'orden_id': {'required': False, 'default': None},
            'usuario': {'required': False, 'allow_blank': True}
        }
    
    def validate_cantidad(self, value):
        """Validar cantidad positiva."""
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser positiva")
        return value
    
    def create(self, validated_data):
        """Crear movimiento con fecha automática."""
        from datetime import datetime
        validated_data['fecha'] = datetime.now()
        return super().create(validated_data)


class StockAlertSerializer(serializers.Serializer):
    """Serializer para alertas de stock bajo."""
    item_type = serializers.CharField()
    item_id = serializers.IntegerField()
    nombre = serializers.CharField()
    stock_actual = serializers.IntegerField()
    stock_minimo = serializers.IntegerField()
    diferencia = serializers.IntegerField()
    ubicacion = serializers.CharField()
    fecha_alerta = serializers.DateTimeField()


class StockReportSerializer(serializers.Serializer):
    """Serializer para reportes de stock."""
    categoria = serializers.CharField()
    total_items = serializers.IntegerField()
    items_stock_bajo = serializers.IntegerField()
    valor_total = serializers.DecimalField(max_digits=15, decimal_places=2)
    porcentaje_stock_bajo = serializers.DecimalField(max_digits=5, decimal_places=2)
