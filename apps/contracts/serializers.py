"""
Serializers para la app de contratos.
"""

from rest_framework import serializers
from .models import Contrato


class ContratoSerializer(serializers.ModelSerializer):
    """Serializer para contratos."""
    cliente_nombre = serializers.CharField(source='cliente.name', read_only=True)
    cliente_email = serializers.CharField(source='cliente.email', read_only=True)
    
    class Meta:
        model = Contrato
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def validate(self, data):
        """Validar fechas de contrato."""
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin and fecha_inicio >= fecha_fin:
            raise serializers.ValidationError("La fecha de fin debe ser posterior a la fecha de inicio")
        
        return data
