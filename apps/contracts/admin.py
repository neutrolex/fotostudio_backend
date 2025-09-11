from django.contrib import admin
from .models import Contrato


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_id', 'fecha_inicio', 'fecha_fin', 'estado', 'created_at')
    list_filter = ('estado', 'fecha_inicio', 'fecha_fin', 'created_at')
    search_fields = ('id', 'cliente_id', 'estado', 'descripcion')
    readonly_fields = ('id', 'created_at', 'updated_at')
    date_hierarchy = 'fecha_inicio'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'tenant_id', 'cliente_id', 'estado')
        }),
        ('Fechas del Contrato', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Detalles del Contrato', {
            'fields': ('descripcion', 'monto_total')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
