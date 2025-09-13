"""
URLs para el sistema de reportes.
"""

from django.urls import path
from .views import (
    ReportListView, ReportDetailView, ReportGenerateView,
    report_categories, ReportExportCSVView,
    ReportExportExcelView, ReportExportPDFView,
    SalesReportView, InventoryReportView, ClientsReportView, ReportExportView
)

urlpatterns = [
    # Reportes
    path('', ReportListView.as_view(), name='report-list'),
    path('<int:pk>/', ReportDetailView.as_view(), name='report-detail'),
    path('generate/', ReportGenerateView.as_view(), name='report-generate'),
    path('export/csv/<int:pk>/', ReportExportCSVView.as_view(), name='report-export-csv'),
    path('export/excel/<int:pk>/', ReportExportExcelView.as_view(), name='report-export-excel'),
    path('export/pdf/<int:pk>/', ReportExportPDFView.as_view(), name='report-export-pdf'),
    
    # Endpoints compatibles con frontend
    path('sales/', SalesReportView.as_view(), name='sales-report'),
    path('inventory/', InventoryReportView.as_view(), name='inventory-report'),
    path('clients/', ClientsReportView.as_view(), name='clients-report'),
    path('export/', ReportExportView.as_view(), name='report-export'),
    
    # Categorías y formatos
    path('categories/', report_categories, name='report-categories'),
]
