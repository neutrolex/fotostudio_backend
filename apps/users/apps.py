from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'   # 👈 ruta completa del módulo
    label = 'users'       # 👈 nombre corto para usar en makemigrations
