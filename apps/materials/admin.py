from django.contrib import admin
from .models import MaterialDiseno


@admin.register(MaterialDiseno)
class MaterialDisenoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo', 'precio', 'stock', 'minimo', 'created_at')
    list_filter = ('tipo', 'created_at')
    search_fields = ('nombre', 'tipo', 'especificaciones')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'tenant_id', 'nombre', 'tipo')
        }),
        ('Precios y Stock', {
            'fields': ('precio', 'stock', 'minimo')
        }),
        ('Especificaciones', {
            'fields': ('especificaciones',),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
