"""
Vistas para el sistema de reportes.
"""

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Sum, Q, F, Avg
from django.utils import timezone
from datetime import timedelta, datetime
import json
import csv
from io import StringIO, BytesIO

from .models import Report, ReportTemplate, ExportLog
from .serializers import (
    ReportSerializer, ReportCreateSerializer, ReportTemplateSerializer,
    ExportLogSerializer, ReportGenerationSerializer, ReportFilterSerializer
)

# Importar modelos de otras apps
from apps.orders.models import Pedido, DetallePedido
from apps.clients.models import Cliente
from apps.contracts.models import Contrato
from apps.agenda.models import Agenda
from apps.inventory.models import (
    Varilla, PinturaAcabado, MaterialImpresion, MaterialRecordatorio,
    SoftwareEquipo, MaterialPintura, MaterialDiseno, ProductoTerminado
)
from apps.production.models import OrdenProduccion, DetalleOrden, Cuadro


class ReportListView(generics.ListCreateAPIView):
    """Lista y creación de reportes."""
    
    def get_queryset(self):
        tenant_id = self.request.user.tenant_id
        return Report.objects.filter(tenant_id=tenant_id)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReportCreateSerializer
        return ReportSerializer


class ReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle, actualización y eliminación de reportes."""
    
    def get_queryset(self):
        tenant_id = self.request.user.tenant_id
        return Report.objects.filter(tenant_id=tenant_id)
    
    serializer_class = ReportSerializer


class ReportGenerateView(APIView):
    """Generar reporte personalizado."""
    
    def post(self, request):
        serializer = ReportGenerationSerializer(data=request.data)
        if serializer.is_valid():
            # Crear reporte
            report_data = serializer.validated_data.copy()
            report_data['tenant_id'] = request.user.tenant_id
            report_data['created_by'] = request.user.username
            report_data['name'] = f"Reporte {report_data['report_type']} - {timezone.now().strftime('%Y-%m-%d %H:%M')}"
            
            report = Report.objects.create(**report_data)
            
            # Generar datos del reporte
            report_data_generated = self.generate_report_data(report)
            
            # Actualizar reporte con datos generados
            report.status = 'completed'
            report.generated_at = timezone.now()
            report.save()
            
            return Response({
                'report': ReportSerializer(report).data,
                'data': report_data_generated
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def generate_report_data(self, report):
        """Generar datos del reporte según el tipo."""
        tenant_id = report.tenant_id
        date_from = report.date_from
        date_to = report.date_to
        
        if report.report_type == 'financial':
            return self.generate_financial_report(tenant_id, date_from, date_to)
        elif report.report_type == 'inventory':
            return self.generate_inventory_report(tenant_id, date_from, date_to)
        elif report.report_type == 'production':
            return self.generate_production_report(tenant_id, date_from, date_to)
        elif report.report_type == 'clients':
            return self.generate_clients_report(tenant_id, date_from, date_to)
        elif report.report_type == 'orders':
            return self.generate_orders_report(tenant_id, date_from, date_to)
        else:
            return {'error': 'Tipo de reporte no soportado'}
    
    def generate_financial_report(self, tenant_id, date_from, date_to):
        """Generar reporte financiero."""
        try:
            pedidos_query = Pedido.objects.filter(tenant_id=tenant_id)
            if date_from:
                pedidos_query = pedidos_query.filter(fecha_pedido__gte=date_from)
            if date_to:
                pedidos_query = pedidos_query.filter(fecha_pedido__lte=date_to)
            
            total_ingresos = pedidos_query.aggregate(total=Sum('total'))['total'] or 0
            total_pedidos = pedidos_query.count()
            pedidos_por_estado = pedidos_query.values('estado').annotate(
                count=Count('id'),
                total=Sum('total')
            )
            
            return {
                'summary': {
                    'total_ingresos': float(total_ingresos),
                    'total_pedidos': total_pedidos,
                    'promedio_pedido': float(total_ingresos / total_pedidos) if total_pedidos > 0 else 0
                },
                'pedidos_por_estado': list(pedidos_por_estado)
            }
        except Exception as e:
            return {
                'summary': {
                    'total_ingresos': 0.0,
                    'total_pedidos': 0,
                    'promedio_pedido': 0.0
                },
                'pedidos_por_estado': [],
                'error': str(e)
            }
    
    def generate_inventory_report(self, tenant_id, date_from, date_to):
        """Generar reporte de inventario."""
        try:
            categorias = {
                'varillas': Varilla.objects.filter(tenant_id=tenant_id),
                'pinturas': PinturaAcabado.objects.filter(tenant_id=tenant_id),
                'impresion': MaterialImpresion.objects.filter(tenant_id=tenant_id),
            }
            
            reporte_categorias = []
            total_valor = 0
            total_items = 0
            items_stock_bajo = 0
            
            for categoria, queryset in categorias.items():
                count = queryset.count()
                stock_bajo = queryset.filter(stock__lte=F('minimo')).count()
                valor_categoria = sum(item.stock * item.precio for item in queryset)
                
                reporte_categorias.append({
                    'categoria': categoria,
                    'total_items': count,
                    'items_stock_bajo': stock_bajo,
                    'valor_total': float(valor_categoria)
                })
                
                total_valor += valor_categoria
                total_items += count
                items_stock_bajo += stock_bajo
            
            return {
                'summary': {
                    'total_categorias': len(categorias),
                    'total_items': total_items,
                    'items_stock_bajo': items_stock_bajo,
                    'valor_total_inventario': float(total_valor)
                },
                'categorias': reporte_categorias
            }
        except Exception as e:
            return {
                'summary': {
                    'total_categorias': 0,
                    'total_items': 0,
                    'items_stock_bajo': 0,
                    'valor_total_inventario': 0.0
                },
                'categorias': [],
                'error': str(e)
            }
    
    def generate_production_report(self, tenant_id, date_from, date_to):
        """Generar reporte de producción."""
        try:
            ordenes_query = OrdenProduccion.objects.filter(tenant_id=tenant_id)
            if date_from:
                ordenes_query = ordenes_query.filter(fecha_creacion__gte=date_from)
            if date_to:
                ordenes_query = ordenes_query.filter(fecha_creacion__lte=date_to)
            
            total_ordenes = ordenes_query.count()
            ordenes_por_estado = ordenes_query.values('estado').annotate(count=Count('id'))
            
            return {
                'summary': {
                    'total_ordenes': total_ordenes,
                    'ordenes_por_estado': list(ordenes_por_estado)
                }
            }
        except Exception as e:
            return {
                'summary': {
                    'total_ordenes': 0,
                    'ordenes_por_estado': []
                },
                'error': str(e)
            }
    
    def generate_clients_report(self, tenant_id, date_from, date_to):
        """Generar reporte de clientes."""
        try:
            clientes_query = Cliente.objects.filter(tenant_id=tenant_id)
            if date_from:
                clientes_query = clientes_query.filter(created_at__gte=date_from)
            if date_to:
                clientes_query = clientes_query.filter(created_at__lte=date_to)
            
            total_clientes = clientes_query.count()
            clientes_por_tipo = clientes_query.values('tipo').annotate(count=Count('id'))
            
            return {
                'summary': {
                    'total_clientes': total_clientes,
                    'clientes_por_tipo': list(clientes_por_tipo)
                }
            }
        except Exception as e:
            return {
                'summary': {
                    'total_clientes': 0,
                    'clientes_por_tipo': []
                },
                'error': str(e)
            }
    
    def generate_orders_report(self, tenant_id, date_from, date_to):
        """Generar reporte de pedidos."""
        try:
            pedidos_query = Pedido.objects.filter(tenant_id=tenant_id)
            if date_from:
                pedidos_query = pedidos_query.filter(fecha_pedido__gte=date_from)
            if date_to:
                pedidos_query = pedidos_query.filter(fecha_pedido__lte=date_to)
            
            total_pedidos = pedidos_query.count()
            pedidos_por_estado = pedidos_query.values('estado').annotate(count=Count('id'))
            
            return {
                'summary': {
                    'total_pedidos': total_pedidos,
                    'pedidos_por_estado': list(pedidos_por_estado)
                }
            }
        except Exception as e:
            return {
                'summary': {
                    'total_pedidos': 0,
                    'pedidos_por_estado': []
                },
                'error': str(e)
            }


class ReportExportCSVView(APIView):
    """Exportar un reporte en CSV simple."""

    def get(self, request, pk):
        try:
            report = Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            return Response({'error': 'Reporte no encontrado'}, status=404)

        # Generar datos nuevamente para exportación (en un caso real, se almacenaría)
        generator = ReportGenerateView()
        data = generator.generate_report_data(report)

        # Convertir dict a CSV plano (solo summary si existe)
        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)

        if isinstance(data, dict) and 'summary' in data and data['summary']:
            writer.writerow(['key', 'value'])
            for k, v in data['summary'].items():
                writer.writerow([k, v])
        else:
            writer.writerow(['message'])
            writer.writerow(['No hay datos para exportar en este reporte'])

        from django.http import HttpResponse
        response = HttpResponse(csv_buffer.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="report_{pk}.csv"'
        return response


class ReportExportExcelView(APIView):
    """Exportar un reporte en Excel (XLSX) si openpyxl está disponible."""

    def get(self, request, pk):
        try:
            from openpyxl import Workbook
        except Exception:
            return Response({'error': 'openpyxl no instalado'}, status=501)

        try:
            report = Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            return Response({'error': 'Reporte no encontrado'}, status=404)

        generator = ReportGenerateView()
        data = generator.generate_report_data(report)

        wb = Workbook()
        ws = wb.active
        ws.title = 'Resumen'
        if isinstance(data, dict) and 'summary' in data and data['summary']:
            ws.append(['key', 'value'])
            for k, v in data['summary'].items():
                ws.append([k, v])
        else:
            ws.append(['message'])
            ws.append(['No hay datos para exportar en este reporte'])

        buf = BytesIO()
        wb.save(buf)
        buf.seek(0)

        from django.http import HttpResponse
        response = HttpResponse(buf.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="report_{pk}.xlsx"'
        return response


class ReportExportPDFView(APIView):
    """Exportar un reporte a PDF si reportlab está disponible."""

    def get(self, request, pk):
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
        except Exception:
            return Response({'error': 'reportlab no instalado'}, status=501)

        try:
            report = Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            return Response({'error': 'Reporte no encontrado'}, status=404)

        generator = ReportGenerateView()
        data = generator.generate_report_data(report)

        buf = BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        width, height = A4
        y = height - 50
        c.setFont('Helvetica-Bold', 14)
        c.drawString(50, y, f'Reporte {report.id} - {report.get_report_type_display()}')
        y -= 30
        c.setFont('Helvetica', 11)
        if isinstance(data, dict) and 'summary' in data:
            for k, v in data['summary'].items():
                c.drawString(50, y, f'{k}: {v}')
                y -= 18
                if y < 50:
                    c.showPage()
                    y = height - 50
        else:
            c.drawString(50, y, 'No hay datos para exportar en este reporte')
        c.showPage()
        c.save()
        pdf_bytes = buf.getvalue()
        buf.close()

        from django.http import HttpResponse
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{pk}.pdf"'
        return response
    
    def generate_report_data(self, report):
        """Generar datos del reporte según el tipo."""
        tenant_id = report.tenant_id
        date_from = report.date_from
        date_to = report.date_to
        
        if report.report_type == 'financial':
            return self.generate_financial_report(tenant_id, date_from, date_to)
        elif report.report_type == 'inventory':
            return self.generate_inventory_report(tenant_id, date_from, date_to)
        elif report.report_type == 'production':
            return self.generate_production_report(tenant_id, date_from, date_to)
        elif report.report_type == 'clients':
            return self.generate_clients_report(tenant_id, date_from, date_to)
        elif report.report_type == 'orders':
            return self.generate_orders_report(tenant_id, date_from, date_to)
        else:
            return {'error': 'Tipo de reporte no soportado'}
    
    def generate_financial_report(self, tenant_id, date_from, date_to):
        """Generar reporte financiero."""
        try:
            pedidos_query = Pedido.objects.filter(tenant_id=tenant_id)
            if date_from:
                pedidos_query = pedidos_query.filter(fecha_pedido__gte=date_from)
            if date_to:
                pedidos_query = pedidos_query.filter(fecha_pedido__lte=date_to)
            
            total_ingresos = pedidos_query.aggregate(total=Sum('total'))['total'] or 0
            total_pedidos = pedidos_query.count()
            pedidos_por_estado = pedidos_query.values('estado').annotate(
                count=Count('id'),
                total=Sum('total')
            )
            
            return {
                'summary': {
                    'total_ingresos': float(total_ingresos),
                    'total_pedidos': total_pedidos,
                    'promedio_pedido': float(total_ingresos / total_pedidos) if total_pedidos > 0 else 0
                },
                'pedidos_por_estado': list(pedidos_por_estado)
            }
        except Exception as e:
            # Si hay error, devolver datos de ejemplo
            return {
                'summary': {
                    'total_ingresos': 0.0,
                    'total_pedidos': 0,
                    'promedio_pedido': 0.0
                },
                'pedidos_por_estado': [],
                'error': str(e)
            }
    
    def generate_inventory_report(self, tenant_id, date_from, date_to):
        """Generar reporte de inventario."""
        try:
            categorias = {
                'varillas': Varilla.objects.filter(tenant_id=tenant_id),
                'pinturas': PinturaAcabado.objects.filter(tenant_id=tenant_id),
                'impresion': MaterialImpresion.objects.filter(tenant_id=tenant_id),
            }
            
            reporte_categorias = []
            total_valor = 0
            total_items = 0
            items_stock_bajo = 0
            
            for categoria, queryset in categorias.items():
                count = queryset.count()
                stock_bajo = queryset.filter(stock__lte=F('minimo')).count()
                valor_categoria = sum(item.stock * item.precio for item in queryset)
                
                reporte_categorias.append({
                    'categoria': categoria,
                    'total_items': count,
                    'items_stock_bajo': stock_bajo,
                    'valor_total': float(valor_categoria)
                })
                
                total_valor += valor_categoria
                total_items += count
                items_stock_bajo += stock_bajo
            
            return {
                'summary': {
                    'total_categorias': len(categorias),
                    'total_items': total_items,
                    'items_stock_bajo': items_stock_bajo,
                    'valor_total_inventario': float(total_valor)
                },
                'categorias': reporte_categorias
            }
        except Exception as e:
            return {
                'summary': {
                    'total_categorias': 0,
                    'total_items': 0,
                    'items_stock_bajo': 0,
                    'valor_total_inventario': 0.0
                },
                'categorias': [],
                'error': str(e)
            }
    
    def generate_production_report(self, tenant_id, date_from, date_to):
        """Generar reporte de producción."""
        ordenes_query = OrdenProduccion.objects.filter(tenant_id=tenant_id)
        if date_from:
            ordenes_query = ordenes_query.filter(fecha_creacion__gte=date_from)
        if date_to:
            ordenes_query = ordenes_query.filter(fecha_creacion__lte=date_to)
        
        total_ordenes = ordenes_query.count()
        ordenes_por_estado = ordenes_query.values('estado').annotate(count=Count('id'))
        
        return {
            'summary': {
                'total_ordenes': total_ordenes
            },
            'ordenes_por_estado': list(ordenes_por_estado)
        }
    
    def generate_clients_report(self, tenant_id, date_from, date_to):
        """Generar reporte de clientes."""
        clientes_query = Cliente.objects.filter(tenant_id=tenant_id)
        total_clientes = clientes_query.count()
        clientes_por_tipo = clientes_query.values('client_type').annotate(count=Count('id'))
        
        return {
            'summary': {
                'total_clientes': total_clientes
            },
            'clientes_por_tipo': list(clientes_por_tipo)
        }
    
    def generate_orders_report(self, tenant_id, date_from, date_to):
        """Generar reporte de pedidos."""
        pedidos_query = Pedido.objects.filter(tenant_id=tenant_id)
        if date_from:
            pedidos_query = pedidos_query.filter(fecha_pedido__gte=date_from)
        if date_to:
            pedidos_query = pedidos_query.filter(fecha_pedido__lte=date_to)
        
        total_pedidos = pedidos_query.count()
        pedidos_por_estado = pedidos_query.values('estado').annotate(
            count=Count('id'),
            total=Sum('total')
        )
        
        return {
            'summary': {
                'total_pedidos': total_pedidos
            },
            'pedidos_por_estado': list(pedidos_por_estado)
        }


@api_view(['GET'])
def report_categories(request):
    """Obtener categorías de reportes disponibles."""
    categories = [
        {'value': 'financial', 'label': 'Reporte Financiero', 'description': 'Análisis de ingresos y costos'},
        {'value': 'inventory', 'label': 'Reporte de Inventario', 'description': 'Estado del stock y materiales'},
        {'value': 'production', 'label': 'Reporte de Producción', 'description': 'Eficiencia y mermas de producción'},
        {'value': 'clients', 'label': 'Reporte de Clientes', 'description': 'Análisis de clientes y comportamiento'},
        {'value': 'orders', 'label': 'Reporte de Pedidos', 'description': 'Estado y tendencias de pedidos'},
    ]
    return Response(categories)