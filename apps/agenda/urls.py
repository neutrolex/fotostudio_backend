"""
URLs para la app de agenda.
"""

from django.urls import path
from . import views

app_name = 'agenda'

urlpatterns = [
    path('', views.AppointmentListView.as_view(), name='appointment-list'),
    path('<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment-detail'),
    path('calendar/', views.AppointmentCalendarView.as_view(), name='appointment-calendar'),
]
