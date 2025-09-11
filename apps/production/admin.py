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
    list_display = ('id', 'numero_orden', 'fecha_creacion', 'solicitado_por', 'responsable_produccion', 'estado', 'created_at')
    list_filter = ('estado', 'fecha_creacion', 'created_at')
    search_fields = ('numero_orden', 'solicitado_por', 'responsable_produccion', 'estado')
    readonly_fields = ('id', 'created_at', 'updated_at', 'fecha_creacion')
    date_hierarchy = 'fecha_creacion'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_orden', 'tenant_id', 'fecha_creacion', 'fecha_entrega_estimada', 'estado')
        }),
        ('Responsables', {
            'fields': ('solicitado_por', 'responsable_produccion')
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


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'material_type', 'material_id', 'tipo_movimiento', 'cantidad', 'fecha', 'usuario')
    list_filter = ('tipo_movimiento', 'material_type', 'fecha', 'created_at')
    search_fields = ('material_type', 'material_id', 'motivo', 'usuario')
    readonly_fields = ('id', 'fecha', 'created_at')
    ordering = ('-fecha',)

# Register your models here.
