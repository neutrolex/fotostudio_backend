from django.contrib import admin
from .models import Agenda


@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'titulo', 'fecha_inicio', 'fecha_fin', 'estado', 'created_at')
    list_filter = ('estado', 'fecha_inicio', 'created_at')
    search_fields = ('id', 'user_id', 'titulo', 'estado', 'descripcion')
    readonly_fields = ('id', 'created_at', 'updated_at')
    date_hierarchy = 'fecha_inicio'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'tenant_id', 'user_id', 'titulo', 'estado')
        }),
        ('Horarios', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Detalles de la Cita', {
            'fields': ('descripcion',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
