"""
Serializers para la app de contratos.
"""

from rest_framework import serializers
from .models import Contrato


class ContratoSerializer(serializers.ModelSerializer):
    """Serializer para contratos compatible con frontend."""
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    cliente_email = serializers.CharField(source='cliente.email', read_only=True)
    
    class Meta:
        model = Contrato
        fields = [
            'id', 'cliente', 'fecha_inicio', 'fecha_fin', 'estado', 'monto_total', 'descripcion',
            'servicio', 'tipo', 'valor', 'pagado', 'porcentajePagado', 'estudiantes',
            'observaciones', 'clausulas', 'fechaCreacion', 'responsable', 'created_at', 'updated_at', 'tenant_id',
            'cliente_nombre', 'cliente_email'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at', 'tenant_id', 'fechaCreacion')
        extra_kwargs = {
            'cliente': {'required': False, 'default': 1},
            'fecha_inicio': {'required': False},
            'fecha_fin': {'required': False},
            'estado': {'required': False, 'default': 'vigente'},
            'monto_total': {'required': False, 'default': 0},
            'descripcion': {'required': False, 'allow_blank': True},
            'servicio': {'required': False, 'allow_blank': True},
            'tipo': {'required': False, 'default': 'Anual'},
            'valor': {'required': False, 'default': 0},
            'pagado': {'required': False, 'default': 0},
            'porcentajePagado': {'required': False, 'default': 0},
            'estudiantes': {'required': False, 'default': 0},
            'observaciones': {'required': False, 'allow_blank': True},
            'clausulas': {'required': False, 'default': []},
            'responsable': {'required': False, 'allow_blank': True}
        }
    
    def validate(self, data):
        """Validar fechas de contrato."""
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin and fecha_inicio >= fecha_fin:
            raise serializers.ValidationError("La fecha de fin debe ser posterior a la fecha de inicio")
        
        return data
