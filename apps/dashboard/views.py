"""
Vistas para la app de dashboard.
"""

from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from apps.orders.models import Pedido
from apps.clients.models import Cliente
from apps.contracts.models import Contrato
from apps.agenda.models import Agenda


class DashboardView(APIView):
    """Dashboard principal con métricas generales."""
    
    def get(self, request):
        # Métricas básicas
        total_pedidos = Pedido.objects.count()
        total_clientes = Cliente.objects.count()
        total_contratos = Contrato.objects.count()
        total_citas = Agenda.objects.count()
        
        # Pedidos por estado
        pedidos_por_estado = Pedido.objects.values('estado').annotate(
            count=Count('id')
        ).order_by('estado')
        
        # Clientes por tipo
        clientes_por_tipo = Cliente.objects.values('client_type').annotate(
            count=Count('id')
        ).order_by('client_type')
        
        # Pedidos del mes actual
        mes_actual = timezone.now().replace(day=1)
        pedidos_mes = Pedido.objects.filter(
            created_at__gte=mes_actual
        ).count()
        
        # Citas de hoy
        hoy = timezone.now().date()
        citas_hoy = Agenda.objects.filter(
            fecha_inicio__date=hoy
        ).count()
        
        data = {
            'totales': {
                'pedidos': total_pedidos,
                'clientes': total_clientes,
                'contratos': total_contratos,
                'citas': total_citas,
            },
            'pedidos_por_estado': list(pedidos_por_estado),
            'clientes_por_tipo': list(clientes_por_tipo),
            'metricas_mes': {
                'pedidos_mes_actual': pedidos_mes,
                'citas_hoy': citas_hoy,
            }
        }
        
        return Response(data)


class DashboardOrdersView(APIView):
    """Métricas específicas de pedidos."""
    
    def get(self, request):
        # Pedidos por estado
        pedidos_por_estado = Pedido.objects.values('estado').annotate(
            count=Count('id')
        ).order_by('estado')
        
        # Pedidos de los últimos 30 días
        fecha_limite = timezone.now() - timedelta(days=30)
        pedidos_recientes = Pedido.objects.filter(
            created_at__gte=fecha_limite
        ).count()
        
        # Total de ingresos (suma de totales de pedidos)
        total_ingresos = Pedido.objects.aggregate(
            total=Sum('total')
        )['total'] or 0
        
        data = {
            'pedidos_por_estado': list(pedidos_por_estado),
            'pedidos_ultimos_30_dias': pedidos_recientes,
            'total_ingresos': float(total_ingresos),
        }
        
        return Response(data)


class DashboardClientsView(APIView):
    """Métricas específicas de clientes."""
    
    def get(self, request):
        # Clientes por tipo
        clientes_por_tipo = Cliente.objects.values('client_type').annotate(
            count=Count('id')
        ).order_by('client_type')
        
        # Clientes activos (con pedidos)
        clientes_activos = Cliente.objects.filter(
            id__in=Pedido.objects.values_list('cliente_id', flat=True).distinct()
        ).count()
        
        # Nuevos clientes del mes
        mes_actual = timezone.now().replace(day=1)
        nuevos_clientes = Cliente.objects.filter(
            created_at__gte=mes_actual
        ).count()
        
        data = {
            'clientes_por_tipo': list(clientes_por_tipo),
            'clientes_activos': clientes_activos,
            'nuevos_clientes_mes': nuevos_clientes,
        }
        
        return Response(data)


class DashboardRevenueView(APIView):
    """Métricas de ingresos."""
    
    def get(self, request):
        # Total de ingresos
        total_ingresos = Pedido.objects.aggregate(
            total=Sum('total')
        )['total'] or 0
        
        # Ingresos del mes actual
        mes_actual = timezone.now().replace(day=1)
        ingresos_mes = Pedido.objects.filter(
            created_at__gte=mes_actual
        ).aggregate(total=Sum('total'))['total'] or 0
        
        # Ingresos de los últimos 7 días
        fecha_limite = timezone.now() - timedelta(days=7)
        ingresos_semana = Pedido.objects.filter(
            created_at__gte=fecha_limite
        ).aggregate(total=Sum('total'))['total'] or 0
        
        data = {
            'total_ingresos': float(total_ingresos),
            'ingresos_mes_actual': float(ingresos_mes),
            'ingresos_ultima_semana': float(ingresos_semana),
        }
        
        return Response(data)
