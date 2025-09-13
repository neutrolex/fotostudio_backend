"""
Vistas para la app de pedidos.
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Pedido
from .serializers import PedidoSerializer


class OrderListView(generics.ListCreateAPIView):
    """Lista y creación de pedidos."""
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de pedidos."""
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer


class OrderSearchView(APIView):
    """Búsqueda de pedidos."""
    
    def get(self, request):
        query = request.query_params.get('q', '')
        if query:
            # Intentar buscar por ID si es numérico
            try:
                query_id = int(query)
                orders = Pedido.objects.filter(
                    Q(id=query_id) | 
                    Q(cliente__name__icontains=query) |
                    Q(estado__icontains=query)
                )[:20]
            except ValueError:
                # Si no es numérico, buscar solo por texto
                orders = Pedido.objects.filter(
                    Q(cliente__name__icontains=query) |
                    Q(estado__icontains=query)
                )[:20]
            serializer = PedidoSerializer(orders, many=True)
            return Response(serializer.data)
        return Response([])


class OrderStatusView(APIView):
    """Pedidos por estado."""
    
    def get(self, request, status):
        orders = Pedido.objects.filter(estado=status)
        serializer = PedidoSerializer(orders, many=True)
        return Response(serializer.data)
