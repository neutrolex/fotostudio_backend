"""
Serializers para la app de agenda.
"""

from rest_framework import serializers
from .models import Agenda


class AgendaSerializer(serializers.ModelSerializer):
    """Serializer para agenda/citas."""
    
    class Meta:
        model = Agenda
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def validate(self, data):
        """Validar fechas de cita."""
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin and fecha_inicio >= fecha_fin:
            raise serializers.ValidationError("La fecha de fin debe ser posterior a la fecha de inicio")
        
        return data
