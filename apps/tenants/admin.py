from django.contrib import admin
from .models import Tenant


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subdomain', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'subdomain', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'name', 'subdomain', 'status')
        }),
        ('Configuración', {
            'fields': ('description', 'settings')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
