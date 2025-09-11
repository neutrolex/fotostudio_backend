"""
Vistas para la app de inventario.
"""

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import F
from django.utils import timezone

from .models import (
    Inventario, Varilla, PinturaAcabado, MaterialImpresion, 
    MaterialRecordatorio, SoftwareEquipo, MaterialPintura, 
    MaterialDiseno, ProductoTerminado, MovimientoInventario
)
from .serializers import (
    InventarioSerializer, VarillaSerializer, PinturaAcabadoSerializer,
    MaterialImpresionSerializer, MaterialRecordatorioSerializer,
    SoftwareEquipoSerializer, MaterialPinturaSerializer, MaterialDisenoSerializer,
    ProductoTerminadoSerializer, MovimientoInventarioSerializer,
    StockAlertSerializer, StockReportSerializer
)


# Views para Varillas
class VarillaListView(generics.ListCreateAPIView):
    """Lista y creación de varillas."""
    queryset = Varilla.objects.all()
    serializer_class = VarillaSerializer
    
    def get_queryset(self):
        queryset = Varilla.objects.all()
        tenant_id = self.request.query_params.get('tenant_id')
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        return queryset


class VarillaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de varillas."""
    queryset = Varilla.objects.all()
    serializer_class = VarillaSerializer


# Views para Pinturas y Acabados
class PinturaAcabadoListView(generics.ListCreateAPIView):
    """Lista y creación de pinturas y acabados."""
    queryset = PinturaAcabado.objects.all()
    serializer_class = PinturaAcabadoSerializer
    
    def get_queryset(self):
        queryset = PinturaAcabado.objects.all()
        tenant_id = self.request.query_params.get('tenant_id')
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        return queryset


class PinturaAcabadoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de pinturas y acabados."""
    queryset = PinturaAcabado.objects.all()
    serializer_class = PinturaAcabadoSerializer


# Views para Materiales de Impresión
class MaterialImpresionListView(generics.ListCreateAPIView):
    """Lista y creación de materiales de impresión."""
    queryset = MaterialImpresion.objects.all()
    serializer_class = MaterialImpresionSerializer
    
    def get_queryset(self):
        queryset = MaterialImpresion.objects.all()
        tenant_id = self.request.query_params.get('tenant_id')
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        return queryset


class MaterialImpresionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de materiales de impresión."""
    queryset = MaterialImpresion.objects.all()
    serializer_class = MaterialImpresionSerializer


# Views para Materiales de Recordatorio
class MaterialRecordatorioListView(generics.ListCreateAPIView):
    """Lista y creación de materiales de recordatorio."""
    queryset = MaterialRecordatorio.objects.all()
    serializer_class = MaterialRecordatorioSerializer
    
    def get_queryset(self):
        queryset = MaterialRecordatorio.objects.all()
        tenant_id = self.request.query_params.get('tenant_id')
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        return queryset


class MaterialRecordatorioDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de materiales de recordatorio."""
    queryset = MaterialRecordatorio.objects.all()
    serializer_class = MaterialRecordatorioSerializer


# Views para Software y Equipos
class SoftwareEquipoListView(generics.ListCreateAPIView):
    """Lista y creación de software y equipos."""
    queryset = SoftwareEquipo.objects.all()
    serializer_class = SoftwareEquipoSerializer
    
    def get_queryset(self):
        queryset = SoftwareEquipo.objects.all()
        tenant_id = self.request.query_params.get('tenant_id')
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        return queryset


class SoftwareEquipoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de software y equipos."""
    queryset = SoftwareEquipo.objects.all()
    serializer_class = SoftwareEquipoSerializer


# Views para Materiales de Pintura
class MaterialPinturaListView(generics.ListCreateAPIView):
    """Lista y creación de materiales de pintura."""
    queryset = MaterialPintura.objects.all()
    serializer_class = MaterialPinturaSerializer
    
    def get_queryset(self):
        queryset = MaterialPintura.objects.all()
        tenant_id = self.request.query_params.get('tenant_id')
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        return queryset


class MaterialPinturaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de materiales de pintura."""
    queryset = MaterialPintura.objects.all()
    serializer_class = MaterialPinturaSerializer


# Views para Materiales de Diseño
class MaterialDisenoListView(generics.ListCreateAPIView):
    """Lista y creación de materiales de diseño."""
    queryset = MaterialDiseno.objects.all()
    serializer_class = MaterialDisenoSerializer
    
    def get_queryset(self):
        queryset = MaterialDiseno.objects.all()
        tenant_id = self.request.query_params.get('tenant_id')
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        return queryset


class MaterialDisenoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de materiales de diseño."""
    queryset = MaterialDiseno.objects.all()
    serializer_class = MaterialDisenoSerializer


# Views para Productos Terminados
class ProductoTerminadoListView(generics.ListCreateAPIView):
    """Lista y creación de productos terminados."""
    queryset = ProductoTerminado.objects.all()
    serializer_class = ProductoTerminadoSerializer
    
    def get_queryset(self):
        queryset = ProductoTerminado.objects.all()
        tenant_id = self.request.query_params.get('tenant_id')
        estado = self.request.query_params.get('estado')
        ubicacion = self.request.query_params.get('ubicacion')
        
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        if estado:
            queryset = queryset.filter(estado=estado)
        if ubicacion:
            queryset = queryset.filter(ubicacion__icontains=ubicacion)
        return queryset


class ProductoTerminadoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de productos terminados."""
    queryset = ProductoTerminado.objects.all()
    serializer_class = ProductoTerminadoSerializer


# Views para Movimientos de Inventario
class MovimientoInventarioListView(generics.ListCreateAPIView):
    """Lista y creación de movimientos de inventario."""
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer
    
    def get_queryset(self):
        queryset = MovimientoInventario.objects.all()
        tenant_id = self.request.query_params.get('tenant_id')
        varilla_id = self.request.query_params.get('varilla_id')
        tipo = self.request.query_params.get('tipo')
        
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        if varilla_id:
            queryset = queryset.filter(varilla_id=varilla_id)
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        return queryset


class MovimientoInventarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de movimientos de inventario."""
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer


# Views especiales para alertas y reportes
@api_view(['GET'])
def stock_alerts(request):
    """Obtener alertas de stock bajo."""
    tenant_id = request.query_params.get('tenant_id')
    alerts = []
    
    # Verificar stock bajo en todas las categorías
    models_map = {
        'varilla': Varilla,
        'pintura_acabado': PinturaAcabado,
        'material_impresion': MaterialImpresion,
        'material_recordatorio': MaterialRecordatorio,
        'software_equipo': SoftwareEquipo,
        'material_pintura': MaterialPintura,
        'material_diseno': MaterialDiseno,
    }
    
    for item_type, model in models_map.items():
        if item_type == 'varilla':
            queryset = model.objects.filter(stock__lte=F('minimo'))
        else:
            queryset = model.objects.filter(stock_actual__lte=F('stock_minimo'))
        
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        
        for item in queryset:
            if item_type == 'varilla':
                stock_actual = item.stock
                stock_minimo = item.minimo
            else:
                stock_actual = item.stock_actual
                stock_minimo = item.stock_minimo
            
            alerts.append({
                'item_type': item_type,
                'item_id': item.id,
                'nombre': getattr(item, 'nombre', f'{item_type} {item.id}'),
                'stock_actual': stock_actual,
                'stock_minimo': stock_minimo,
                'diferencia': stock_actual - stock_minimo,
                'ubicacion': getattr(item, 'ubicacion', ''),
                'fecha_alerta': timezone.now()
            })
    
    serializer = StockAlertSerializer(alerts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def stock_report(request):
    """Obtener reporte de stock por categoría."""
    tenant_id = request.query_params.get('tenant_id')
    reports = []
    
    models_map = {
        'Varillas': Varilla,
        'Pinturas y Acabados': PinturaAcabado,
        'Materiales de Impresión': MaterialImpresion,
        'Materiales de Recordatorio': MaterialRecordatorio,
        'Software y Equipos': SoftwareEquipo,
        'Materiales de Pintura': MaterialPintura,
        'Materiales de Diseño': MaterialDiseno,
    }
    
    for categoria, model in models_map.items():
        queryset = model.objects.all()
        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        
        total_items = queryset.count()
        
        if categoria == 'Varillas':
            items_stock_bajo = queryset.filter(stock__lte=F('minimo')).count()
            valor_total = sum(item.stock * item.precio for item in queryset)
        else:
            items_stock_bajo = queryset.filter(stock_actual__lte=F('stock_minimo')).count()
            valor_total = sum(item.stock_actual * item.precio_unitario for item in queryset)
        
        porcentaje_stock_bajo = (items_stock_bajo / total_items * 100) if total_items > 0 else 0
        
        reports.append({
            'categoria': categoria,
            'total_items': total_items,
            'items_stock_bajo': items_stock_bajo,
            'valor_total': valor_total,
            'porcentaje_stock_bajo': round(porcentaje_stock_bajo, 2)
        })
    
    serializer = StockReportSerializer(reports, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def adjust_stock(request):
    """Ajustar stock de un material."""
    item_type = request.data.get('item_type')
    item_id = request.data.get('item_id')
    cantidad = request.data.get('cantidad')
    motivo = request.data.get('motivo', 'Ajuste manual')
    usuario = request.data.get('usuario')
    tenant_id = request.data.get('tenant_id')
    
    if not all([item_type, item_id, cantidad, tenant_id]):
        return Response(
            {'error': 'Faltan parámetros requeridos'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Obtener el modelo correspondiente
    models_map = {
        'varilla': Varilla,
        'pintura_acabado': PinturaAcabado,
        'material_impresion': MaterialImpresion,
        'material_recordatorio': MaterialRecordatorio,
        'software_equipo': SoftwareEquipo,
        'material_pintura': MaterialPintura,
        'material_diseno': MaterialDiseno,
    }
    
    if item_type not in models_map:
        return Response(
            {'error': 'Tipo de material no válido'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        model = models_map[item_type]
        item = model.objects.get(id=item_id, tenant_id=tenant_id)
        
        # Crear movimiento
        movimiento = MovimientoInventario.objects.create(
            tenant_id=tenant_id,
            item_type=item_type,
            item_id=item_id,
            tipo_movimiento='ajuste',
            cantidad=abs(cantidad),
            motivo=motivo,
            usuario=usuario
        )
        
        # Actualizar stock
        if item_type == 'varilla':
            item.stock += cantidad
            if item.stock < 0:
                item.stock = 0
        else:
            item.stock_actual += cantidad
            if item.stock_actual < 0:
                item.stock_actual = 0
        item.save()
        
        serializer = MovimientoInventarioSerializer(movimiento)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except model.DoesNotExist:
        return Response(
            {'error': 'Material no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Views legacy para compatibilidad
class InventoryListView(generics.ListCreateAPIView):
    """Lista y creación de inventario (legacy)."""
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer


class InventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de inventario (legacy)."""
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer
