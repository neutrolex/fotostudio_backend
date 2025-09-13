from django.contrib import admin
from .models import MaterialVarilla


@admin.register(MaterialVarilla)
class MaterialVarillaAdmin(admin.ModelAdmin):
    list_display = ('id', 'varilla', 'material_type', 'material_id', 'cantidad', 'created_at')
    list_filter = ('material_type', 'created_at')
    search_fields = ('varilla__nombre', 'material_type', 'material_id')
    readonly_fields = ('id', 'created_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'varilla', 'material_type', 'material_id')
        }),
        ('Cantidad', {
            'fields': ('cantidad',)
        }),
        ('Auditoría', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
