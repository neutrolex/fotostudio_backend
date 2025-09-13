from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo', 'contacto', 'email', 'ie', 'fecha_registro')
    list_filter = ('tipo', 'fecha_registro')
    search_fields = ('nombre', 'email', 'contacto', 'ie')
    readonly_fields = ('id', 'fecha_registro', 'total_pedidos', 'monto_total', 'created_at', 'updated_at')
    ordering = ('-fecha_registro',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'nombre', 'tipo', 'contacto', 'email')
        }),
        ('Información Adicional', {
            'fields': ('ie', 'direccion', 'detalles'),
            'classes': ('collapse',)
        }),
        ('Estadísticas', {
            'fields': ('total_pedidos', 'monto_total', 'ultimo_pedido'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('fecha_registro', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
