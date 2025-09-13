"""
Serializers para la app de pedidos.
"""

from rest_framework import serializers
from .models import Pedido, Proyecto


class PedidoSerializer(serializers.ModelSerializer):
    """
    Serializer para pedidos compatible con el frontend.
    """
    
    class Meta:
        model = Pedido
        fields = [
            'id', 'cliente', 'servicio', 'estado',
            'fotografias', 'diseño', 'detalles',
            'fecha_actualizacion', 'tenant'
        ]
        read_only_fields = ['id', 'fecha_actualizacion']
    
    def create(self, validated_data):
        """Override create para generar ID automáticamente"""
        # Generar ID automático si no se proporciona
        if 'id' not in validated_data or not validated_data['id']:
            # Obtener el último ID y generar el siguiente
            last_order = Pedido.objects.filter(tenant=validated_data.get('tenant', 1)).order_by('-id').first()
            if last_order:
                try:
                    last_id = int(last_order.id.replace('P', ''))
                    new_id = f"P{last_id + 1:03d}"
                except (ValueError, AttributeError):
                    new_id = "P001"
            else:
                new_id = "P001"
            validated_data['id'] = new_id
        
        return super().create(validated_data)


class ProyectoSerializer(serializers.ModelSerializer):
    """
    Serializer para proyectos compatible con el frontend.
    """
    
    class Meta:
        model = Proyecto
        fields = [
            'id', 'nombre', 'cliente', 'tipo', 'estado',
            'fechaInicio', 'fechaEntrega', 'presupuesto', 'descripcion',
            'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion', 'tenant']
    
    def validate_fechaEntrega(self, value):
        """Validar que la fecha de entrega sea posterior a la fecha de inicio"""
        if self.initial_data.get('fechaInicio') and value < self.initial_data['fechaInicio']:
            raise serializers.ValidationError("La fecha de entrega debe ser posterior a la fecha de inicio")
        return value


# DetallePedidoSerializer removido - no existe el modelo
