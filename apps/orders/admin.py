from django.contrib import admin
from .models import Pedido, DetallePedido


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_id', 'fecha_pedido', 'fecha_entrega_estimada', 'estado', 'total', 'created_at')
    list_filter = ('estado', 'fecha_pedido', 'created_at')
    search_fields = ('id', 'cliente_id', 'estado')
    readonly_fields = ('id', 'created_at', 'updated_at')
    date_hierarchy = 'fecha_pedido'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'tenant_id', 'cliente_id')
        }),
        ('Fechas', {
            'fields': ('fecha_pedido', 'fecha_entrega_estimada')
        }),
        ('Estado y Total', {
            'fields': ('estado', 'total')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido_id', 'item_type', 'item_id', 'cantidad', 'precio_unitario', 'subtotal')
    list_filter = ('item_type', 'created_at')
    search_fields = ('pedido_id', 'item_type', 'item_id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
