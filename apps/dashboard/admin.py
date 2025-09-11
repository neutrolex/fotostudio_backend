from django.contrib import admin
from django.contrib.admin import AdminSite
from django.http import HttpResponseRedirect
from django.urls import reverse


class DashboardAdminSite(AdminSite):
    site_header = "Fotostudio Dashboard"
    site_title = "Fotostudio Admin"
    index_title = "Panel de Administración"
    
    def index(self, request, extra_context=None):
        # Redirigir al dashboard personalizado
        return HttpResponseRedirect(reverse('dashboard:main'))


# Registrar el sitio de admin personalizado
dashboard_admin = DashboardAdminSite(name='dashboard_admin')
