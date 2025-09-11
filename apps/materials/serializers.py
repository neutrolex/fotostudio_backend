"""
Serializers para la app de materiales.
"""

from rest_framework import serializers
from .models import MaterialDiseno


class MaterialDisenoSerializer(serializers.ModelSerializer):
    """Serializer para materiales de diseño."""
    
    class Meta:
        model = MaterialDiseno
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
