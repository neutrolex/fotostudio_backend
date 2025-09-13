"""
URLs para la aplicación de configuraciones del fotostudio.
"""

from django.urls import path
from .views import (
    SystemConfigurationView, BusinessSettingsView, SecuritySettingsView,
    ServiceConfigurationListView, ServiceConfigurationDetailView,
    UserRoleListView, UserRoleDetailView, UserManagementView,
    DataExportView, DataImportView, ConfigurationResetView
)

urlpatterns = [
    # Configuraciones del sistema
    path('system/', SystemConfigurationView.as_view(), name='system-configuration'),
    
    # Configuraciones de negocio
    path('business/', BusinessSettingsView.as_view(), name='business-settings'),
    
    # Configuraciones de seguridad
    path('security/', SecuritySettingsView.as_view(), name='security-settings'),
    
    # Configuraciones de servicios
    path('services/', ServiceConfigurationListView.as_view(), name='service-configuration-list'),
    path('services/<int:pk>/', ServiceConfigurationDetailView.as_view(), name='service-configuration-detail'),
    
    # Roles de usuario
    path('roles/', UserRoleListView.as_view(), name='user-role-list'),
    path('roles/<int:pk>/', UserRoleDetailView.as_view(), name='user-role-detail'),
    
    # Gestión de usuarios
    path('users/', UserManagementView.as_view(), name='user-management'),
    path('users/<int:user_id>/', UserManagementView.as_view(), name='user-management-detail'),
    
    # Exportación e importación de datos
    path('export/', DataExportView.as_view(), name='data-export'),
    path('import/', DataImportView.as_view(), name='data-import'),
    
    # Reset de configuraciones
    path('reset/', ConfigurationResetView.as_view(), name='configuration-reset'),
]
