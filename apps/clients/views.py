"""
Vistas para la app de clientes.
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Client
from .serializers import ClientSerializer
from apps.users.permissions import CanManageClients


class ClientListView(generics.ListCreateAPIView):
    """
    Lista y creación de clientes.
    
    Permisos:
    - Administradores y empleados: Acceso completo (crear, leer, actualizar, eliminar)
    - Usuarios regulares: Solo lectura
    """
    serializer_class = ClientSerializer
    permission_classes = [CanManageClients]
    
    def get_queryset(self):
        """Filtrar clientes por tenant del usuario autenticado"""
        from apps.tenants.models import Tenant
        tenant = Tenant.objects.get(id=self.request.user.tenant_id)
        return Client.objects.filter(tenant=tenant)
    
    def perform_create(self, serializer):
        """Asignar automáticamente el tenant del usuario autenticado"""
        from apps.tenants.models import Tenant
        tenant = Tenant.objects.get(id=self.request.user.tenant_id)
        serializer.save(tenant=tenant)


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalle, actualización y eliminación de clientes.
    
    Permisos:
    - Administradores y empleados: Acceso completo
    - Usuarios regulares: Solo lectura
    """
    serializer_class = ClientSerializer
    permission_classes = [CanManageClients]
    
    def get_queryset(self):
        """Filtrar clientes por tenant del usuario autenticado"""
        from apps.tenants.models import Tenant
        tenant = Tenant.objects.get(id=self.request.user.tenant_id)
        return Client.objects.filter(tenant=tenant)


class ClientSearchView(APIView):
    """
    Búsqueda de clientes.
    
    Permisos:
    - Administradores y empleados: Acceso completo
    - Usuarios regulares: Solo lectura
    """
    permission_classes = [CanManageClients]
    
    def get(self, request):
        query = request.query_params.get('q', '')
        if query:
            from apps.tenants.models import Tenant
            tenant = Tenant.objects.get(id=request.user.tenant_id)
            clients = Client.objects.filter(
                Q(nombre__icontains=query) | 
                Q(email__icontains=query) |
                Q(contacto__icontains=query) |
                Q(ie__icontains=query),
                tenant=tenant
            )[:20]
            serializer = ClientSerializer(clients, many=True)
            return Response(serializer.data)
        return Response([])


class SchoolListView(APIView):
    """
    Lista de colegios (clientes tipo empresa).
    
    Permisos:
    - Administradores y empleados: Acceso completo
    - Usuarios regulares: Solo lectura
    """
    permission_classes = [CanManageClients]
    
    def get(self, request):
        from apps.tenants.models import Tenant
        tenant = Tenant.objects.get(id=request.user.tenant_id)
        schools = Client.objects.filter(tipo='colegio', tenant=tenant)
        serializer = ClientSerializer(schools, many=True)
        return Response(serializer.data)
