"""
Vistas para la app de materiales.
"""

from rest_framework import generics
from .models import MaterialVarilla
from .serializers import MaterialVarillaSerializer


class MaterialVarillaListView(generics.ListCreateAPIView):
    """Lista y creación de relaciones material-varilla."""
    queryset = MaterialVarilla.objects.all()
    serializer_class = MaterialVarillaSerializer


class MaterialVarillaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de relaciones material-varilla."""
    queryset = MaterialVarilla.objects.all()
    serializer_class = MaterialVarillaSerializer
