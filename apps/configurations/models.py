"""
Modelos para el sistema de configuraciones del fotostudio.

Este módulo define los modelos para gestionar configuraciones del sistema,
incluyendo configuraciones de empresa, seguridad, servicios y usuarios.
"""

from django.db import models
from django.contrib.auth.models import User
from apps.tenants.models import Tenant


class SystemConfiguration(models.Model):
    """
    Modelo para configuraciones generales del sistema.
    
    Almacena configuraciones globales como información de la empresa,
    configuraciones de seguridad, y otros ajustes del sistema.
    """
    
    CONFIG_TYPES = [
        ('business', 'Configuración de Negocio'),
        ('security', 'Configuración de Seguridad'),
        ('system', 'Configuración del Sistema'),
        ('ui', 'Configuración de Interfaz'),
    ]
    
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='configurations')
    config_type = models.CharField(max_length=20, choices=CONFIG_TYPES)
    key = models.CharField(max_length=100, help_text="Clave de configuración")
    value = models.JSONField(help_text="Valor de configuración (JSON)")
    description = models.TextField(blank=True, null=True, help_text="Descripción de la configuración")
    
    # Metadatos
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey('users.Users', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'system_configurations'
        unique_together = ['tenant', 'config_type', 'key']
        ordering = ['config_type', 'key']
    
    def __str__(self):
        return f"{self.get_config_type_display()} - {self.key}"


class BusinessSettings(models.Model):
    """
    Modelo para configuraciones específicas del negocio.
    
    Almacena información de la empresa como nombre, dirección,
    datos fiscales, etc.
    """
    
    id = models.AutoField(primary_key=True)
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='business_settings')
    
    # Información de la empresa
    company_name = models.CharField(max_length=200, default='Arte Ideas Diseño Gráfico')
    address = models.TextField(default='Av. Lima 123, San Juan de Lurigancho')
    phone = models.CharField(max_length=20, default='987654321')
    email = models.EmailField(default='info@arteideas.com')
    website = models.URLField(blank=True, null=True)
    
    # Datos fiscales
    tax_id = models.CharField(max_length=20, default='20123456789', help_text="RUC")
    currency = models.CharField(max_length=3, default='PEN', choices=[
        ('PEN', 'Soles (S/)'),
        ('USD', 'Dólares (USD)'),
        ('EUR', 'Euros (EUR)'),
    ])
    
    # Configuraciones adicionales
    logo_url = models.URLField(blank=True, null=True)
    timezone = models.CharField(max_length=50, default='America/Lima')
    language = models.CharField(max_length=5, default='es', choices=[
        ('es', 'Español'),
        ('en', 'English'),
    ])
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'business_settings'
    
    def __str__(self):
        return f"Configuración de {self.company_name}"


class SecuritySettings(models.Model):
    """
    Modelo para configuraciones de seguridad.
    
    Almacena configuraciones relacionadas con la seguridad del sistema
    como autenticación de dos factores, expiración de contraseñas, etc.
    """
    
    id = models.AutoField(primary_key=True)
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='security_settings')
    
    # Configuraciones de autenticación
    two_factor_auth = models.BooleanField(default=False, help_text="Autenticación de dos factores")
    session_timeout = models.IntegerField(default=30, help_text="Timeout de sesión en minutos")
    password_expiry = models.BooleanField(default=False, help_text="Expiración de contraseña")
    password_expiry_days = models.IntegerField(default=90, help_text="Días para expiración de contraseña")
    
    # Configuraciones de login
    max_login_attempts = models.IntegerField(default=5, help_text="Máximo intentos de login")
    lockout_duration = models.IntegerField(default=15, help_text="Duración del bloqueo en minutos")
    
    # Configuraciones de contraseña
    min_password_length = models.IntegerField(default=8, help_text="Longitud mínima de contraseña")
    require_uppercase = models.BooleanField(default=True, help_text="Requerir mayúsculas")
    require_lowercase = models.BooleanField(default=True, help_text="Requerir minúsculas")
    require_numbers = models.BooleanField(default=True, help_text="Requerir números")
    require_special_chars = models.BooleanField(default=True, help_text="Requerir caracteres especiales")
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'security_settings'
    
    def __str__(self):
        return f"Configuración de Seguridad - {self.tenant.name}"


class ServiceConfiguration(models.Model):
    """
    Modelo para configuraciones de servicios.
    
    Almacena configuraciones de servicios ofrecidos por la empresa
    como precios base, estados, etc.
    """
    
    SERVICE_TYPES = [
        ('Impresión Digital', 'Impresión Digital'),
        ('Fotografía Escolar', 'Fotografía Escolar'),
        ('Promoción Escolar', 'Promoción Escolar'),
        ('Enmarcado', 'Enmarcado'),
        ('Retoque Fotográfico', 'Retoque Fotográfico'),
        ('Recordatorios', 'Recordatorios'),
        ('Ampliaciones', 'Ampliaciones'),
        ('Fotografía de Eventos', 'Fotografía de Eventos'),
        ('Sesión Familiar', 'Sesión Familiar'),
    ]
    
    STATUS_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
        ('Mantenimiento', 'Mantenimiento'),
    ]
    
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='service_configurations')
    
    # Información del servicio
    service_name = models.CharField(max_length=100, choices=SERVICE_TYPES)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Activo')
    
    # Configuraciones adicionales
    description = models.TextField(blank=True, null=True)
    estimated_duration = models.IntegerField(blank=True, null=True, help_text="Duración estimada en días")
    requires_approval = models.BooleanField(default=False, help_text="Requiere aprobación")
    
    # Metadatos
    created_by = models.ForeignKey('users.Users', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'service_configurations'
        unique_together = ['tenant', 'service_name']
        ordering = ['service_name']
    
    def __str__(self):
        return f"{self.service_name} - {self.get_status_display()}"


class UserRole(models.Model):
    """
    Modelo para roles de usuario.
    
    Define los diferentes roles que pueden tener los usuarios
    en el sistema.
    """
    
    ROLE_TYPES = [
        ('Administrador', 'Administrador'),
        ('Editor', 'Editor'),
        ('Usuario', 'Usuario'),
        ('Vendedor', 'Vendedor'),
        ('Fotógrafo', 'Fotógrafo'),
        ('Editor Gráfico', 'Editor Gráfico'),
    ]
    
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='user_roles')
    
    # Información del rol
    role_name = models.CharField(max_length=50, choices=ROLE_TYPES)
    description = models.TextField(blank=True, null=True)
    
    # Permisos
    can_manage_users = models.BooleanField(default=False)
    can_manage_orders = models.BooleanField(default=False)
    can_manage_inventory = models.BooleanField(default=False)
    can_manage_production = models.BooleanField(default=False)
    can_manage_reports = models.BooleanField(default=False)
    can_manage_settings = models.BooleanField(default=False)
    
    # Metadatos
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_roles'
        unique_together = ['tenant', 'role_name']
        ordering = ['role_name']
    
    def __str__(self):
        return f"{self.role_name} - {self.tenant.name}"


class DataBackup(models.Model):
    """
    Modelo para respaldos de datos.
    
    Almacena información sobre respaldos realizados del sistema.
    """
    
    BACKUP_TYPES = [
        ('full', 'Respaldo Completo'),
        ('incremental', 'Respaldo Incremental'),
        ('differential', 'Respaldo Diferencial'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('in_progress', 'En Progreso'),
        ('completed', 'Completado'),
        ('failed', 'Fallido'),
    ]
    
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='data_backups')
    
    # Información del respaldo
    backup_type = models.CharField(max_length=20, choices=BACKUP_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Detalles del archivo
    file_path = models.CharField(max_length=500, blank=True, null=True)
    file_size = models.BigIntegerField(default=0, help_text="Tamaño del archivo en bytes")
    record_count = models.IntegerField(default=0, help_text="Número de registros respaldados")
    
    # Metadatos
    created_by = models.ForeignKey('users.Users', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'data_backups'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Respaldo {self.get_backup_type_display()} - {self.get_status_display()}"