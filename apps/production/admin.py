from django.contrib import admin
from .models import Cuadro, DetalleOrden, OrdenProduccion


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
    list_display = ('id', 'fecha_creacion', 'solicitado_por', 'responsable_produccion', 'estado', 'created_at')
    list_filter = ('estado', 'fecha_creacion', 'created_at')
    search_fields = ('id', 'solicitado_por', 'responsable_produccion', 'estado')
    readonly_fields = ('id', 'created_at', 'updated_at')
    date_hierarchy = 'fecha_creacion'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'tenant_id', 'fecha_creacion', 'estado')
        }),
        ('Responsables', {
            'fields': ('solicitado_por', 'responsable_produccion')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# Register your models here.
