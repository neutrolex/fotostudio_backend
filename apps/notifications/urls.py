"""
URLs para la aplicación de notificaciones del fotostudio.
"""

from django.urls import path
from .views import (
    NotificationListView, NotificationDetailView,
    AlertListView, AlertDetailView,
    NotificationPreferenceView, MarkNotificationsAsReadView,
    MarkAlertsAsResolvedView, NotificationStatsView,
    CreateNotificationView, CreateAlertView,
    ClearNotificationsView
)

urlpatterns = [
    # Notificaciones
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('mark-read/', MarkNotificationsAsReadView.as_view(), name='mark-notifications-read'),
    path('clear/', ClearNotificationsView.as_view(), name='clear-notifications'),
    
    # Alertas
    path('alerts/', AlertListView.as_view(), name='alert-list'),
    path('alerts/<int:pk>/', AlertDetailView.as_view(), name='alert-detail'),
    path('alerts/mark-resolved/', MarkAlertsAsResolvedView.as_view(), name='mark-alerts-resolved'),
    
    # Preferencias de notificaciones
    path('preferences/', NotificationPreferenceView.as_view(), name='notification-preferences'),
    
    # Estadísticas
    path('stats/', NotificationStatsView.as_view(), name='notification-stats'),
    
    # Creación de notificaciones y alertas
    path('create/', CreateNotificationView.as_view(), name='create-notification'),
    path('alerts/create/', CreateAlertView.as_view(), name='create-alert'),
]
