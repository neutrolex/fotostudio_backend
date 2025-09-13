"""
URLs para el sistema de reportes.
"""

from django.urls import path
from .views import (
    ReportListView, ReportDetailView, ReportGenerateView,
    report_categories, ReportExportCSVView,
    ReportExportExcelView, ReportExportPDFView
)

urlpatterns = [
    # Reportes
    path('', ReportListView.as_view(), name='report-list'),
    path('<int:pk>/', ReportDetailView.as_view(), name='report-detail'),
    path('generate/', ReportGenerateView.as_view(), name='report-generate'),
    path('export/csv/<int:pk>/', ReportExportCSVView.as_view(), name='report-export-csv'),
    path('export/excel/<int:pk>/', ReportExportExcelView.as_view(), name='report-export-excel'),
    path('export/pdf/<int:pk>/', ReportExportPDFView.as_view(), name='report-export-pdf'),
    
    # Categorías y formatos
    path('categories/', report_categories, name='report-categories'),
]
