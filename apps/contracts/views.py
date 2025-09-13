"""
Vistas para la app de contratos.
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Contrato
from .serializers import ContratoSerializer


class ContractListView(generics.ListCreateAPIView):
    """Lista y creación de contratos."""
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer


class ContractDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de contratos."""
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer


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
