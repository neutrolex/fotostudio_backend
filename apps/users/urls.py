"""
Configuración de URLs para la aplicación de usuarios del sistema de fotostudio.

Este módulo define todas las rutas URL para los endpoints de la API de usuarios,
organizadas por categorías funcionales para facilitar el mantenimiento y
la comprensión del sistema.

Categorías de endpoints:
- Autenticación: Registro, login tradicional y con código
- Gestión de usuarios: CRUD de información personal
- Gestión de perfiles: Perfiles públicos y privados
- Gestión de contraseñas: Cambio, reset y políticas
- Verificación: Códigos de verificación y cambio de email

Autor: Sistema Fotostudio
Fecha: 2025
"""

from django.urls import path

# Imports de vistas locales
from .views import (
    # Vistas de autenticación
    RegisterAPIView, LoginAPIView, LogoutAPIView,
    RequestLoginCodeView, LoginWithCodeView,
    
    # Vistas de gestión de usuarios
    UserDetailView, UserUpdateView, UserProfilePhotoView, UserSearchView,
    
    # Vistas de gestión de perfiles
    ProfileDetailView, PublicProfileView, ProfileSettingsView,
    ProfileCompletionView, ProfileSearchView,
    
    # Vistas de gestión de contraseñas
    PasswordChangeView, PasswordResetView, PasswordResetConfirmView, 
    PasswordStrengthView, PasswordPolicyView,
    
    # Vistas de verificación
    VerificationCodeView, EmailChangeView, EmailChangeConfirmView, 
    VerificationCodeResendView, VerificationStatusView, 
    EmailVerificationView, EmailVerificationConfirmView,
    
    # Vistas compatibles con frontend
    UpdateProfileView, ChangePasswordView, UploadAvatarView, UserProfileView
)

# Import de vista JWT para refresh de tokens
from rest_framework_simplejwt.views import TokenRefreshView

# =============================================================================
# CONFIGURACIÓN DE URLS
# =============================================================================

urlpatterns = [
    # ========================================================================
    # ENDPOINTS DE AUTENTICACIÓN
    # ========================================================================
    # Registro de nuevos usuarios
    path('register/', RegisterAPIView.as_view(), name='auth-register'),
    
    # Login tradicional con username/email y contraseña
    path('login/', LoginAPIView.as_view(), name='auth-login'),
    
    # Logout de usuarios autenticados
    path('logout/', LogoutAPIView.as_view(), name='auth-logout'),
    
    # Solicitar código de verificación para login
    path('login/code/request/', RequestLoginCodeView.as_view(), name='login-code-request'),
    
    # Login usando código de verificación
    path('login/code/', LoginWithCodeView.as_view(), name='login-with-code'),
    
    # Refresh de tokens JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('refresh/', TokenRefreshView.as_view(), name='auth-refresh'),  # Alias para compatibilidad
    
    # ========================================================================
    # ENDPOINTS DE GESTIÓN DE USUARIOS
    # ========================================================================
    # Obtener información del usuario autenticado
    path('users/me/', UserDetailView.as_view(), name='user-detail'),
    
    # Actualizar información del usuario autenticado
    path('users/me/update/', UserUpdateView.as_view(), name='user-update'),
    
    # Subir/actualizar foto de perfil
    path('users/me/photo/', UserProfilePhotoView.as_view(), name='user-photo'),
    
    # Buscar usuarios en el sistema
    path('users/search/', UserSearchView.as_view(), name='user-search'),
    
    # Alias para obtener perfil del usuario (compatibilidad)
    path('users/profile/', UserDetailView.as_view(), name='user-profile'),
    path('profile/', UserDetailView.as_view(), name='auth-profile'),  # Alias para compatibilidad
    
    # ========================================================================
    # ENDPOINTS DE GESTIÓN DE PERFILES
    # ========================================================================
    # Obtener perfil detallado del usuario autenticado
    path('profiles/me/', ProfileDetailView.as_view(), name='profile-detail'),
    
    # Crear perfil (reutiliza ProfileDetailView)
    path('profiles/create/', ProfileDetailView.as_view(), name='profile-create'),
    
    # Obtener perfil público de un usuario específico
    path('profiles/public/<str:user_name>/', PublicProfileView.as_view(), name='public-profile'),
    
    # Configuraciones del perfil
    path('profiles/settings/', ProfileSettingsView.as_view(), name='profile-settings'),
    
    # Estado de completitud del perfil
    path('profiles/completion/', ProfileCompletionView.as_view(), name='profile-completion'),
    
    # Búsqueda de perfiles
    path('profiles/search/', ProfileSearchView.as_view(), name='profile-search'),
    
    # ========================================================================
    # ENDPOINTS DE GESTIÓN DE CONTRASEÑAS
    # ========================================================================
    # Cambiar contraseña del usuario autenticado
    path('password/change/', PasswordChangeView.as_view(), name='password-change'),
    
    # Solicitar reset de contraseña
    path('password/reset/', PasswordResetView.as_view(), name='password-reset'),
    
    # Confirmar reset de contraseña con código
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    
    # Verificar fortaleza de contraseña
    path('password/strength/', PasswordStrengthView.as_view(), name='password-strength'),
    
    # Obtener política de contraseñas
    path('password/policy/', PasswordPolicyView.as_view(), name='password-policy'),
    
    # ========================================================================
    # ENDPOINTS DE VERIFICACIÓN
    # ========================================================================
    # Verificar código de verificación
    path('verification/code/', VerificationCodeView.as_view(), name='verification-code'),
    
    # Solicitar cambio de email
    path('verification/email/change/', EmailChangeView.as_view(), name='email-change'),
    
    # Confirmar cambio de email con código
    path('verification/email/change/confirm/', EmailChangeConfirmView.as_view(), name='email-change-confirm'),
    
    # Reenviar código de verificación
    path('verification/code/resend/', VerificationCodeResendView.as_view(), name='verification-resend'),
    
    # Estado de verificación del usuario
    path('verification/status/', VerificationStatusView.as_view(), name='verification-status'),
    
    # Verificación de email
    path('verification/email/', EmailVerificationView.as_view(), name='email-verification'),
    
    # Confirmar verificación de email
    path('verification/email/confirm/', EmailVerificationConfirmView.as_view(), name='email-verification-confirm'),
    
    # ========================================================================
    # ENDPOINTS COMPATIBLES CON FRONTEND
    # ========================================================================
    # Perfil completo del usuario
    path('profile/', UserProfileView.as_view(), name='user-profile-frontend'),
    
    # Actualizar perfil
    path('profile/update/', UpdateProfileView.as_view(), name='update-profile-frontend'),
    
    # Cambiar contraseña
    path('profile/change-password/', ChangePasswordView.as_view(), name='change-password-frontend'),
    
    # Subir avatar
    path('profile/upload-avatar/', UploadAvatarView.as_view(), name='upload-avatar-frontend'),
]
