from django.apps import AppConfig


class MetricsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.metrics'
    verbose_name = 'Sistema de Métricas y KPIs'