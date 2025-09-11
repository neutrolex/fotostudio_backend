"""
Vistas para la app de materiales.
"""

from rest_framework import generics
from .models import MaterialDiseno
from .serializers import MaterialDisenoSerializer


class MaterialListView(generics.ListCreateAPIView):
    """Lista y creación de materiales."""
    queryset = MaterialDiseno.objects.all()
    serializer_class = MaterialDisenoSerializer


class MaterialDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de materiales."""
    queryset = MaterialDiseno.objects.all()
    serializer_class = MaterialDisenoSerializer
