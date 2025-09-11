"""
Vistas para la app de inventario.
"""

from rest_framework import generics
from .models import Inventario
from .serializers import InventarioSerializer


class InventoryListView(generics.ListCreateAPIView):
    """Lista y creación de inventario."""
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer


class InventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de inventario."""
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer
