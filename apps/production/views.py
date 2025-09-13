"""
Vistas para la app de producción.
"""

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import timedelta

from .models import Cuadro, OrdenProduccion, DetalleOrden, MovimientoInventario
from .serializers import (
    CuadroSerializer, OrdenProduccionSerializer, DetalleOrdenSerializer,
    MovimientoInventarioSerializer, ProductionReportSerializer,
    WasteReportSerializer, ProductionEfficiencySerializer
)


# Views para Órdenes de Producción
class ProductionListView(generics.ListCreateAPIView):
    """Lista y creación de órdenes de producción."""
    queryset = OrdenProduccion.objects.all()
    serializer_class = OrdenProduccionSerializer
    
    def get_queryset(self):
        queryset = OrdenProduccion.objects.all()
        tenant_id = self.request.query_params.get('tenant_id')
        estado = self.request.query_params.get('estado')
        
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset


class ProductionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de órdenes de producción."""
    queryset = OrdenProduccion.objects.all()
    serializer_class = OrdenProduccionSerializer


# Views para Cuadros
class CuadroListView(generics.ListCreateAPIView):
    """Lista y creación de cuadros."""
    queryset = Cuadro.objects.all()
    serializer_class = CuadroSerializer
    
    def get_queryset(self):
        queryset = Cuadro.objects.all()
        tenant_id = self.request.query_params.get('tenant_id')
        estado = self.request.query_params.get('estado')
        orden_id = self.request.query_params.get('orden_id')
        
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        if estado:
            queryset = queryset.filter(estado=estado)
        if orden_id:
            queryset = queryset.filter(orden_id=orden_id)
        return queryset


class CuadroDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de cuadros."""
    queryset = Cuadro.objects.all()
    serializer_class = CuadroSerializer


# Views para Detalles de Orden
class DetalleOrdenListView(generics.ListCreateAPIView):
    """Lista y creación de detalles de orden."""
    queryset = DetalleOrden.objects.all()
    serializer_class = DetalleOrdenSerializer
    
    def get_queryset(self):
        queryset = DetalleOrden.objects.all()
        orden_id = self.request.query_params.get('orden_id')
        material_type = self.request.query_params.get('material_type')
        
        if orden_id:
            queryset = queryset.filter(orden_id=orden_id)
        if material_type:
            queryset = queryset.filter(material_type=material_type)
        return queryset


class DetalleOrdenDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de detalles de orden."""
    queryset = DetalleOrden.objects.all()
    serializer_class = DetalleOrdenSerializer


# Views para Movimientos de Inventario en Producción
class MovimientoInventarioListView(generics.ListCreateAPIView):
    """Lista y creación de movimientos de inventario en producción."""
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer
    
    def get_queryset(self):
        queryset = MovimientoInventario.objects.all()
        tenant_id = self.request.query_params.get('tenant_id')
        material_type = self.request.query_params.get('material_type')
        tipo_movimiento = self.request.query_params.get('tipo_movimiento')
        orden_id = self.request.query_params.get('orden_id')
        
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        if material_type:
            queryset = queryset.filter(material_type=material_type)
        if tipo_movimiento:
            queryset = queryset.filter(tipo_movimiento=tipo_movimiento)
        if orden_id:
            queryset = queryset.filter(orden_produccion_id=orden_id)
        return queryset


class MovimientoInventarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de movimientos de inventario."""
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer


# Views especiales para reportes y funcionalidades
@api_view(['POST'])
def register_production(request):
    """Registrar producción de una orden."""
    orden_id = request.data.get('orden_id')
    material_type = request.data.get('material_type')
    material_id = request.data.get('material_id')
    cantidad_usada = request.data.get('cantidad_usada')
    cantidad_merma = request.data.get('cantidad_merma', 0)
    usuario = request.data.get('usuario')
    tenant_id = request.data.get('tenant_id')
    
    if not all([orden_id, material_type, material_id, cantidad_usada]):
        return Response(
            {'error': 'Faltan parámetros requeridos: orden_id, material_type, material_id, cantidad_usada'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Establecer tenant_id por defecto si no se proporciona
    if not tenant_id:
        tenant_id = 1
    
    try:
        # Obtener la orden
        orden = OrdenProduccion.objects.get(id=orden_id, tenant_id=tenant_id)
        
        # Obtener o crear el detalle de orden
        detalle, created = DetalleOrden.objects.get_or_create(
            orden_id=orden,
            material_type=material_type,
            material_id=material_id,
            defaults={
                'cantidad_planificada': 0,
                'cantidad_usada': 0,
                'cantidad_merma': 0
            }
        )
        
        # Actualizar cantidades
        detalle.cantidad_usada += cantidad_usada
        detalle.cantidad_merma += cantidad_merma
        detalle.save()
        
        # Crear movimientos de inventario
        if cantidad_usada > 0:
            MovimientoInventario.objects.create(
                tenant_id=tenant_id,
                material_type=material_type,
                material_id=material_id,
                tipo_movimiento='uso_produccion',
                cantidad=cantidad_usada,
                motivo=f'Uso en producción - Orden {orden.numero_orden}',
                orden_produccion_id=orden,
                usuario=usuario
            )
        
        if cantidad_merma > 0:
            MovimientoInventario.objects.create(
                tenant_id=tenant_id,
                material_type=material_type,
                material_id=material_id,
                tipo_movimiento='merma',
                cantidad=cantidad_merma,
                motivo=f'Merma en producción - Orden {orden.numero_orden}',
                orden_produccion_id=orden,
                usuario=usuario
            )
        
        serializer = DetalleOrdenSerializer(detalle)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except OrdenProduccion.DoesNotExist:
        return Response(
            {'error': 'Orden de producción no encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def production_efficiency(request):
    """Obtener reporte de eficiencia de producción."""
    tenant_id = request.query_params.get('tenant_id')
    periodo = request.query_params.get('periodo', '30')  # días
    
    try:
        fecha_inicio = timezone.now() - timedelta(days=int(periodo))
        
        queryset = OrdenProduccion.objects.filter(
            tenant_id=tenant_id,
            fecha_creacion__gte=fecha_inicio,
            estado='completada'
        )
        
        eficiencia_data = []
        for orden in queryset:
            detalles = orden.detalles.all()
            total_planificado = sum(d.cantidad_planificada for d in detalles)
            total_usado = sum(d.cantidad_usada for d in detalles)
            total_merma = sum(d.cantidad_merma for d in detalles)
            
            if total_planificado > 0:
                eficiencia = ((total_usado - total_merma) / total_planificado) * 100
            else:
                eficiencia = 0
            
            eficiencia_data.append({
                'orden_id': orden.id,
                'numero_orden': orden.numero_orden,
                'fecha_creacion': orden.fecha_creacion,
                'fecha_completada': orden.updated_at.date(),
                'dias_produccion': (orden.updated_at.date() - orden.fecha_creacion).days,
                'materiales_usados': total_usado,
                'materiales_merma': total_merma,
                'eficiencia': round(eficiencia, 2)
            })
        
        serializer = ProductionEfficiencySerializer(eficiencia_data, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def waste_report(request):
    """Obtener reporte de mermas."""
    tenant_id = request.query_params.get('tenant_id')
    material_type = request.query_params.get('material_type')
    periodo = request.query_params.get('periodo', '30')  # días
    
    try:
        fecha_inicio = timezone.now() - timedelta(days=int(periodo))
        
        queryset = DetalleOrden.objects.filter(
            orden_id__tenant_id=tenant_id,
            orden_id__fecha_creacion__gte=fecha_inicio,
            cantidad_merma__gt=0
        )
        
        if material_type:
            queryset = queryset.filter(material_type=material_type)
        
        # Agrupar por material
        waste_data = {}
        for detalle in queryset:
            key = f"{detalle.material_type}_{detalle.material_id}"
            if key not in waste_data:
                waste_data[key] = {
                    'material_type': detalle.material_type,
                    'material_id': detalle.material_id,
                    'material_nombre': f"{detalle.material_type} - ID: {detalle.material_id}",
                    'cantidad_merma': 0,
                    'ordenes_afectadas': 0
                }
            
            waste_data[key]['cantidad_merma'] += detalle.cantidad_merma
            waste_data[key]['ordenes_afectadas'] += 1
        
        # Calcular porcentajes
        for key, data in waste_data.items():
            total_usado = sum(
                d.cantidad_usada for d in queryset.filter(
                    material_type=data['material_type'],
                    material_id=data['material_id']
                )
            )
            if total_usado > 0:
                data['porcentaje_merma'] = round((data['cantidad_merma'] / total_usado) * 100, 2)
            else:
                data['porcentaje_merma'] = 0
        
        serializer = WasteReportSerializer(waste_data.values(), many=True)
        return Response(serializer.data)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def production_report(request):
    """Obtener reporte general de producción."""
    tenant_id = request.query_params.get('tenant_id')
    periodo = request.query_params.get('periodo', '30')  # días
    
    try:
        fecha_inicio = timezone.now() - timedelta(days=int(periodo))
        
        queryset = OrdenProduccion.objects.filter(
            tenant_id=tenant_id,
            fecha_creacion__gte=fecha_inicio
        )
        
        total_ordenes = queryset.count()
        ordenes_completadas = queryset.filter(estado='completada').count()
        ordenes_en_proceso = queryset.filter(estado='en_proceso').count()
        ordenes_canceladas = queryset.filter(estado='cancelada').count()
        
        # Calcular eficiencia general
        if total_ordenes > 0:
            eficiencia = (ordenes_completadas / total_ordenes) * 100
        else:
            eficiencia = 0
        
        # Calcular merma total
        total_merma = DetalleOrden.objects.filter(
            orden_id__in=queryset
        ).aggregate(
            total=Sum('cantidad_merma')
        )['total'] or 0
        
        report_data = {
            'periodo': f"{periodo} días",
            'total_ordenes': total_ordenes,
            'ordenes_completadas': ordenes_completadas,
            'ordenes_en_proceso': ordenes_en_proceso,
            'ordenes_canceladas': ordenes_canceladas,
            'eficiencia': round(eficiencia, 2),
            'total_merma': total_merma
        }
        
        serializer = ProductionReportSerializer(report_data)
        return Response(serializer.data)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
