from django.contrib import admin
from .models import Users, UsersVerificationCode, Admin, DocumentTypes


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'name', 'paternal_lastname', 'email', 'is_active', 'date_joined')
    list_filter = ('is_active', 'date_joined', 'tenant_id')
    search_fields = ('username', 'name', 'paternal_lastname', 'email', 'phone')
    readonly_fields = ('id', 'date_joined', 'last_login')
    ordering = ('-date_joined',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'tenant_id', 'username', 'name', 'paternal_lastname', 'maternal_lastname')
        }),
        ('Contacto', {
            'fields': ('email', 'phone', 'photo_url')
        }),
        ('Documento', {
            'fields': ('document_number', 'document_type')
        }),
        ('Estado de la Cuenta', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Fechas', {
            'fields': ('date_joined', 'last_login', 'email_verified_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UsersVerificationCode)
class UsersVerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'code', 'expires_at', 'failed_attempts', 'created_at')
    list_filter = ('expires_at', 'created_at')
    search_fields = ('user_id', 'code', 'temp_email')
    readonly_fields = ('id', 'created_at')
    ordering = ('-created_at',)


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('id', 'date_joined', 'last_login')
    ordering = ('-date_joined',)


@admin.register(DocumentTypes)
class DocumentTypesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    readonly_fields = ('id',)
    ordering = ('name',)
