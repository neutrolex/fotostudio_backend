"""
Servicios para la app de producción.
"""

from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from typing import Dict, List, Optional, Tuple
from decimal import Decimal

from .models import OrdenProduccion, DetalleOrden, Cuadro, MovimientoInventario
from apps.inventory.services import InventoryService


class ProductionService:
    """Servicio para gestión de producción."""
    
    @staticmethod
    def create_production_order(tenant_id: int, numero_orden: str, 
                              solicitado_por: str = None, responsable_produccion: str = None,
                              fecha_entrega_estimada=None, observaciones: str = None) -> OrdenProduccion:
        """Crear nueva orden de producción."""
        return OrdenProduccion.objects.create(
            tenant_id=tenant_id,
            numero_orden=numero_orden,
            solicitado_por=solicitado_por,
            responsable_produccion=responsable_produccion,
            fecha_entrega_estimada=fecha_entrega_estimada,
            observaciones=observaciones
        )
    
    @staticmethod
    def add_material_to_order(orden_id: int, material_type: str, material_id: int,
                             cantidad_planificada: int) -> Tuple[bool, str]:
        """Agregar material a una orden de producción."""
        try:
            orden = OrdenProduccion.objects.get(id=orden_id)
            
            detalle, created = DetalleOrden.objects.get_or_create(
                orden_id=orden,
                material_type=material_type,
                material_id=material_id,
                defaults={
                    'cantidad_planificada': cantidad_planificada,
                    'cantidad_usada': 0,
                    'cantidad_merma': 0
                }
            )
            
            if not created:
                detalle.cantidad_planificada += cantidad_planificada
                detalle.save()
            
            return True, "Material agregado a la orden"
            
        except OrdenProduccion.DoesNotExist:
            return False, "Orden de producción no encontrada"
        except Exception as e:
            return False, f"Error al agregar material: {str(e)}"
    
    @staticmethod
    def register_production_usage(tenant_id: int, orden_id: int, material_type: str, 
                                material_id: int, cantidad_usada: int, cantidad_merma: int = 0,
                                usuario: str = None) -> Tuple[bool, str]:
        """Registrar uso de materiales en producción."""
        try:
            orden = OrdenProduccion.objects.get(id=orden_id, tenant_id=tenant_id)
            
            # Validar disponibilidad de stock
            disponible, mensaje = InventoryService.validate_stock_availability(
                tenant_id, material_type, material_id, cantidad_usada
            )
            if not disponible:
                return False, mensaje
            
            # Obtener o crear detalle de orden
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
                InventoryService.create_movement(
                    tenant_id=tenant_id,
                    item_type=material_type,
                    item_id=material_id,
                    tipo_movimiento='uso_produccion',
                    cantidad=cantidad_usada,
                    motivo=f'Uso en producción - Orden {orden.numero_orden}',
                    orden_produccion_id=orden_id,
                    usuario=usuario
                )
            
            if cantidad_merma > 0:
                InventoryService.create_movement(
                    tenant_id=tenant_id,
                    item_type=material_type,
                    item_id=material_id,
                    tipo_movimiento='merma',
                    cantidad=cantidad_merma,
                    motivo=f'Merma en producción - Orden {orden.numero_orden}',
                    orden_produccion_id=orden_id,
                    usuario=usuario
                )
            
            # Actualizar stock
            model = InventoryService.get_model_by_type(material_type)
            if model:
                item = model.objects.get(id=material_id, tenant_id=tenant_id)
                item.stock_actual -= cantidad_usada
                item.save()
            
            return True, "Producción registrada correctamente"
            
        except OrdenProduccion.DoesNotExist:
            return False, "Orden de producción no encontrada"
        except Exception as e:
            return False, f"Error al registrar producción: {str(e)}"
    
    @staticmethod
    def create_product(tenant_id: int, orden_id: int, nombre: str, descripcion: str = None,
                      dimensiones: str = None, precio_venta: Decimal = None,
                      ubicacion: str = None) -> Tuple[bool, str, Cuadro]:
        """Crear producto terminado (cuadro)."""
        try:
            orden = OrdenProduccion.objects.get(id=orden_id, tenant_id=tenant_id)
            
            cuadro = Cuadro.objects.create(
                tenant_id=tenant_id,
                orden_id=orden,
                nombre=nombre,
                descripcion=descripcion,
                dimensiones=dimensiones,
                precio_venta=precio_venta or Decimal('0.00'),
                ubicacion=ubicacion
            )
            
            return True, "Producto creado correctamente", cuadro
            
        except OrdenProduccion.DoesNotExist:
            return False, "Orden de producción no encontrada", None
        except Exception as e:
            return False, f"Error al crear producto: {str(e)}", None
    
    @staticmethod
    def complete_order(orden_id: int, usuario: str = None) -> Tuple[bool, str]:
        """Completar orden de producción."""
        try:
            orden = OrdenProduccion.objects.get(id=orden_id)
            
            if orden.estado == 'completada':
                return False, "La orden ya está completada"
            
            orden.estado = 'completada'
            orden.save()
            
            # Marcar todos los cuadros como terminados
            Cuadro.objects.filter(
                orden_id=orden,
                estado='en_produccion'
            ).update(
                estado='terminado',
                fecha_terminacion=timezone.now().date()
            )
            
            return True, "Orden completada correctamente"
            
        except OrdenProduccion.DoesNotExist:
            return False, "Orden de producción no encontrada"
        except Exception as e:
            return False, f"Error al completar orden: {str(e)}"
    
    @staticmethod
    def calculate_efficiency(orden_id: int) -> Dict:
        """Calcular eficiencia de una orden de producción."""
        try:
            orden = OrdenProduccion.objects.get(id=orden_id)
            detalles = orden.detalles.all()
            
            total_planificado = sum(d.cantidad_planificada for d in detalles)
            total_usado = sum(d.cantidad_usada for d in detalles)
            total_merma = sum(d.cantidad_merma for d in detalles)
            
            if total_planificado > 0:
                eficiencia = ((total_usado - total_merma) / total_planificado) * 100
            else:
                eficiencia = 0
            
            return {
                'orden_id': orden_id,
                'numero_orden': orden.numero_orden,
                'total_planificado': total_planificado,
                'total_usado': total_usado,
                'total_merma': total_merma,
                'eficiencia': round(eficiencia, 2),
                'dias_produccion': (orden.updated_at.date() - orden.fecha_creacion).days
            }
            
        except OrdenProduccion.DoesNotExist:
            return {'error': 'Orden no encontrada'}
    
    @staticmethod
    def get_production_report(tenant_id: int, periodo_dias: int = 30) -> Dict:
        """Obtener reporte de producción."""
        fecha_inicio = timezone.now() - timedelta(days=periodo_dias)
        
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
        
        # Calcular tiempo promedio de producción
        ordenes_completadas_objs = queryset.filter(estado='completada')
        if ordenes_completadas_objs.exists():
            tiempos = []
            for orden in ordenes_completadas_objs:
                tiempo = (orden.updated_at.date() - orden.fecha_creacion).days
                tiempos.append(tiempo)
            tiempo_promedio = sum(tiempos) / len(tiempos)
        else:
            tiempo_promedio = 0
        
        return {
            'periodo': f"{periodo_dias} días",
            'total_ordenes': total_ordenes,
            'ordenes_completadas': ordenes_completadas,
            'ordenes_en_proceso': ordenes_en_proceso,
            'ordenes_canceladas': ordenes_canceladas,
            'eficiencia': round(eficiencia, 2),
            'total_merma': total_merma,
            'tiempo_promedio_dias': round(tiempo_promedio, 2)
        }
    
    @staticmethod
    def get_waste_analysis(tenant_id: int, periodo_dias: int = 30) -> List[Dict]:
        """Obtener análisis de mermas por material."""
        fecha_inicio = timezone.now() - timedelta(days=periodo_dias)
        
        queryset = DetalleOrden.objects.filter(
            orden_id__tenant_id=tenant_id,
            orden_id__fecha_creacion__gte=fecha_inicio,
            cantidad_merma__gt=0
        )
        
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
                    'cantidad_usada': 0,
                    'ordenes_afectadas': 0
                }
            
            waste_data[key]['cantidad_merma'] += detalle.cantidad_merma
            waste_data[key]['cantidad_usada'] += detalle.cantidad_usada
            waste_data[key]['ordenes_afectadas'] += 1
        
        # Calcular porcentajes y agregar al resultado
        for key, data in waste_data.items():
            if data['cantidad_usada'] > 0:
                data['porcentaje_merma'] = round((data['cantidad_merma'] / data['cantidad_usada']) * 100, 2)
            else:
                data['porcentaje_merma'] = 0
        
        return list(waste_data.values())
    
    @staticmethod
    def get_material_consumption_report(tenant_id: int, periodo_dias: int = 30) -> List[Dict]:
        """Obtener reporte de consumo de materiales."""
        fecha_inicio = timezone.now() - timedelta(days=periodo_dias)
        
        movimientos = MovimientoInventario.objects.filter(
            tenant_id=tenant_id,
            fecha__gte=fecha_inicio,
            tipo_movimiento__in=['uso_produccion', 'merma']
        )
        
        consumption_data = {}
        for movimiento in movimientos:
            key = f"{movimiento.material_type}_{movimiento.material_id}"
            if key not in consumption_data:
                consumption_data[key] = {
                    'material_type': movimiento.material_type,
                    'material_id': movimiento.material_id,
                    'material_nombre': f"{movimiento.material_type} - ID: {movimiento.material_id}",
                    'cantidad_usada': 0,
                    'cantidad_merma': 0,
                    'ordenes_afectadas': set()
                }
            
            if movimiento.tipo_movimiento == 'uso_produccion':
                consumption_data[key]['cantidad_usada'] += movimiento.cantidad
            elif movimiento.tipo_movimiento == 'merma':
                consumption_data[key]['cantidad_merma'] += movimiento.cantidad
            
            if movimiento.orden_produccion_id:
                consumption_data[key]['ordenes_afectadas'].add(movimiento.orden_produccion_id.id)
        
        # Convertir sets a listas y calcular totales
        for key, data in consumption_data.items():
            data['ordenes_afectadas'] = len(data['ordenes_afectadas'])
            data['total_consumido'] = data['cantidad_usada'] + data['cantidad_merma']
            if data['total_consumido'] > 0:
                data['porcentaje_merma'] = round((data['cantidad_merma'] / data['total_consumido']) * 100, 2)
            else:
                data['porcentaje_merma'] = 0
        
        return list(consumption_data.values())


class ProductionOptimizationService:
    """Servicio para optimización de producción."""
    
    @staticmethod
    def suggest_material_requirements(orden_id: int) -> List[Dict]:
        """Sugerir requerimientos de materiales basado en historial."""
        try:
            orden = OrdenProduccion.objects.get(id=orden_id)
            
            # Obtener órdenes similares completadas
            ordenes_similares = OrdenProduccion.objects.filter(
                tenant_id=orden.tenant_id,
                estado='completada'
            ).exclude(id=orden_id)
            
            suggestions = []
            
            # Analizar patrones de uso de materiales
            for orden_similar in ordenes_similares:
                detalles = orden_similar.detalles.all()
                for detalle in detalles:
                    # Buscar si ya existe en la orden actual
                    exists = DetalleOrden.objects.filter(
                        orden_id=orden,
                        material_type=detalle.material_type,
                        material_id=detalle.material_id
                    ).exists()
                    
                    if not exists:
                        suggestions.append({
                            'material_type': detalle.material_type,
                            'material_id': detalle.material_id,
                            'cantidad_sugerida': detalle.cantidad_usada,
                            'eficiencia_historica': 1 - (detalle.cantidad_merma / max(detalle.cantidad_usada, 1))
                        })
            
            return suggestions
            
        except OrdenProduccion.DoesNotExist:
            return []
    
    @staticmethod
    def optimize_production_sequence(tenant_id: int) -> List[Dict]:
        """Optimizar secuencia de producción basada en prioridades."""
        ordenes_pendientes = OrdenProduccion.objects.filter(
            tenant_id=tenant_id,
            estado='pendiente'
        ).order_by('fecha_entrega_estimada', 'fecha_creacion')
        
        optimized_sequence = []
        
        for orden in ordenes_pendientes:
            # Calcular prioridad basada en fecha de entrega y complejidad
            dias_restantes = (orden.fecha_entrega_estimada - timezone.now().date()).days if orden.fecha_entrega_estimada else 999
            
            # Calcular complejidad basada en número de materiales
            complejidad = orden.detalles.count()
            
            # Calcular puntuación de prioridad
            prioridad = (100 - dias_restantes) + (10 - complejidad)
            
            optimized_sequence.append({
                'orden_id': orden.id,
                'numero_orden': orden.numero_orden,
                'prioridad': prioridad,
                'dias_restantes': dias_restantes,
                'complejidad': complejidad,
                'fecha_entrega': orden.fecha_entrega_estimada
            })
        
        # Ordenar por prioridad descendente
        optimized_sequence.sort(key=lambda x: x['prioridad'], reverse=True)
        
        return optimized_sequence
