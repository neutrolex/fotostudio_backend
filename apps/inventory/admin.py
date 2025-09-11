from django.contrib import admin
from .models import (
    Inventario, Varilla, PinturaAcabado, MaterialImpresion, 
    MaterialRecordatorio, SoftwareEquipo, MaterialPintura, 
    MaterialDiseno, ProductoTerminado, MovimientoInventario
)


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_type', 'item_id', 'stock_actual', 'stock_minimo', 'ubicacion', 'created_at')
    list_filter = ('item_type', 'created_at')
    search_fields = ('item_type', 'item_id', 'ubicacion')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(Varilla)
class VarillaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'longitud', 'tipo', 'stock', 'minimo', 'precio')
    list_filter = ('tipo', 'created_at')
    search_fields = ('nombre', 'tipo')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(PinturaAcabado)
class PinturaAcabadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo', 'color', 'stock', 'minimo', 'precio')
    list_filter = ('tipo', 'color', 'created_at')
    search_fields = ('nombre', 'tipo')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(MaterialImpresion)
class MaterialImpresionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo', 'stock', 'minimo', 'precio')
    list_filter = ('tipo', 'created_at')
    search_fields = ('nombre', 'tipo')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(MaterialRecordatorio)
class MaterialRecordatorioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo', 'stock', 'minimo', 'precio')
    list_filter = ('tipo', 'created_at')
    search_fields = ('nombre', 'tipo')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(SoftwareEquipo)
class SoftwareEquipoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo', 'version', 'stock', 'minimo', 'precio')
    list_filter = ('tipo', 'created_at')
    search_fields = ('nombre', 'tipo')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(MaterialPintura)
class MaterialPinturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo', 'color', 'stock', 'minimo', 'precio')
    list_filter = ('tipo', 'color', 'created_at')
    search_fields = ('nombre', 'tipo')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(MaterialDiseno)
class MaterialDisenoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo', 'stock', 'minimo', 'precio')
    list_filter = ('tipo', 'created_at')
    search_fields = ('nombre', 'tipo')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(ProductoTerminado)
class ProductoTerminadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'tipo', 'estado', 'precio_venta', 'ubicacion', 'created_at')
    list_filter = ('tipo', 'estado', 'created_at')
    search_fields = ('nombre', 'descripcion', 'ubicacion')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'varilla_id', 'tipo', 'cantidad', 'fecha', 'usuario')
    list_filter = ('tipo', 'fecha', 'created_at')
    search_fields = ('varilla_id', 'motivo', 'usuario')
    readonly_fields = ('id', 'fecha', 'created_at')
    ordering = ('-fecha',)
