"""
Modelos para el sistema de notificaciones del fotostudio.

Este módulo define los modelos para gestionar notificaciones del sistema,
incluyendo alertas, notificaciones en tiempo real y recordatorios.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.tenants.models import Tenant


class Notification(models.Model):
    """
    Modelo para notificaciones del sistema.
    
    Almacena notificaciones que se muestran a los usuarios,
    incluyendo alertas, recordatorios y mensajes del sistema.
    """
    
    NOTIFICATION_TYPES = [
        ('info', 'Informativo'),
        ('success', 'Éxito'),
        ('warning', 'Advertencia'),
        ('error', 'Error'),
        ('alerta', 'Alerta'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('urgent', 'Urgente'),
    ]
    
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='notifications')
    
    # Información de la notificación
    title = models.CharField(max_length=200, help_text="Título de la notificación")
    message = models.TextField(help_text="Mensaje de la notificación")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='info')
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='medium')
    
    # Destinatarios
    user = models.ForeignKey('users.Users', on_delete=models.CASCADE, null=True, blank=True, 
                           help_text="Usuario específico (null = todos los usuarios)")
    role = models.CharField(max_length=50, blank=True, null=True, 
                          help_text="Rol específico (null = todos los roles)")
    
    # Estado y metadatos
    is_read = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    auto_remove = models.BooleanField(default=True, help_text="Eliminar automáticamente después de ser leída")
    duration = models.IntegerField(default=5000, help_text="Duración en milisegundos")
    
    # Fechas
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True, help_text="Fecha de expiración")
    
    # Datos adicionales
    metadata = models.JSONField(default=dict, blank=True, help_text="Datos adicionales en formato JSON")
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['tenant', 'notification_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.get_notification_type_display()}"
    
    @property
    def is_expired(self):
        """Verifica si la notificación ha expirado."""
        if not self.expires_at:
            return False
        return timezone.now() > self.expires_at


class Alert(models.Model):
    """
    Modelo para alertas del sistema.
    
    Almacena alertas específicas como stock bajo, fechas de vencimiento,
    recordatorios de citas, etc.
    """
    
    ALERT_TYPES = [
        ('stock_low', 'Stock Bajo'),
        ('stock_out', 'Stock Agotado'),
        ('appointment_reminder', 'Recordatorio de Cita'),
        ('deadline_approaching', 'Fecha Límite Próxima'),
        ('payment_due', 'Pago Pendiente'),
        ('system_maintenance', 'Mantenimiento del Sistema'),
        ('security_breach', 'Brecha de Seguridad'),
        ('backup_failed', 'Respaldo Fallido'),
    ]
    
    SEVERITY_LEVELS = [
        ('info', 'Informativo'),
        ('warning', 'Advertencia'),
        ('error', 'Error'),
        ('critical', 'Crítico'),
    ]
    
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='alerts')
    
    # Información de la alerta
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS, default='warning')
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Contexto de la alerta
    related_model = models.CharField(max_length=50, blank=True, null=True, 
                                   help_text="Modelo relacionado (ej: 'inventory', 'order')")
    related_id = models.IntegerField(blank=True, null=True, 
                                   help_text="ID del objeto relacionado")
    
    # Destinatarios
    user = models.ForeignKey('users.Users', on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    
    # Estado
    is_resolved = models.BooleanField(default=False)
    is_acknowledged = models.BooleanField(default=False)
    auto_resolve = models.BooleanField(default=False, help_text="Resolver automáticamente")
    
    # Fechas
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    acknowledged_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    
    # Datos adicionales
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'alerts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['alert_type', 'is_resolved']),
            models.Index(fields=['severity', 'is_acknowledged']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.title}"
    
    @property
    def is_expired(self):
        """Verifica si la alerta ha expirado."""
        if not self.expires_at:
            return False
        return timezone.now() > self.expires_at


class NotificationTemplate(models.Model):
    """
    Modelo para plantillas de notificaciones.
    
    Almacena plantillas reutilizables para diferentes tipos
    de notificaciones del sistema.
    """
    
    TEMPLATE_TYPES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('in_app', 'Notificación en App'),
    ]
    
    id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='notification_templates')
    
    # Información de la plantilla
    name = models.CharField(max_length=100, help_text="Nombre de la plantilla")
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES)
    subject = models.CharField(max_length=200, blank=True, null=True, help_text="Asunto (para email)")
    content = models.TextField(help_text="Contenido de la plantilla")
    
    # Variables disponibles
    variables = models.JSONField(default=list, blank=True, 
                               help_text="Lista de variables disponibles en la plantilla")
    
    # Configuración
    is_active = models.BooleanField(default=True)
    is_system = models.BooleanField(default=False, help_text="Plantilla del sistema")
    
    # Metadatos
    created_by = models.ForeignKey('users.Users', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notification_templates'
        unique_together = ['tenant', 'name', 'template_type']
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.get_template_type_display()}"


class NotificationPreference(models.Model):
    """
    Modelo para preferencias de notificaciones de usuarios.
    
    Almacena las preferencias de cada usuario sobre qué tipos
    de notificaciones desea recibir y cómo.
    """
    
    NOTIFICATION_CHANNELS = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('in_app', 'Notificación en App'),
    ]
    
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField('users.Users', on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Preferencias por tipo de notificación
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=True)
    in_app_notifications = models.BooleanField(default=True)
    
    # Preferencias por tipo de alerta
    stock_alerts = models.BooleanField(default=True)
    appointment_reminders = models.BooleanField(default=True)
    deadline_alerts = models.BooleanField(default=True)
    payment_reminders = models.BooleanField(default=True)
    system_notifications = models.BooleanField(default=True)
    
    # Configuraciones adicionales
    quiet_hours_start = models.TimeField(blank=True, null=True, help_text="Inicio de horas silenciosas")
    quiet_hours_end = models.TimeField(blank=True, null=True, help_text="Fin de horas silenciosas")
    timezone = models.CharField(max_length=50, default='America/Lima')
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notification_preferences'
    
    def __str__(self):
        return f"Preferencias de {self.user.username}"


class NotificationLog(models.Model):
    """
    Modelo para logs de notificaciones.
    
    Almacena el historial de notificaciones enviadas para
    auditoría y seguimiento.
    """
    
    STATUS_CHOICES = [
        ('sent', 'Enviado'),
        ('delivered', 'Entregado'),
        ('read', 'Leído'),
        ('failed', 'Fallido'),
        ('bounced', 'Rebotado'),
    ]
    
    id = models.AutoField(primary_key=True)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='logs')
    user = models.ForeignKey('users.Users', on_delete=models.CASCADE, null=True, blank=True)
    
    # Información del envío
    channel = models.CharField(max_length=20, choices=NotificationPreference.NOTIFICATION_CHANNELS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    
    # Detalles del envío
    sent_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    read_at = models.DateTimeField(blank=True, null=True)
    
    # Información adicional
    error_message = models.TextField(blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'notification_logs'
        ordering = ['-sent_at']
        indexes = [
            models.Index(fields=['notification', 'status']),
            models.Index(fields=['user', 'sent_at']),
        ]
    
    def __str__(self):
        return f"Log {self.id} - {self.get_status_display()}"