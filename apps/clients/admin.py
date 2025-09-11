from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'client_type', 'company_name', 'email', 'phone', 'created_at')
    list_filter = ('client_type', 'created_at')
    search_fields = ('name', 'email', 'phone', 'company_name')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'tenant_id', 'name', 'client_type')
        }),
        ('Información de Empresa', {
            'fields': ('company_name', 'contact'),
            'classes': ('collapse',)
        }),
        ('Contacto', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Información Adicional', {
            'fields': ('additional_details',),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
