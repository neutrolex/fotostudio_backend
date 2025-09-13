"""
Vistas para la app de contratos.
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Contrato
from .serializers import ContratoSerializer
from apps.users.permissions import CanManageContracts


class ContractListView(generics.ListCreateAPIView):
    """Lista y creación de contratos."""
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer
    permission_classes = [CanManageContracts]
    
    def get_queryset(self):
        """Filtrar contratos por tenant del usuario autenticado"""
        from apps.tenants.models import Tenant
        tenant = Tenant.objects.get(id=self.request.user.tenant_id)
        return Contrato.objects.filter(tenant_id=tenant.id)
    
    def perform_create(self, serializer):
        """Asignar automáticamente el tenant del usuario autenticado"""
        from apps.tenants.models import Tenant
        tenant = Tenant.objects.get(id=self.request.user.tenant_id)
        serializer.save(tenant_id=tenant.id)


class ContractDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de contratos."""
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer
    permission_classes = [CanManageContracts]
    
    def get_queryset(self):
        """Filtrar contratos por tenant del usuario autenticado"""
        from apps.tenants.models import Tenant
        tenant = Tenant.objects.get(id=self.request.user.tenant_id)
        return Contrato.objects.filter(tenant_id=tenant.id)


class ContractExpiringView(APIView):
    """Contratos próximos a vencer."""
    
    def get(self, request):
        # Contratos que vencen en los próximos 30 días
        from datetime import timedelta
        fecha_limite = timezone.now().date() + timedelta(days=30)
        
        contracts = Contrato.objects.filter(
            fecha_fin__lte=fecha_limite,
            fecha_fin__gte=timezone.now().date()
        ).select_related('cliente')
        serializer = ContratoSerializer(contracts, many=True)
        return Response(serializer.data)
