"""
Vistas para la aplicación de notificaciones del fotostudio.
"""

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db.models import Q
from django.utils import timezone

from .models import (
    Notification, Alert, NotificationTemplate, 
    NotificationPreference, NotificationLog
)
from .serializers import (
    NotificationSerializer, AlertSerializer, NotificationTemplateSerializer,
    NotificationPreferenceSerializer, NotificationLogSerializer,
    CreateNotificationSerializer, CreateAlertSerializer,
    NotificationPreferenceUpdateSerializer, MarkAsReadSerializer,
    MarkAsResolvedSerializer, NotificationStatsSerializer,
    BulkNotificationSerializer, NotificationFilterSerializer,
    AlertFilterSerializer
)


class NotificationListView(ListCreateAPIView):
    """Vista para listar y crear notificaciones."""
    
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Notification.objects.filter(
            Q(tenant_id=self.request.user.tenant_id) &
            (Q(user=self.request.user) | Q(user__isnull=True))
        )
        
        # Aplicar filtros
        notification_type = self.request.query_params.get('notification_type')
        priority = self.request.query_params.get('priority')
        is_read = self.request.query_params.get('is_read')
        search = self.request.query_params.get('search')
        
        if notification_type:
            queryset = queryset.filter(notification_type=notification_type)
        if priority:
            queryset = queryset.filter(priority=priority)
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read.lower() == 'true')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(message__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(tenant_id=self.request.user.tenant_id, user=self.request.user)


class NotificationDetailView(RetrieveUpdateDestroyAPIView):
    """Vista para gestionar una notificación específica."""
    
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(
            Q(tenant_id=self.request.user.tenant_id) &
            (Q(user=self.request.user) | Q(user__isnull=True))
        )
    
    def retrieve(self, request, *args, **kwargs):
        """Marcar como leída al obtener detalles."""
        instance = self.get_object()
        if not instance.is_read:
            instance.is_read = True
            instance.read_at = timezone.now()
            instance.save()
        return super().retrieve(request, *args, **kwargs)


class AlertListView(ListCreateAPIView):
    """Vista para listar y crear alertas."""
    
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Alert.objects.filter(
            Q(tenant_id=self.request.user.tenant_id) &
            (Q(user=self.request.user) | Q(user__isnull=True))
        )
        
        # Aplicar filtros
        alert_type = self.request.query_params.get('alert_type')
        severity = self.request.query_params.get('severity')
        is_resolved = self.request.query_params.get('is_resolved')
        is_acknowledged = self.request.query_params.get('is_acknowledged')
        related_model = self.request.query_params.get('related_model')
        search = self.request.query_params.get('search')
        
        if alert_type:
            queryset = queryset.filter(alert_type=alert_type)
        if severity:
            queryset = queryset.filter(severity=severity)
        if is_resolved is not None:
            queryset = queryset.filter(is_resolved=is_resolved.lower() == 'true')
        if is_acknowledged is not None:
            queryset = queryset.filter(is_acknowledged=is_acknowledged.lower() == 'true')
        if related_model:
            queryset = queryset.filter(related_model=related_model)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(message__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(tenant_id=self.request.user.tenant_id, user=self.request.user)


class AlertDetailView(RetrieveUpdateDestroyAPIView):
    """Vista para gestionar una alerta específica."""
    
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Alert.objects.filter(
            Q(tenant_id=self.request.user.tenant_id) &
            (Q(user=self.request.user) | Q(user__isnull=True))
        )


class NotificationPreferenceView(APIView):
    """Vista para gestionar preferencias de notificaciones."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Obtener preferencias de notificaciones del usuario."""
        try:
            preferences = NotificationPreference.objects.get(user=request.user)
            serializer = NotificationPreferenceSerializer(preferences)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NotificationPreference.DoesNotExist:
            # Crear preferencias por defecto
            preferences = NotificationPreference.objects.create(user=request.user)
            serializer = NotificationPreferenceSerializer(preferences)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """Actualizar preferencias de notificaciones."""
        serializer = NotificationPreferenceUpdateSerializer(data=request.data)
        if serializer.is_valid():
            preferences, created = NotificationPreference.objects.update_or_create(
                user=request.user,
                defaults=serializer.validated_data
            )
            
            return Response({
                'message': 'Preferencias actualizadas correctamente',
                'preferences': NotificationPreferenceSerializer(preferences).data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarkNotificationsAsReadView(APIView):
    """Vista para marcar notificaciones como leídas."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Marcar notificaciones como leídas."""
        serializer = MarkAsReadSerializer(data=request.data)
        if serializer.is_valid():
            notification_ids = serializer.validated_data['notification_ids']
            
            updated_count = Notification.objects.filter(
                id__in=notification_ids,
                tenant_id=request.user.tenant_id,
                user=request.user
            ).update(
                is_read=True,
                read_at=timezone.now()
            )
            
            return Response({
                'message': f'{updated_count} notificaciones marcadas como leídas'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarkAlertsAsResolvedView(APIView):
    """Vista para marcar alertas como resueltas."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Marcar alertas como resueltas."""
        serializer = MarkAsResolvedSerializer(data=request.data)
        if serializer.is_valid():
            alert_ids = serializer.validated_data['alert_ids']
            
            updated_count = Alert.objects.filter(
                id__in=alert_ids,
                tenant_id=request.user.tenant_id,
                user=request.user
            ).update(
                is_resolved=True,
                resolved_at=timezone.now()
            )
            
            return Response({
                'message': f'{updated_count} alertas marcadas como resueltas'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationStatsView(APIView):
    """Vista para obtener estadísticas de notificaciones."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Obtener estadísticas de notificaciones."""
        # Estadísticas de notificaciones
        notifications = Notification.objects.filter(
            tenant_id=request.user.tenant_id,
            user=request.user
        )
        
        total_notifications = notifications.count()
        unread_notifications = notifications.filter(is_read=False).count()
        
        # Estadísticas de alertas
        alerts = Alert.objects.filter(
            tenant_id=request.user.tenant_id,
            user=request.user
        )
        
        total_alerts = alerts.count()
        unresolved_alerts = alerts.filter(is_resolved=False).count()
        
        # Notificaciones por tipo
        notifications_by_type = {}
        for notification_type, _ in Notification.NOTIFICATION_TYPES:
            count = notifications.filter(notification_type=notification_type).count()
            notifications_by_type[notification_type] = count
        
        # Alertas por tipo
        alerts_by_type = {}
        for alert_type, _ in Alert.ALERT_TYPES:
            count = alerts.filter(alert_type=alert_type).count()
            alerts_by_type[alert_type] = count
        
        # Notificaciones recientes
        recent_notifications = notifications.order_by('-created_at')[:5]
        recent_alerts = alerts.order_by('-created_at')[:5]
        
        stats = {
            'total_notifications': total_notifications,
            'unread_notifications': unread_notifications,
            'total_alerts': total_alerts,
            'unresolved_alerts': unresolved_alerts,
            'notifications_by_type': notifications_by_type,
            'alerts_by_type': alerts_by_type,
            'recent_notifications': NotificationSerializer(recent_notifications, many=True).data,
            'recent_alerts': AlertSerializer(recent_alerts, many=True).data
        }
        
        return Response(stats, status=status.HTTP_200_OK)


class CreateNotificationView(APIView):
    """Vista para crear notificaciones individuales."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Crear una notificación."""
        serializer = CreateNotificationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Determinar destinatario
            user = None
            if data.get('user_id'):
                try:
                    from apps.users.models import Users
                    user = Users.objects.get(id=data['user_id'], tenant_id=request.user.tenant_id)
                except Users.DoesNotExist:
                    return Response({'error': 'Usuario no encontrado'}, 
                                  status=status.HTTP_404_NOT_FOUND)
            
            # Crear notificación
            notification = Notification.objects.create(
                tenant_id=request.user.tenant_id,
                user=user,
                role=data.get('role'),
                title=data['title'],
                message=data['message'],
                notification_type=data['notification_type'],
                priority=data['priority'],
                auto_remove=data['auto_remove'],
                duration=data['duration'],
                expires_at=data.get('expires_at'),
                metadata=data.get('metadata', {})
            )
            
            return Response({
                'message': 'Notificación creada correctamente',
                'notification': NotificationSerializer(notification).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateAlertView(APIView):
    """Vista para crear alertas individuales."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Crear una alerta."""
        serializer = CreateAlertSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Determinar destinatario
            user = None
            if data.get('user_id'):
                try:
                    from apps.users.models import Users
                    user = Users.objects.get(id=data['user_id'], tenant_id=request.user.tenant_id)
                except Users.DoesNotExist:
                    return Response({'error': 'Usuario no encontrado'}, 
                                  status=status.HTTP_404_NOT_FOUND)
            
            # Crear alerta
            alert = Alert.objects.create(
                tenant_id=request.user.tenant_id,
                user=user,
                role=data.get('role'),
                alert_type=data['alert_type'],
                severity=data['severity'],
                title=data['title'],
                message=data['message'],
                related_model=data.get('related_model'),
                related_id=data.get('related_id'),
                auto_resolve=data['auto_resolve'],
                expires_at=data.get('expires_at'),
                metadata=data.get('metadata', {})
            )
            
            return Response({
                'message': 'Alerta creada correctamente',
                'alert': AlertSerializer(alert).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClearNotificationsView(APIView):
    """Vista para limpiar notificaciones."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Limpiar notificaciones del usuario."""
        notification_type = request.data.get('notification_type')
        older_than_days = request.data.get('older_than_days', 30)
        
        # Calcular fecha límite
        cutoff_date = timezone.now() - timezone.timedelta(days=older_than_days)
        
        # Construir queryset
        queryset = Notification.objects.filter(
            tenant_id=request.user.tenant_id,
            user=request.user,
            created_at__lt=cutoff_date
        )
        
        if notification_type:
            queryset = queryset.filter(notification_type=notification_type)
        
        # Eliminar notificaciones
        deleted_count = queryset.count()
        queryset.delete()
        
        return Response({
            'message': f'{deleted_count} notificaciones eliminadas'
        }, status=status.HTTP_200_OK)
