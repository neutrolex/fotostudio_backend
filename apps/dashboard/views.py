"""
Vistas para la app de dashboard.
"""

from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Sum, Q, F
from django.utils import timezone
from datetime import timedelta, datetime
from apps.orders.models import Pedido, Proyecto
from apps.clients.models import Client
from apps.contracts.models import Contrato
from apps.agenda.models import Agenda
from apps.inventory.models import Inventario


class DashboardStatsView(APIView):
    """Estadísticas del dashboard compatible con frontend."""
    
    def get(self, request):
        # Métricas básicas
        total_pedidos = Pedido.objects.count()
        total_clientes = Client.objects.count()
        total_proyectos = Proyecto.objects.count()
        total_citas = Agenda.objects.count()
        
        # Ingresos totales (suma de precios de pedidos)
        total_ingresos = Pedido.objects.aggregate(
            total=Sum('precio')
        )['total'] or 0
        
        # Nuevos clientes del mes
        mes_actual = timezone.now().replace(day=1)
        nuevos_clientes = Client.objects.filter(
            created_at__gte=mes_actual
        ).count()
        
        # Proyectos activos
        proyectos_activos = Proyecto.objects.filter(
            estado__in=['Planificación', 'En Progreso', 'Revision']
        ).count()
        
        # Pedidos pendientes
        pedidos_pendientes = Pedido.objects.filter(
            estado='Nuevo'
        ).count()
        
        data = {
            'ingresos_totales': float(total_ingresos),
            'nuevos_clientes': nuevos_clientes,
            'proyectos_activos': proyectos_activos,
            'pedidos_pendientes': pedidos_pendientes,
        }
        
        return Response(data)


class DashboardActivitiesView(APIView):
    """Actividades recientes del dashboard."""
    
    def get(self, request):
        # Últimos pedidos creados
        ultimos_pedidos = Pedido.objects.order_by('-created_at')[:5]
        pedidos_data = []
        for pedido in ultimos_pedidos:
            pedidos_data.append({
                'type': 'pedido',
                'title': 'Nuevo pedido creado',
                'description': f'{pedido.servicio} - {pedido.cliente}',
                'time': pedido.created_at.strftime('Hace %M minutos')
            })
        
        # Próximas citas
        citas_proximas = Agenda.objects.filter(
            fecha_inicio__gte=timezone.now()
        ).order_by('fecha_inicio')[:3]
        citas_data = []
        for cita in citas_proximas:
            citas_data.append({
                'type': 'cita',
                'title': 'Cita programada',
                'description': f'{cita.titulo} - {cita.client or "Sin cliente"}',
                'time': cita.fecha_inicio.strftime('%H:%M')
            })
        
        # Alertas de inventario
        inventario_bajo = Inventario.objects.filter(
            stock__lt=F('stock_minimo')
        )[:3]
        alertas_data = []
        for item in inventario_bajo:
            alertas_data.append({
                'type': 'alerta',
                'title': 'Stock bajo',
                'description': f'{item.nombre} - Solo {item.stock} unidades',
                'time': 'Hace 2 horas'
            })
        
        activities = pedidos_data + citas_data + alertas_data
        activities.sort(key=lambda x: x.get('time', ''), reverse=True)
        
        return Response(activities[:10])


class DashboardUpcomingView(APIView):
    """Eventos próximos del dashboard."""
    
    def get(self, request):
        # Próximas citas (próximos 7 días)
        fecha_limite = timezone.now() + timedelta(days=7)
        citas_proximas = Agenda.objects.filter(
            fecha_inicio__gte=timezone.now(),
            fecha_inicio__lte=fecha_limite
        ).order_by('fecha_inicio')[:5]
        
        upcoming_events = []
        for cita in citas_proximas:
            priority = 'alta' if cita.type == 'sesion' else 'media'
            upcoming_events.append({
                'title': cita.titulo,
                'client': cita.client or 'Sin cliente',
                'time': cita.fecha_inicio.strftime('%H:%M'),
                'priority': priority
            })
        
        return Response(upcoming_events)


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
        # Clients por tipo
        clientes_por_tipo = Client.objects.values('client_type').annotate(
            count=Count('id')
        ).order_by('client_type')
        
        # Clients activos (con pedidos)
        clientes_activos = Client.objects.filter(
            id__in=Pedido.objects.values_list('cliente_id', flat=True).distinct()
        ).count()
        
        # Nuevos clientes del mes
        mes_actual = timezone.now().replace(day=1)
        nuevos_clientes = Client.objects.filter(
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
