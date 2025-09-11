from django.contrib import admin
from .models import Inventario


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_type', 'item_id', 'stock_actual', 'stock_minimo', 'ubicacion', 'created_at')
    list_filter = ('item_type', 'created_at')
    search_fields = ('item_type', 'item_id', 'ubicacion')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'tenant_id', 'item_type', 'item_id')
        }),
        ('Stock', {
            'fields': ('stock_actual', 'stock_minimo')
        }),
        ('Ubicación', {
            'fields': ('ubicacion',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
