"""
Vistas para la app de pedidos.
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Pedido
from .serializers import PedidoSerializer
from apps.users.permissions import CanManageOrders


class OrderListView(generics.ListCreateAPIView):
    """
    Lista y creación de pedidos.
    
    Permisos:
    - Administradores y empleados: Acceso completo
    - Usuarios regulares: Solo lectura
    """
    serializer_class = PedidoSerializer
    permission_classes = [CanManageOrders]
    
    def get_queryset(self):
        """Filtrar pedidos por tenant del usuario autenticado"""
        from apps.tenants.models import Tenant
        tenant = Tenant.objects.get(id=self.request.user.tenant_id)
        return Pedido.objects.filter(tenant=tenant)
    
    def perform_create(self, serializer):
        """Asignar automáticamente el tenant del usuario autenticado"""
        from apps.tenants.models import Tenant
        tenant = Tenant.objects.get(id=self.request.user.tenant_id)
        serializer.save(tenant=tenant)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detalle, actualización y eliminación de pedidos.
    
    Permisos:
    - Administradores y empleados: Acceso completo
    - Usuarios regulares: Solo lectura
    """
    serializer_class = PedidoSerializer
    permission_classes = [CanManageOrders]
    
    def get_queryset(self):
        """Filtrar pedidos por tenant del usuario autenticado"""
        from apps.tenants.models import Tenant
        tenant = Tenant.objects.get(id=self.request.user.tenant_id)
        return Pedido.objects.filter(tenant=tenant)


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
                    Q(cliente__icontains=query) |
                    Q(estado__icontains=query)
                )[:20]
            except ValueError:
                # Si no es numérico, buscar solo por texto
                orders = Pedido.objects.filter(
                    Q(cliente__icontains=query) |
                    Q(estado__icontains=query)
                )[:20]
            serializer = PedidoSerializer(orders, many=True)
            return Response(serializer.data)
        return Response([])


class OrderStatusView(APIView):
    """Pedidos por estado."""
    permission_classes = [CanManageOrders]
    
    def get(self, request, status):
        from apps.tenants.models import Tenant
        tenant = Tenant.objects.get(id=request.user.tenant_id)
        orders = Pedido.objects.filter(estado=status, tenant=tenant)
        serializer = PedidoSerializer(orders, many=True)
        return Response(serializer.data)


class OrderStatusUpdateView(APIView):
    """
    Vista para actualizar el estado de un pedido específico.
    
    Permite cambiar el estado de un pedido individual,
    con validaciones de estados válidos.
    
    Características:
        - Solo usuarios autenticados
        - Validación de estados válidos
        - Actualización de fecha de modificación
        - Respuesta con datos actualizados
    
    Endpoint: PATCH /api/orders/{id}/status/
    """
    
    permission_classes = [CanManageOrders]
    
    def patch(self, request, pk):
        """
        Actualiza el estado de un pedido específico.
        
        Args:
            request: Objeto de solicitud HTTP con nuevo estado
            pk: ID del pedido a actualizar
            
        Returns:
            Response: Respuesta HTTP con datos del pedido actualizado
        """
        try:
            # Buscar el pedido
            order = Pedido.objects.get(pk=pk)
            
            # Obtener nuevo estado del request
            new_status = request.data.get('status')
            
            # Validar que el estado sea válido
            estados_validos = ['pendiente', 'en_proceso', 'entregado', 'cancelado']
            if new_status not in estados_validos:
                return Response({
                    'error': 'Estado inválido',
                    'message': f'El estado debe ser uno de: {", ".join(estados_validos)}',
                    'valid_states': estados_validos
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Actualizar el estado
            order.estado = new_status
            order.save()
            
            # Serializar y devolver respuesta
            serializer = PedidoSerializer(order)
            return Response({
                'message': 'Estado actualizado correctamente',
                'order': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Pedido.DoesNotExist:
            return Response({
                'error': 'Pedido no encontrado',
                'message': f'No existe un pedido con ID {pk}'
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({
                'error': 'Error al actualizar estado',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
