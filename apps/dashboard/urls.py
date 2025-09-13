"""
URLs para la app de dashboard.
"""

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('stats/', views.DashboardStatsView.as_view(), name='dashboard-stats'),
    path('activities/', views.DashboardActivitiesView.as_view(), name='dashboard-activities'),
    path('upcoming/', views.DashboardUpcomingView.as_view(), name='dashboard-upcoming'),
    path('orders/', views.DashboardOrdersView.as_view(), name='dashboard-orders'),
    path('clients/', views.DashboardClientsView.as_view(), name='dashboard-clients'),
    path('revenue/', views.DashboardRevenueView.as_view(), name='dashboard-revenue'),
]
