"""
Servicios para la app de inventario.
"""

from django.db.models import Q, Sum, Count, F
from django.utils import timezone
from decimal import Decimal
from typing import Dict, List, Optional, Tuple

from .models import (
    Inventario, Varilla, PinturaAcabado, MaterialImpresion, 
    MaterialRecordatorio, SoftwareEquipo, MaterialPintura, 
    MaterialDiseno, ProductoTerminado, MovimientoInventario
)


class InventoryService:
    """Servicio para gestión de inventario."""
    
    # Mapeo de modelos por tipo
    MODELS_MAP = {
        'varilla': Varilla,
        'pintura_acabado': PinturaAcabado,
        'material_impresion': MaterialImpresion,
        'material_recordatorio': MaterialRecordatorio,
        'software_equipo': SoftwareEquipo,
        'material_pintura': MaterialPintura,
        'material_diseno': MaterialDiseno,
        'producto_terminado': ProductoTerminado,
    }
    
    @classmethod
    def get_model_by_type(cls, item_type: str):
        """Obtener modelo por tipo de item."""
        return cls.MODELS_MAP.get(item_type)
    
    @classmethod
    def create_movement(cls, tenant_id: int, item_type: str, item_id: int, 
                       tipo_movimiento: str, cantidad: int, motivo: str = None,
                       orden_produccion_id: int = None, usuario: str = None) -> MovimientoInventario:
        """Crear movimiento de inventario."""
        return MovimientoInventario.objects.create(
            tenant_id=tenant_id,
            item_type=item_type,
            item_id=item_id,
            tipo_movimiento=tipo_movimiento,
            cantidad=cantidad,
            motivo=motivo,
            orden_produccion_id_id=orden_produccion_id,
            usuario=usuario
        )
    
    @classmethod
    def adjust_stock(cls, tenant_id: int, item_type: str, item_id: int, 
                    cantidad: int, motivo: str = 'Ajuste manual', usuario: str = None) -> Tuple[bool, str]:
        """Ajustar stock de un material."""
        try:
            model = cls.get_model_by_type(item_type)
            if not model:
                return False, f"Tipo de material no válido: {item_type}"
            
            item = model.objects.get(id=item_id, tenant_id=tenant_id)
            
            # Crear movimiento
            cls.create_movement(
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
            
            return True, "Stock ajustado correctamente"
            
        except model.DoesNotExist:
            return False, "Material no encontrado"
        except Exception as e:
            return False, f"Error al ajustar stock: {str(e)}"
    
    @classmethod
    def get_low_stock_items(cls, tenant_id: int) -> List[Dict]:
        """Obtener items con stock bajo."""
        alerts = []
        
        for item_type, model in cls.MODELS_MAP.items():
            if item_type == 'producto_terminado':
                continue  # Los productos terminados no tienen stock mínimo
                
            if item_type == 'varilla':
                queryset = model.objects.filter(
                    tenant_id=tenant_id,
                    stock__lte=F('minimo')
                )
            else:
                queryset = model.objects.filter(
                    tenant_id=tenant_id,
                    stock_actual__lte=F('stock_minimo')
                )
            
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
        
        return alerts
    
    @classmethod
    def get_stock_report(cls, tenant_id: int) -> List[Dict]:
        """Obtener reporte de stock por categoría."""
        reports = []
        
        category_names = {
            'varilla': 'Varillas',
            'pintura_acabado': 'Pinturas y Acabados',
            'material_impresion': 'Materiales de Impresión',
            'material_recordatorio': 'Materiales de Recordatorio',
            'software_equipo': 'Software y Equipos',
            'material_pintura': 'Materiales de Pintura',
            'material_diseno': 'Materiales de Diseño',
        }
        
        for item_type, model in cls.MODELS_MAP.items():
            if item_type == 'producto_terminado':
                continue
                
            queryset = model.objects.filter(tenant_id=tenant_id)
            
            total_items = queryset.count()
            
            if item_type == 'varilla':
                items_stock_bajo = queryset.filter(stock__lte=F('minimo')).count()
                valor_total = sum(item.stock * item.precio for item in queryset)
            else:
                items_stock_bajo = queryset.filter(stock_actual__lte=F('stock_minimo')).count()
                valor_total = sum(item.stock_actual * item.precio_unitario for item in queryset)
            
            porcentaje_stock_bajo = (items_stock_bajo / total_items * 100) if total_items > 0 else 0
            
            reports.append({
                'categoria': category_names[item_type],
                'total_items': total_items,
                'items_stock_bajo': items_stock_bajo,
                'valor_total': valor_total,
                'porcentaje_stock_bajo': round(porcentaje_stock_bajo, 2)
            })
        
        return reports
    
    @classmethod
    def get_movements_history(cls, tenant_id: int, item_type: str = None, 
                             item_id: int = None, days: int = 30) -> List[MovimientoInventario]:
        """Obtener historial de movimientos."""
        fecha_inicio = timezone.now() - timezone.timedelta(days=days)
        
        queryset = MovimientoInventario.objects.filter(
            tenant_id=tenant_id,
            fecha__gte=fecha_inicio
        )
        
        if item_type:
            queryset = queryset.filter(item_type=item_type)
        if item_id:
            queryset = queryset.filter(item_id=item_id)
        
        return queryset.order_by('-fecha')
    
    @classmethod
    def validate_stock_availability(cls, tenant_id: int, item_type: str, 
                                   item_id: int, cantidad_requerida: int) -> Tuple[bool, str]:
        """Validar disponibilidad de stock."""
        try:
            model = cls.get_model_by_type(item_type)
            if not model:
                return False, f"Tipo de material no válido: {item_type}"
            
            item = model.objects.get(id=item_id, tenant_id=tenant_id)
            
            if item_type == 'varilla':
                stock_disponible = item.stock
            else:
                stock_disponible = item.stock_actual
            
            if stock_disponible >= cantidad_requerida:
                return True, "Stock disponible"
            else:
                return False, f"Stock insuficiente. Disponible: {stock_disponible}, Requerido: {cantidad_requerida}"
                
        except model.DoesNotExist:
            return False, "Material no encontrado"
        except Exception as e:
            return False, f"Error al validar stock: {str(e)}"
    
    @classmethod
    def consume_materials(cls, tenant_id: int, materiales: List[Dict], 
                         orden_produccion_id: int = None, usuario: str = None) -> Tuple[bool, str]:
        """Consumir materiales para producción."""
        try:
            for material in materiales:
                item_type = material['item_type']
                item_id = material['item_id']
                cantidad = material['cantidad']
                
                # Validar disponibilidad
                disponible, mensaje = cls.validate_stock_availability(
                    tenant_id, item_type, item_id, cantidad
                )
                if not disponible:
                    return False, mensaje
            
            # Si todos los materiales están disponibles, consumirlos
            for material in materiales:
                item_type = material['item_type']
                item_id = material['item_id']
                cantidad = material['cantidad']
                
                model = cls.get_model_by_type(item_type)
                item = model.objects.get(id=item_id, tenant_id=tenant_id)
                
                # Crear movimiento de salida
                cls.create_movement(
                    tenant_id=tenant_id,
                    item_type=item_type,
                    item_id=item_id,
                    tipo_movimiento='salida',
                    cantidad=cantidad,
                    motivo=f'Uso en producción - Orden {orden_produccion_id}',
                    orden_produccion_id=orden_produccion_id,
                    usuario=usuario
                )
                
                # Actualizar stock
                if item_type == 'varilla':
                    item.stock -= cantidad
                else:
                    item.stock_actual -= cantidad
                item.save()
            
            return True, "Materiales consumidos correctamente"
            
        except Exception as e:
            return False, f"Error al consumir materiales: {str(e)}"
    
    @classmethod
    def add_materials(cls, tenant_id: int, materiales: List[Dict], 
                     usuario: str = None, motivo: str = 'Entrada de materiales') -> Tuple[bool, str]:
        """Agregar materiales al inventario."""
        try:
            for material in materiales:
                item_type = material['item_type']
                item_id = material.get('item_id')
                cantidad = material['cantidad']
                
                if item_id:
                    # Actualizar material existente
                    model = cls.get_model_by_type(item_type)
                    if model:
                        item = model.objects.get(id=item_id, tenant_id=tenant_id)
                        if item_type == 'varilla':
                            item.stock += cantidad
                        else:
                            item.stock_actual += cantidad
                        item.save()
                        
                        # Crear movimiento de entrada
                        cls.create_movement(
                            tenant_id=tenant_id,
                            item_type=item_type,
                            item_id=item_id,
                            tipo_movimiento='entrada',
                            cantidad=cantidad,
                            motivo=motivo,
                            usuario=usuario
                        )
            
            return True, "Materiales agregados correctamente"
            
        except Exception as e:
            return False, f"Error al agregar materiales: {str(e)}"


class StockAlertService:
    """Servicio para alertas de stock."""
    
    @staticmethod
    def check_expiring_materials(tenant_id: int, days_ahead: int = 30) -> List[Dict]:
        """Verificar materiales próximos a vencer."""
        fecha_vencimiento = timezone.now().date() + timezone.timedelta(days=days_ahead)
        
        alerts = []
        
        # Verificar MaterialImpresion
        materiales_vencimiento = MaterialImpresion.objects.filter(
            tenant_id=tenant_id,
            fecha_vencimiento__lte=fecha_vencimiento,
            fecha_vencimiento__isnull=False
        )
        
        for material in materiales_vencimiento:
            alerts.append({
                'item_type': 'material_impresion',
                'item_id': material.id,
                'nombre': material.nombre,
                'fecha_vencimiento': material.fecha_vencimiento,
                'dias_restantes': (material.fecha_vencimiento - timezone.now().date()).days,
                'tipo_alerta': 'vencimiento'
            })
        
        # Verificar SoftwareEquipo con licencias
        licencias_vencimiento = SoftwareEquipo.objects.filter(
            tenant_id=tenant_id,
            fecha_vencimiento_licencia__lte=fecha_vencimiento,
            fecha_vencimiento_licencia__isnull=False
        )
        
        for equipo in licencias_vencimiento:
            alerts.append({
                'item_type': 'software_equipo',
                'item_id': equipo.id,
                'nombre': equipo.nombre,
                'fecha_vencimiento': equipo.fecha_vencimiento_licencia,
                'dias_restantes': (equipo.fecha_vencimiento_licencia - timezone.now().date()).days,
                'tipo_alerta': 'licencia'
            })
        
        return alerts
    
    @staticmethod
    def check_inactive_materials(tenant_id: int, days_inactive: int = 90) -> List[Dict]:
        """Verificar materiales sin movimiento."""
        fecha_limite = timezone.now() - timezone.timedelta(days=days_inactive)
        
        alerts = []
        
        for item_type, model in InventoryService.MODELS_MAP.items():
            if item_type == 'producto_terminado':
                continue
                
            # Obtener materiales sin movimientos recientes
            materiales_activos = MovimientoInventario.objects.filter(
                tenant_id=tenant_id,
                item_type=item_type,
                fecha__gte=fecha_limite
            ).values_list('item_id', flat=True).distinct()
            
            materiales_inactivos = model.objects.filter(
                tenant_id=tenant_id
            ).exclude(id__in=materiales_activos)
            
            for material in materiales_inactivos:
                alerts.append({
                    'item_type': item_type,
                    'item_id': material.id,
                    'nombre': getattr(material, 'nombre', f'{item_type} {material.id}'),
                    'stock_actual': material.stock_actual,
                    'dias_inactivo': days_inactive,
                    'tipo_alerta': 'inactivo'
                })
        
        return alerts
