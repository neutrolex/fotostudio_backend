"""
Admin para el sistema de reportes.
"""

from django.contrib import admin
from .models import Report, ReportTemplate, ExportLog


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['name', 'report_type', 'status', 'created_by', 'created_at']
    list_filter = ['report_type', 'status', 'export_format', 'created_at']
    search_fields = ['name', 'description', 'created_by']
    readonly_fields = ['created_at', 'generated_at']


@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'report_type', 'is_active', 'is_system', 'created_by']
    list_filter = ['report_type', 'is_active', 'is_system']
    search_fields = ['name', 'description']


@admin.register(ExportLog)
class ExportLogAdmin(admin.ModelAdmin):
    list_display = ['report_id', 'export_format', 'status', 'exported_by', 'exported_at']
    list_filter = ['export_format', 'status', 'exported_at']
    readonly_fields = ['exported_at']