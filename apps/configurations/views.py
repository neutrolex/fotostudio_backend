"""
Vistas para la aplicación de configuraciones del fotostudio.
"""

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.utils import timezone
from django.http import JsonResponse

from .models import (
    SystemConfiguration, BusinessSettings, SecuritySettings,
    ServiceConfiguration, UserRole, DataBackup
)
from .serializers import (
    SystemConfigurationSerializer, BusinessSettingsSerializer, SecuritySettingsSerializer,
    ServiceConfigurationSerializer, UserRoleSerializer, DataBackupSerializer,
    ConfigurationUpdateSerializer, BusinessSettingsUpdateSerializer,
    SecuritySettingsUpdateSerializer, ServiceConfigurationUpdateSerializer,
    UserRoleUpdateSerializer, DataExportSerializer, DataImportSerializer
)


class SystemConfigurationView(APIView):
    """Vista para gestionar configuraciones del sistema."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Obtener todas las configuraciones del sistema."""
        configs = SystemConfiguration.objects.filter(
            tenant_id=request.user.tenant_id,
            is_active=True
        )
        
        # Agrupar por tipo
        grouped_configs = {}
        for config in configs:
            config_type = config.config_type
            if config_type not in grouped_configs:
                grouped_configs[config_type] = {}
            grouped_configs[config_type][config.key] = config.value
        
        return Response(grouped_configs, status=status.HTTP_200_OK)
    
    def post(self, request):
        """Crear o actualizar configuración del sistema."""
        serializer = ConfigurationUpdateSerializer(data=request.data)
        if serializer.is_valid():
            config_type = serializer.validated_data['config_type']
            key = serializer.validated_data['key']
            value = serializer.validated_data['value']
            description = serializer.validated_data.get('description', '')
            
            config, created = SystemConfiguration.objects.update_or_create(
                tenant_id=request.user.tenant_id,
                config_type=config_type,
                key=key,
                defaults={
                    'value': value,
                    'description': description,
                    'created_by': request.user
                }
            )
            
            return Response({
                'message': 'Configuración actualizada correctamente',
                'config': SystemConfigurationSerializer(config).data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessSettingsView(APIView):
    """Vista para gestionar configuraciones de negocio."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Obtener configuraciones de negocio."""
        try:
            business_settings = BusinessSettings.objects.get(tenant_id=request.user.tenant_id)
            serializer = BusinessSettingsSerializer(business_settings)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BusinessSettings.DoesNotExist:
            # Crear configuración por defecto
            business_settings = BusinessSettings.objects.create(
                tenant_id=request.user.tenant_id
            )
            serializer = BusinessSettingsSerializer(business_settings)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """Actualizar configuraciones de negocio."""
        serializer = BusinessSettingsUpdateSerializer(data=request.data)
        if serializer.is_valid():
            business_settings, created = BusinessSettings.objects.update_or_create(
                tenant_id=request.user.tenant_id,
                defaults=serializer.validated_data
            )
            
            return Response({
                'message': 'Configuraciones de negocio actualizadas correctamente',
                'settings': BusinessSettingsSerializer(business_settings).data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        """Actualizar configuraciones de negocio (PUT)."""
        return self.post(request)
    
    def patch(self, request):
        """Actualizar configuraciones de negocio (PATCH)."""
        return self.post(request)


class SecuritySettingsView(APIView):
    """Vista para gestionar configuraciones de seguridad."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Obtener configuraciones de seguridad."""
        try:
            security_settings = SecuritySettings.objects.get(tenant_id=request.user.tenant_id)
            serializer = SecuritySettingsSerializer(security_settings)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SecuritySettings.DoesNotExist:
            # Crear configuración por defecto
            security_settings = SecuritySettings.objects.create(
                tenant_id=request.user.tenant_id
            )
            serializer = SecuritySettingsSerializer(security_settings)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """Actualizar configuraciones de seguridad."""
        serializer = SecuritySettingsUpdateSerializer(data=request.data)
        if serializer.is_valid():
            security_settings, created = SecuritySettings.objects.update_or_create(
                tenant_id=request.user.tenant_id,
                defaults=serializer.validated_data
            )
            
            return Response({
                'message': 'Configuraciones de seguridad actualizadas correctamente',
                'settings': SecuritySettingsSerializer(security_settings).data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceConfigurationListView(ListCreateAPIView):
    """Vista para listar y crear configuraciones de servicios."""
    
    serializer_class = ServiceConfigurationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ServiceConfiguration.objects.filter(tenant_id=self.request.user.tenant_id)
    
    def perform_create(self, serializer):
        serializer.save(tenant_id=self.request.user.tenant_id, created_by=self.request.user)


class ServiceConfigurationDetailView(RetrieveUpdateDestroyAPIView):
    """Vista para gestionar una configuración de servicio específica."""
    
    serializer_class = ServiceConfigurationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ServiceConfiguration.objects.filter(tenant_id=self.request.user.tenant_id)


class UserRoleListView(ListCreateAPIView):
    """Vista para listar y crear roles de usuario."""
    
    serializer_class = UserRoleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserRole.objects.filter(tenant_id=self.request.user.tenant_id)
    
    def perform_create(self, serializer):
        serializer.save(tenant_id=self.request.user.tenant_id)


class UserRoleDetailView(RetrieveUpdateDestroyAPIView):
    """Vista para gestionar un rol de usuario específico."""
    
    serializer_class = UserRoleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserRole.objects.filter(tenant_id=self.request.user.tenant_id)


class UserManagementView(APIView):
    """Vista para gestión de usuarios (compatible con frontend)."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Obtener lista de usuarios."""
        from apps.users.models import Users
        
        users = Users.objects.filter(tenant_id=request.user.tenant_id)
        
        user_list = []
        for user in users:
            user_list.append({
                'id': user.id,
                'usuario': user.username,
                'rol': 'Administrador' if user.is_superuser else 'Usuario',
                'estado': 'Activo' if user.is_active else 'Inactivo',
                'ultimoAcceso': user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else 'Nunca'
            })
        
        return Response(user_list, status=status.HTTP_200_OK)
    
    def post(self, request):
        """Crear nuevo usuario."""
        from apps.users.models import Users
        from django.contrib.auth.hashers import make_password
        
        username = request.data.get('usuario')
        rol = request.data.get('rol', 'Usuario')
        estado = request.data.get('estado', 'Activo')
        
        if not username:
            return Response({'error': 'El nombre de usuario es requerido'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Crear usuario
        user = Users.objects.create(
            username=username,
            email=f"{username}@example.com",
            password=make_password('password123'),
            tenant_id=request.user.tenant_id,
            is_superuser=(rol == 'Administrador'),
            is_active=(estado == 'Activo')
        )
        
        return Response({
            'message': 'Usuario creado correctamente',
            'user': {
                'id': user.id,
                'usuario': user.username,
                'rol': rol,
                'estado': estado,
                'ultimoAcceso': 'Nunca'
            }
        }, status=status.HTTP_201_CREATED)
    
    def put(self, request, user_id):
        """Actualizar usuario."""
        from apps.users.models import Users
        
        try:
            user = Users.objects.get(id=user_id, tenant_id=request.user.tenant_id)
        except Users.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        rol = request.data.get('rol', 'Usuario')
        estado = request.data.get('estado', 'Activo')
        
        user.is_superuser = (rol == 'Administrador')
        user.is_active = (estado == 'Activo')
        user.save()
        
        return Response({
            'message': 'Usuario actualizado correctamente',
            'user': {
                'id': user.id,
                'usuario': user.username,
                'rol': rol,
                'estado': estado,
                'ultimoAcceso': user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else 'Nunca'
            }
        }, status=status.HTTP_200_OK)
    
    def delete(self, request, user_id):
        """Eliminar usuario."""
        from apps.users.models import Users
        
        try:
            user = Users.objects.get(id=user_id, tenant_id=request.user.tenant_id)
        except Users.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        # No permitir eliminar el usuario actual
        if user.id == request.user.id:
            return Response({'error': 'No puedes eliminar tu propia cuenta'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        user.delete()
        return Response({'message': 'Usuario eliminado correctamente'}, 
                      status=status.HTTP_200_OK)


class DataExportView(APIView):
    """Vista para exportar datos del sistema."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Exportar datos del sistema."""
        serializer = DataExportSerializer(data=request.data)
        if serializer.is_valid():
            export_type = serializer.validated_data['export_type']
            format_type = serializer.validated_data['format']
            
            # Simular exportación de datos
            data = {'message': f'Datos de {export_type} exportados en formato {format_type}'}
            
            if format_type == 'json':
                response = JsonResponse(data, safe=False)
                response['Content-Disposition'] = f'attachment; filename="export_{export_type}_{timezone.now().strftime("%Y%m%d_%H%M%S")}.json"'
                return response
            
            return Response(data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DataImportView(APIView):
    """Vista para importar datos al sistema."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Importar datos al sistema."""
        serializer = DataImportSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            import_type = serializer.validated_data['import_type']
            
            return Response({
                'message': f'Datos de {import_type} importados correctamente',
                'records_imported': 0,
                'records_updated': 0,
                'errors': []
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfigurationResetView(APIView):
    """Vista para resetear configuraciones."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Resetear configuraciones a valores por defecto."""
        config_type = request.data.get('config_type')
        
        if config_type == 'business':
            BusinessSettings.objects.filter(tenant_id=request.user.tenant_id).delete()
            BusinessSettings.objects.create(tenant_id=request.user.tenant_id)
        elif config_type == 'security':
            SecuritySettings.objects.filter(tenant_id=request.user.tenant_id).delete()
            SecuritySettings.objects.create(tenant_id=request.user.tenant_id)
        elif config_type == 'all':
            BusinessSettings.objects.filter(tenant_id=request.user.tenant_id).delete()
            SecuritySettings.objects.filter(tenant_id=request.user.tenant_id).delete()
            SystemConfiguration.objects.filter(tenant_id=request.user.tenant_id).delete()
            
            BusinessSettings.objects.create(tenant_id=request.user.tenant_id)
            SecuritySettings.objects.create(tenant_id=request.user.tenant_id)
        
        return Response({
            'message': f'Configuraciones de {config_type} reseteadas correctamente'
        }, status=status.HTTP_200_OK)
