"""
Serializers para la aplicación de notificaciones del fotostudio.

Este módulo define todos los serializers necesarios para la validación,
serialización y deserialización de datos relacionados con notificaciones.
"""

from rest_framework import serializers
from .models import (
    Notification, Alert, NotificationTemplate, 
    NotificationPreference, NotificationLog
)


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer para notificaciones.
    """
    
    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'message', 'notification_type', 'priority',
            'user', 'role', 'is_read', 'is_active', 'auto_remove',
            'duration', 'created_at', 'read_at', 'expires_at', 'metadata'
        ]
        read_only_fields = ['id', 'created_at', 'read_at']


class AlertSerializer(serializers.ModelSerializer):
    """
    Serializer para alertas.
    """
    
    class Meta:
        model = Alert
        fields = [
            'id', 'alert_type', 'severity', 'title', 'message',
            'related_model', 'related_id', 'user', 'role',
            'is_resolved', 'is_acknowledged', 'auto_resolve',
            'created_at', 'resolved_at', 'acknowledged_at',
            'expires_at', 'metadata'
        ]
        read_only_fields = ['id', 'created_at', 'resolved_at', 'acknowledged_at']


class NotificationTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer para plantillas de notificaciones.
    """
    
    class Meta:
        model = NotificationTemplate
        fields = [
            'id', 'name', 'template_type', 'subject', 'content',
            'variables', 'is_active', 'is_system', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """
    Serializer para preferencias de notificaciones.
    """
    
    class Meta:
        model = NotificationPreference
        fields = [
            'id', 'email_notifications', 'sms_notifications',
            'push_notifications', 'in_app_notifications', 'stock_alerts',
            'appointment_reminders', 'deadline_alerts', 'payment_reminders',
            'system_notifications', 'quiet_hours_start', 'quiet_hours_end',
            'timezone', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class NotificationLogSerializer(serializers.ModelSerializer):
    """
    Serializer para logs de notificaciones.
    """
    
    class Meta:
        model = NotificationLog
        fields = [
            'id', 'notification', 'user', 'channel', 'status',
            'sent_at', 'delivered_at', 'read_at', 'error_message', 'metadata'
        ]
        read_only_fields = ['id', 'sent_at', 'delivered_at', 'read_at']


class CreateNotificationSerializer(serializers.Serializer):
    """
    Serializer para crear notificaciones.
    """
    
    title = serializers.CharField(max_length=200)
    message = serializers.CharField()
    notification_type = serializers.ChoiceField(choices=Notification.NOTIFICATION_TYPES, default='info')
    priority = serializers.ChoiceField(choices=Notification.PRIORITY_LEVELS, default='medium')
    user_id = serializers.IntegerField(required=False, allow_null=True)
    role = serializers.CharField(max_length=50, required=False, allow_blank=True)
    auto_remove = serializers.BooleanField(default=True)
    duration = serializers.IntegerField(default=5000, min_value=1000, max_value=30000)
    expires_at = serializers.DateTimeField(required=False, allow_null=True)
    metadata = serializers.JSONField(default=dict, required=False)


class CreateAlertSerializer(serializers.Serializer):
    """
    Serializer para crear alertas.
    """
    
    alert_type = serializers.ChoiceField(choices=Alert.ALERT_TYPES)
    severity = serializers.ChoiceField(choices=Alert.SEVERITY_LEVELS, default='warning')
    title = serializers.CharField(max_length=200)
    message = serializers.CharField()
    related_model = serializers.CharField(max_length=50, required=False, allow_blank=True)
    related_id = serializers.IntegerField(required=False, allow_null=True)
    user_id = serializers.IntegerField(required=False, allow_null=True)
    role = serializers.CharField(max_length=50, required=False, allow_blank=True)
    auto_resolve = serializers.BooleanField(default=False)
    expires_at = serializers.DateTimeField(required=False, allow_null=True)
    metadata = serializers.JSONField(default=dict, required=False)


class NotificationPreferenceUpdateSerializer(serializers.Serializer):
    """
    Serializer para actualizar preferencias de notificaciones.
    """
    
    email_notifications = serializers.BooleanField(required=False)
    sms_notifications = serializers.BooleanField(required=False)
    push_notifications = serializers.BooleanField(required=False)
    in_app_notifications = serializers.BooleanField(required=False)
    stock_alerts = serializers.BooleanField(required=False)
    appointment_reminders = serializers.BooleanField(required=False)
    deadline_alerts = serializers.BooleanField(required=False)
    payment_reminders = serializers.BooleanField(required=False)
    system_notifications = serializers.BooleanField(required=False)
    quiet_hours_start = serializers.TimeField(required=False, allow_null=True)
    quiet_hours_end = serializers.TimeField(required=False, allow_null=True)
    timezone = serializers.CharField(max_length=50, required=False)


class MarkAsReadSerializer(serializers.Serializer):
    """
    Serializer para marcar notificaciones como leídas.
    """
    
    notification_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )


class MarkAsResolvedSerializer(serializers.Serializer):
    """
    Serializer para marcar alertas como resueltas.
    """
    
    alert_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )


class NotificationStatsSerializer(serializers.Serializer):
    """
    Serializer para estadísticas de notificaciones.
    """
    
    total_notifications = serializers.IntegerField()
    unread_notifications = serializers.IntegerField()
    total_alerts = serializers.IntegerField()
    unresolved_alerts = serializers.IntegerField()
    notifications_by_type = serializers.DictField()
    alerts_by_type = serializers.DictField()
    recent_notifications = NotificationSerializer(many=True)
    recent_alerts = AlertSerializer(many=True)


class BulkNotificationSerializer(serializers.Serializer):
    """
    Serializer para envío masivo de notificaciones.
    """
    
    title = serializers.CharField(max_length=200)
    message = serializers.CharField()
    notification_type = serializers.ChoiceField(choices=Notification.NOTIFICATION_TYPES, default='info')
    priority = serializers.ChoiceField(choices=Notification.PRIORITY_LEVELS, default='medium')
    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True
    )
    role = serializers.CharField(max_length=50, required=False, allow_blank=True)
    auto_remove = serializers.BooleanField(default=True)
    duration = serializers.IntegerField(default=5000, min_value=1000, max_value=30000)
    expires_at = serializers.DateTimeField(required=False, allow_null=True)
    metadata = serializers.JSONField(default=dict, required=False)
    
    def validate(self, data):
        """
        Valida que se proporcione al menos un destinatario.
        """
        if not data.get('user_ids') and not data.get('role'):
            raise serializers.ValidationError(
                "Debe proporcionar al menos user_ids o role"
            )
        return data


class NotificationFilterSerializer(serializers.Serializer):
    """
    Serializer para filtros de notificaciones.
    """
    
    notification_type = serializers.ChoiceField(
        choices=Notification.NOTIFICATION_TYPES,
        required=False
    )
    priority = serializers.ChoiceField(
        choices=Notification.PRIORITY_LEVELS,
        required=False
    )
    is_read = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)
    date_from = serializers.DateTimeField(required=False)
    date_to = serializers.DateTimeField(required=False)
    search = serializers.CharField(max_length=200, required=False, allow_blank=True)


class AlertFilterSerializer(serializers.Serializer):
    """
    Serializer para filtros de alertas.
    """
    
    alert_type = serializers.ChoiceField(
        choices=Alert.ALERT_TYPES,
        required=False
    )
    severity = serializers.ChoiceField(
        choices=Alert.SEVERITY_LEVELS,
        required=False
    )
    is_resolved = serializers.BooleanField(required=False)
    is_acknowledged = serializers.BooleanField(required=False)
    related_model = serializers.CharField(max_length=50, required=False, allow_blank=True)
    date_from = serializers.DateTimeField(required=False)
    date_to = serializers.DateTimeField(required=False)
    search = serializers.CharField(max_length=200, required=False, allow_blank=True)
