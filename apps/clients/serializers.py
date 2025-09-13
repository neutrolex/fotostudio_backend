"""
Serializers para la app de clientes.
"""

from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer para clientes compatible con el frontend.
    """
    
    class Meta:
        model = Client
        fields = [
            'id', 'nombre', 'email', 'contacto', 'tipo',
            'direccion', 'ie', 'detalles',
            'fecha_registro', 'ultimo_pedido', 'total_pedidos',
            'monto_total', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'fecha_registro', 'ultimo_pedido', 
            'total_pedidos', 'monto_total', 'created_at', 'updated_at', 'tenant'
        ]
    
    def to_representation(self, instance):
        """Formatear la respuesta para compatibilidad con frontend."""
        data = super().to_representation(instance)
        
        # Formatear fechas
        if data.get('fecha_registro'):
            data['fecha_registro'] = instance.fecha_registro.strftime('%Y-%m-%d')
        if data.get('ultimo_pedido'):
            data['ultimo_pedido'] = instance.ultimo_pedido.strftime('%Y-%m-%d')
        
        # Formatear monto
        if data.get('monto_total'):
            data['monto_total'] = float(instance.monto_total)
        
        return data
    
    def validate_tipo(self, value):
        """Validar tipo de cliente."""
        tipos_validos = ['individual', 'school', 'business']
        if value not in tipos_validos:
            raise serializers.ValidationError(f"Tipo debe ser uno de: {', '.join(tipos_validos)}")
        return value
    
    def validate_email(self, value):
        """Validar email único."""
        if value and Client.objects.filter(email=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("Email ya registrado")
        return value
