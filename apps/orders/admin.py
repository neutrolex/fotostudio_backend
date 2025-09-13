from django.contrib import admin
from .models import Pedido, Proyecto


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'servicio', 'estado', 'fecha_actualizacion')
    list_filter = ('estado', 'servicio')
    search_fields = ('id', 'cliente', 'servicio', 'estado')
    readonly_fields = ('id', 'fecha_actualizacion')
    ordering = ('-fecha_actualizacion',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'cliente', 'servicio', 'estado')
        }),
        ('Detalles del Pedido', {
            'fields': ('fotografias', 'diseño', 'detalles')
        }),
        ('Auditoría', {
            'fields': ('fecha_actualizacion',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'cliente', 'tipo', 'estado', 'fechaInicio', 'fechaEntrega', 'presupuesto')
    list_filter = ('estado', 'tipo', 'fechaInicio')
    search_fields = ('id', 'nombre', 'cliente', 'tipo', 'estado')
    readonly_fields = ('id', 'fecha_creacion', 'fecha_actualizacion')
    date_hierarchy = 'fechaInicio'
    ordering = ('-fechaInicio',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'nombre', 'cliente', 'tipo', 'estado')
        }),
        ('Fechas', {
            'fields': ('fechaInicio', 'fechaEntrega')
        }),
        ('Información Financiera', {
            'fields': ('presupuesto',)
        }),
        ('Detalles del Proyecto', {
            'fields': ('descripcion',)
        }),
        ('Auditoría', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
