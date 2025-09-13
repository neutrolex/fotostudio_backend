"""
Serializers para la app de materiales.
"""

from rest_framework import serializers
from .models import MaterialVarilla


class MaterialVarillaSerializer(serializers.ModelSerializer):
    """Serializer para relaciones material-varilla."""
    varilla_nombre = serializers.CharField(source='varilla.nombre', read_only=True)
    
    class Meta:
        model = MaterialVarilla
        fields = '__all__'
        read_only_fields = ('id', 'created_at')
