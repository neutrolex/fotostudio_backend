"""
Vistas para el sistema de métricas y KPIs.
"""

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Sum, Q, F, Avg
from django.utils import timezone
from datetime import timedelta, datetime

from .models import Metric, KPIDefinition, MetricAlert
from .serializers import MetricSerializer, KPIDefinitionSerializer, MetricAlertSerializer


class MetricsListView(APIView):
    """Lista todas las métricas disponibles."""
    
    def get(self, request):
        """Obtener lista de métricas disponibles."""
        metrics = {
            'available_endpoints': [
                '/api/metrics/dashboard/',
                '/api/metrics/available/',
                '/api/metrics/revenue/',
                '/api/metrics/orders/',
                '/api/metrics/clients/',
                '/api/metrics/inventory/',
                '/api/metrics/production/'
            ],
            'description': 'Sistema de métricas y KPIs del fotostudio',
            'total_endpoints': 7
        }
        return Response(metrics, status=status.HTTP_200_OK)

# Importar modelos de otras apps
from apps.orders.models import Pedido
from apps.clients.models import Client
from apps.inventory.models import Varilla, PinturaAcabado, MaterialImpresion
from apps.production.models import OrdenProduccion


class DashboardMetricsView(APIView):
    """Métricas principales para el dashboard."""
    
    def get(self, request):
        tenant_id = request.user.tenant_id
        
        # Métricas financieras
        financial_metrics = self.get_financial_metrics(tenant_id)
        
        # Métricas operacionales
        operational_metrics = self.get_operational_metrics(tenant_id)
        
        # Métricas de clientes
        client_metrics = self.get_client_metrics(tenant_id)
        
        # Métricas de inventario
        inventory_metrics = self.get_inventory_metrics(tenant_id)
        
        # Métricas de producción
        production_metrics = self.get_production_metrics(tenant_id)
        
        return Response({
            'financial': financial_metrics,
            'operational': operational_metrics,
            'clients': client_metrics,
            'inventory': inventory_metrics,
            'production': production_metrics,
            'generated_at': timezone.now()
        })
    
    def get_financial_metrics(self, tenant_id):
        """Obtener métricas financieras."""
        mes_actual = timezone.now().replace(day=1)
        ingresos_mes = Pedido.objects.filter(
            tenant_id=tenant_id,
            created_at__gte=mes_actual
        ).aggregate(total=Sum('total'))['total'] or 0
        
        return {
            'ingresos_mes_actual': float(ingresos_mes),
            'total_ingresos': float(Pedido.objects.filter(tenant_id=tenant_id).aggregate(total=Sum('total'))['total'] or 0)
        }
    
    def get_operational_metrics(self, tenant_id):
        """Obtener métricas operacionales."""
        mes_actual = timezone.now().replace(day=1)
        pedidos_mes = Pedido.objects.filter(
            tenant_id=tenant_id,
            created_at__gte=mes_actual
        ).count()
        
        return {
            'pedidos_mes_actual': pedidos_mes,
            'total_pedidos': Pedido.objects.filter(tenant_id=tenant_id).count()
        }
    
    def get_client_metrics(self, tenant_id):
        """Obtener métricas de clientes."""
        fecha_limite = timezone.now() - timedelta(days=30)
        clientes_activos = Client.objects.filter(
            tenant_id=tenant_id,
            id__in=Pedido.objects.filter(
                created_at__gte=fecha_limite
            ).values_list('cliente_id', flat=True).distinct()
        ).count()
        
        return {
            'clientes_activos': clientes_activos,
            'total_clientes': Client.objects.filter(tenant_id=tenant_id).count()
        }
    
    def get_inventory_metrics(self, tenant_id):
        """Obtener métricas de inventario."""
        varillas_stock_bajo = Varilla.objects.filter(
            tenant_id=tenant_id,
            stock__lte=F('minimo')
        ).count()
        
        return {
            'items_stock_bajo': varillas_stock_bajo
        }
    
    def get_production_metrics(self, tenant_id):
        """Obtener métricas de producción."""
        ordenes_proceso = OrdenProduccion.objects.filter(
            tenant_id=tenant_id,
            estado='en_proceso'
        ).count()
        
        return {
            'ordenes_en_proceso': ordenes_proceso,
            'total_ordenes': OrdenProduccion.objects.filter(tenant_id=tenant_id).count()
        }


@api_view(['GET'])
def available_metrics(request):
    """Obtener métricas disponibles."""
    metrics = [
        {'value': 'financial', 'label': 'Métricas Financieras', 'description': 'Ingresos, costos y rentabilidad'},
        {'value': 'operational', 'label': 'Métricas Operacionales', 'description': 'Eficiencia y productividad'},
        {'value': 'client', 'label': 'Métricas de Client', 'description': 'Comportamiento y satisfacción'},
        {'value': 'inventory', 'label': 'Métricas de Inventario', 'description': 'Stock y rotación'},
        {'value': 'production', 'label': 'Métricas de Producción', 'description': 'Eficiencia y mermas'},
    ]
    return Response(metrics)


class RevenueMetricsView(APIView):
    """Métricas específicas de ingresos."""

    def get(self, request):
        tenant_id = request.user.tenant_id
        fecha_limite_30 = timezone.now() - timedelta(days=30)
        diarios = Pedido.objects.filter(
            tenant_id=tenant_id,
            created_at__gte=fecha_limite_30
        ).extra(select={'date': 'DATE(created_at)'}).values('date').annotate(
            total=Sum('total'), count=Count('id')
        ).order_by('date')

        fecha_limite_365 = timezone.now() - timedelta(days=365)
        mensuales = Pedido.objects.filter(
            tenant_id=tenant_id,
            created_at__gte=fecha_limite_365
        ).extra(select={'month': 'MONTH(created_at)', 'year': 'YEAR(created_at)'}).values('year', 'month').annotate(
            total=Sum('total'), count=Count('id')
        ).order_by('year', 'month')

        return Response({'daily': list(diarios), 'monthly': list(mensuales)})


class OrdersMetricsView(APIView):
    """Métricas específicas de pedidos."""

    def get(self, request):
        tenant_id = request.user.tenant_id
        by_status = Pedido.objects.filter(tenant_id=tenant_id).values('estado').annotate(
            count=Count('id'), total=Sum('total')
        )

        fecha_limite_30 = timezone.now() - timedelta(days=30)
        diarios = Pedido.objects.filter(
            tenant_id=tenant_id,
            created_at__gte=fecha_limite_30
        ).extra(select={'date': 'DATE(created_at)'}).values('date').annotate(
            count=Count('id')
        ).order_by('date')

        fecha_limite_365 = timezone.now() - timedelta(days=365)
        mensuales = Pedido.objects.filter(
            tenant_id=tenant_id,
            created_at__gte=fecha_limite_365
        ).extra(select={'month': 'MONTH(created_at)', 'year': 'YEAR(created_at)'}).values('year', 'month').annotate(
            count=Count('id')
        ).order_by('year', 'month')

        return Response({'by_status': list(by_status), 'daily': list(diarios), 'monthly': list(mensuales)})


class ClientsMetricsView(APIView):
    """Métricas específicas de clientes."""

    def get(self, request):
        tenant_id = request.user.tenant_id
        by_type = Client.objects.filter(tenant_id=tenant_id).values('client_type').annotate(count=Count('id'))
        activos = Client.objects.filter(
            tenant_id=tenant_id,
            id__in=Pedido.objects.values_list('cliente_id', flat=True).distinct()
        ).count()
        total = Client.objects.filter(tenant_id=tenant_id).count()
        return Response({'by_type': list(by_type), 'active': activos, 'inactive': total - activos, 'total': total})


class InventoryMetricsView(APIView):
    """Métricas específicas de inventario."""

    def get(self, request):
        tenant_id = request.user.tenant_id
        varillas_bajo = Varilla.objects.filter(tenant_id=tenant_id, stock__lte=F('minimo')).count()
        pinturas_bajo = PinturaAcabado.objects.filter(tenant_id=tenant_id, stock__lte=F('minimo')).count()
        materiales_bajo = MaterialImpresion.objects.filter(tenant_id=tenant_id, stock__lte=F('minimo')).count()
        return Response({
            'low_stock': {
                'varillas': varillas_bajo,
                'pinturas': pinturas_bajo,
                'materiales_impresion': materiales_bajo
            },
            'total_low_stock': varillas_bajo + pinturas_bajo + materiales_bajo
        })


class ProductionMetricsView(APIView):
    """Métricas específicas de producción."""

    def get(self, request):
        tenant_id = request.user.tenant_id
        by_status = OrdenProduccion.objects.filter(tenant_id=tenant_id).values('estado').annotate(count=Count('id'))
        total = OrdenProduccion.objects.filter(tenant_id=tenant_id).count()
        completas = OrdenProduccion.objects.filter(tenant_id=tenant_id, estado='completada').count()
        eficiencia = (completas / total * 100) if total > 0 else 0
        return Response({'by_status': list(by_status), 'efficiency': round(eficiencia, 2), 'total': total})