"""
Vistas para la app de producción.
"""

from rest_framework import generics
from .models import Cuadro, OrdenProduccion
from .serializers import CuadroSerializer, OrdenProduccionSerializer


class ProductionListView(generics.ListCreateAPIView):
    """Lista y creación de órdenes de producción."""
    queryset = OrdenProduccion.objects.all()
    serializer_class = OrdenProduccionSerializer


class ProductionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de órdenes de producción."""
    queryset = OrdenProduccion.objects.all()
    serializer_class = OrdenProduccionSerializer
