"""
Vistas para la app de agenda.
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Agenda
from .serializers import AgendaSerializer
from apps.users.permissions import CanManageAgenda


class AppointmentListView(generics.ListCreateAPIView):
    """Lista y creación de citas."""
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
    permission_classes = [CanManageAgenda]
    
    def get_queryset(self):
        """Filtrar citas por tenant del usuario autenticado"""
        from apps.tenants.models import Tenant
        tenant = Tenant.objects.get(id=self.request.user.tenant_id)
        return Agenda.objects.filter(tenant_id=tenant.id)
    
    def perform_create(self, serializer):
        """Asignar automáticamente el tenant del usuario autenticado"""
        from apps.tenants.models import Tenant
        tenant = Tenant.objects.get(id=self.request.user.tenant_id)
        serializer.save(tenant_id=tenant.id)


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de citas."""
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
    permission_classes = [CanManageAgenda]
    
    def get_queryset(self):
        """Filtrar citas por tenant del usuario autenticado"""
        from apps.tenants.models import Tenant
        tenant = Tenant.objects.get(id=self.request.user.tenant_id)
        return Agenda.objects.filter(tenant_id=tenant.id)


class AppointmentCalendarView(APIView):
    """Citas por fecha."""
    
    def get(self, request):
        fecha = request.query_params.get('fecha')
        if fecha:
            appointments = Agenda.objects.filter(fecha_inicio__date=fecha).select_related('user')
        else:
            # Si no se especifica fecha, mostrar las próximas 7 días
            from datetime import timedelta
            from django.utils import timezone
            fecha_limite = timezone.now().date() + timedelta(days=7)
            appointments = Agenda.objects.filter(
                fecha_inicio__date__lte=fecha_limite,
                fecha_inicio__date__gte=timezone.now().date()
            ).select_related('user')
        
        serializer = AgendaSerializer(appointments, many=True)
        return Response(serializer.data)
