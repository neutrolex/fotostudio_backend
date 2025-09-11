"""
Serializers para la app de pedidos.
"""

from rest_framework import serializers
from .models import Pedido, DetallePedido


class DetallePedidoSerializer(serializers.ModelSerializer):
    """Serializer para detalles de pedido."""
    
    class Meta:
        model = DetallePedido
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class PedidoSerializer(serializers.ModelSerializer):
    """Serializer para pedidos."""
    detalles = DetallePedidoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Pedido
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def validate_estado(self, value):
        """Validar estado del pedido."""
        estados_validos = ['pendiente', 'en_proceso', 'entregado', 'cancelado']
        if value not in estados_validos:
            raise serializers.ValidationError(f"Estado debe ser uno de: {', '.join(estados_validos)}")
        return value
