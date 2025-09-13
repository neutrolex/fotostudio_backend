from django.contrib import admin
from .models import Cuadro, DetalleOrden, OrdenProduccion, MovimientoInventario


@admin.register(Cuadro)
class CuadroAdmin(admin.ModelAdmin):
    list_display = ('id', 'orden_id', 'descripcion', 'estado', 'precio', 'fecha_creacion', 'created_at')
    list_filter = ('estado', 'fecha_creacion', 'created_at')
    search_fields = ('orden_id', 'descripcion', 'ubicacion')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(DetalleOrden)
class DetalleOrdenAdmin(admin.ModelAdmin):
    list_display = ('id', 'orden_id', 'varilla_id', 'cant_varilla_plan', 'cant_cuadros_plan', 'cant_varilla_usada', 'cant_cuadros_prod', 'merma', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('orden_id', 'varilla_id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(OrdenProduccion)
class OrdenProduccionAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_numero_orden', 'fecha_creacion', 'solicitado_por', 'responsable_produccion', 'estado', 'created_at')
    list_filter = ('estado', 'fecha_creacion', 'created_at')
    search_fields = ('id', 'solicitado_por', 'responsable_produccion', 'estado')
    readonly_fields = ('id', 'created_at', 'updated_at', 'fecha_creacion', 'get_numero_orden')
    date_hierarchy = 'fecha_creacion'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('get_numero_orden', 'tenant_id', 'fecha_creacion', 'fecha_entrega', 'estado')
        }),
        ('Responsables', {
            'fields': ('solicitado_por', 'responsable_produccion')
        }),
        ('Detalles Adicionales', {
            'fields': ('descripcion', 'fecha_inicio', 'prioridad'),
            'classes': ('collapse',)
        }),
        ('Observaciones', {
            'fields': ('observaciones',),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_numero_orden(self, obj):
        """Método para mostrar el número de orden en el admin."""
        return obj.numero_orden
    get_numero_orden.short_description = 'Número de Orden'


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'material_type', 'material_id', 'tipo_movimiento', 'cantidad', 'fecha', 'usuario')
    list_filter = ('tipo_movimiento', 'material_type', 'fecha', 'created_at')
    search_fields = ('material_type', 'material_id', 'motivo', 'usuario')
    readonly_fields = ('id', 'fecha', 'created_at')
    ordering = ('-fecha',)

# Register your models here.
