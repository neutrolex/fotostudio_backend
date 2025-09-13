"""
Serializers para la aplicación de configuraciones del fotostudio.

Este módulo define todos los serializers necesarios para la validación,
serialización y deserialización de datos relacionados con configuraciones.
"""

from rest_framework import serializers
from .models import (
    SystemConfiguration, BusinessSettings, SecuritySettings,
    ServiceConfiguration, UserRole, DataBackup
)


class SystemConfigurationSerializer(serializers.ModelSerializer):
    """
    Serializer para configuraciones del sistema.
    """
    
    class Meta:
        model = SystemConfiguration
        fields = [
            'id', 'config_type', 'key', 'value', 'description',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class BusinessSettingsSerializer(serializers.ModelSerializer):
    """
    Serializer para configuraciones de negocio.
    """
    
    class Meta:
        model = BusinessSettings
        fields = [
            'id', 'company_name', 'address', 'phone', 'email', 'website',
            'tax_id', 'currency', 'logo_url', 'timezone', 'language',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SecuritySettingsSerializer(serializers.ModelSerializer):
    """
    Serializer para configuraciones de seguridad.
    """
    
    class Meta:
        model = SecuritySettings
        fields = [
            'id', 'two_factor_auth', 'session_timeout', 'password_expiry',
            'password_expiry_days', 'max_login_attempts', 'lockout_duration',
            'min_password_length', 'require_uppercase', 'require_lowercase',
            'require_numbers', 'require_special_chars', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ServiceConfigurationSerializer(serializers.ModelSerializer):
    """
    Serializer para configuraciones de servicios.
    """
    
    class Meta:
        model = ServiceConfiguration
        fields = [
            'id', 'service_name', 'base_price', 'status', 'description',
            'estimated_duration', 'requires_approval', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserRoleSerializer(serializers.ModelSerializer):
    """
    Serializer para roles de usuario.
    """
    
    class Meta:
        model = UserRole
        fields = [
            'id', 'role_name', 'description', 'can_manage_users',
            'can_manage_orders', 'can_manage_inventory', 'can_manage_production',
            'can_manage_reports', 'can_manage_settings', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DataBackupSerializer(serializers.ModelSerializer):
    """
    Serializer para respaldos de datos.
    """
    
    class Meta:
        model = DataBackup
        fields = [
            'id', 'backup_type', 'status', 'file_path', 'file_size',
            'record_count', 'created_at', 'completed_at'
        ]
        read_only_fields = ['id', 'created_at', 'completed_at']


class ConfigurationUpdateSerializer(serializers.Serializer):
    """
    Serializer para actualizaciones de configuración.
    """
    
    config_type = serializers.ChoiceField(choices=SystemConfiguration.CONFIG_TYPES)
    key = serializers.CharField(max_length=100)
    value = serializers.JSONField()
    description = serializers.CharField(required=False, allow_blank=True)


class BusinessSettingsUpdateSerializer(serializers.Serializer):
    """
    Serializer para actualizaciones de configuraciones de negocio.
    """
    
    company_name = serializers.CharField(max_length=200, required=False)
    address = serializers.CharField(required=False)
    phone = serializers.CharField(max_length=20, required=False)
    email = serializers.EmailField(required=False)
    website = serializers.URLField(required=False, allow_blank=True)
    tax_id = serializers.CharField(max_length=20, required=False)
    currency = serializers.ChoiceField(choices=BusinessSettings._meta.get_field('currency').choices, required=False)
    logo_url = serializers.URLField(required=False, allow_blank=True)
    timezone = serializers.CharField(max_length=50, required=False)
    language = serializers.ChoiceField(choices=BusinessSettings._meta.get_field('language').choices, required=False)


class SecuritySettingsUpdateSerializer(serializers.Serializer):
    """
    Serializer para actualizaciones de configuraciones de seguridad.
    """
    
    two_factor_auth = serializers.BooleanField(required=False)
    session_timeout = serializers.IntegerField(min_value=5, max_value=1440, required=False)
    password_expiry = serializers.BooleanField(required=False)
    password_expiry_days = serializers.IntegerField(min_value=1, max_value=365, required=False)
    max_login_attempts = serializers.IntegerField(min_value=3, max_value=10, required=False)
    lockout_duration = serializers.IntegerField(min_value=5, max_value=60, required=False)
    min_password_length = serializers.IntegerField(min_value=6, max_value=20, required=False)
    require_uppercase = serializers.BooleanField(required=False)
    require_lowercase = serializers.BooleanField(required=False)
    require_numbers = serializers.BooleanField(required=False)
    require_special_chars = serializers.BooleanField(required=False)


class ServiceConfigurationUpdateSerializer(serializers.Serializer):
    """
    Serializer para actualizaciones de configuraciones de servicios.
    """
    
    service_name = serializers.ChoiceField(choices=ServiceConfiguration.SERVICE_TYPES, required=False)
    base_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    status = serializers.ChoiceField(choices=ServiceConfiguration.STATUS_CHOICES, required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    estimated_duration = serializers.IntegerField(min_value=1, required=False)
    requires_approval = serializers.BooleanField(required=False)


class UserRoleUpdateSerializer(serializers.Serializer):
    """
    Serializer para actualizaciones de roles de usuario.
    """
    
    role_name = serializers.ChoiceField(choices=UserRole.ROLE_TYPES, required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    can_manage_users = serializers.BooleanField(required=False)
    can_manage_orders = serializers.BooleanField(required=False)
    can_manage_inventory = serializers.BooleanField(required=False)
    can_manage_production = serializers.BooleanField(required=False)
    can_manage_reports = serializers.BooleanField(required=False)
    can_manage_settings = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)


class DataExportSerializer(serializers.Serializer):
    """
    Serializer para exportación de datos.
    """
    
    export_type = serializers.ChoiceField(choices=[
        ('full', 'Exportación Completa'),
        ('clients', 'Solo Clientes'),
        ('orders', 'Solo Pedidos'),
        ('inventory', 'Solo Inventario'),
        ('production', 'Solo Producción'),
    ])
    format = serializers.ChoiceField(choices=[
        ('json', 'JSON'),
        ('csv', 'CSV'),
        ('excel', 'Excel'),
    ])
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)


class DataImportSerializer(serializers.Serializer):
    """
    Serializer para importación de datos.
    """
    
    file = serializers.FileField()
    import_type = serializers.ChoiceField(choices=[
        ('full', 'Importación Completa'),
        ('clients', 'Solo Clientes'),
        ('orders', 'Solo Pedidos'),
        ('inventory', 'Solo Inventario'),
        ('production', 'Solo Producción'),
    ])
    overwrite_existing = serializers.BooleanField(default=False)
