"""
Vistas para la app de clientes.
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Cliente
from .serializers import ClienteSerializer


class ClientListView(generics.ListCreateAPIView):
    """Lista y creación de clientes."""
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de clientes."""
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ClientSearchView(APIView):
    """Búsqueda de clientes."""
    
    def get(self, request):
        query = request.query_params.get('q', '')
        if query:
            clients = Cliente.objects.filter(
                Q(name__icontains=query) | 
                Q(email__icontains=query) |
                Q(phone__icontains=query) |
                Q(company_name__icontains=query)
            )[:20]
            serializer = ClienteSerializer(clients, many=True)
            return Response(serializer.data)
        return Response([])


class SchoolListView(APIView):
    """Lista de colegios (clientes tipo empresa)."""
    
    def get(self, request):
        schools = Cliente.objects.filter(client_type='empresa')
        serializer = ClienteSerializer(schools, many=True)
        return Response(serializer.data)
