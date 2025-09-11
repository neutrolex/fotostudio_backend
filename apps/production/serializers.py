"""
Serializers para la app de producción.
"""

from rest_framework import serializers
from .models import Cuadro, DetalleOrden, OrdenProduccion


class CuadroSerializer(serializers.ModelSerializer):
    """Serializer para cuadros."""
    
    class Meta:
        model = Cuadro
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class DetalleOrdenSerializer(serializers.ModelSerializer):
    """Serializer para detalles de orden."""
    
    class Meta:
        model = DetalleOrden
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class OrdenProduccionSerializer(serializers.ModelSerializer):
    """Serializer para órdenes de producción."""
    detalles = DetalleOrdenSerializer(many=True, read_only=True)
    
    class Meta:
        model = OrdenProduccion
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
