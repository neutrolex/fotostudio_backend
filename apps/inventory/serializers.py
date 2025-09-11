"""
Serializers para la app de inventario.
"""

from rest_framework import serializers
from .models import Inventario


class InventarioSerializer(serializers.ModelSerializer):
    """Serializer para inventario."""
    
    class Meta:
        model = Inventario
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def validate_stock(self, value):
        """Validar stock no negativo."""
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo")
        return value
