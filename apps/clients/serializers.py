"""
Serializers para la app de clientes.
"""

from rest_framework import serializers
from .models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    """Serializer para clientes."""
    
    class Meta:
        model = Cliente
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def validate_client_type(self, value):
        """Validar tipo de cliente."""
        tipos_validos = ['persona', 'empresa', 'otro']
        if value not in tipos_validos:
            raise serializers.ValidationError(f"Tipo debe ser uno de: {', '.join(tipos_validos)}")
        return value
    
    def validate_email(self, value):
        """Validar email único."""
        if value and Cliente.objects.filter(email=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("Email ya registrado")
        return value
