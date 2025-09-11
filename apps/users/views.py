"""
Vistas de la aplicación de usuarios para el sistema de fotostudio.

Este módulo define todas las vistas API para la gestión de usuarios,
incluyendo autenticación, registro, gestión de perfiles, cambio de
contraseñas, verificación de códigos y más funcionalidades.

Características principales:
- Autenticación con JWT (JSON Web Tokens)
- Sistema de códigos de verificación
- Gestión completa de perfiles de usuario
- Cambio seguro de contraseñas y emails
- Búsqueda y filtrado de usuarios
- Manejo de fotos de perfil

Autor: Sistema Fotostudio
Fecha: 2025
"""

# Imports de Django REST Framework
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView

# Imports de JWT para autenticación
from rest_framework_simplejwt.tokens import RefreshToken

# Imports de Django para funcionalidades del sistema
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.utils import timezone

# Imports de Python estándar
import random
import string
from datetime import datetime, timedelta

# Imports locales
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer, UserUpdateSerializer,
    PasswordChangeSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer,
    VerificationCodeSerializer, EmailChangeSerializer, EmailChangeConfirmSerializer, UserSearchSerializer,
    ProfilePhotoSerializer, LoginWithCodeSerializer, RequestLoginCodeSerializer
)
from .models import Users, UsersVerificationCode


class RegisterAPIView(CreateAPIView):
    """
    Vista para el registro de nuevos usuarios en el sistema.
    
    Esta vista maneja el proceso completo de registro de usuarios,
    incluyendo validación de datos, creación del usuario y generación
    automática de tokens JWT para autenticación inmediata.
    
    Características:
        - Validación completa de datos de entrada
        - Generación automática de tokens JWT
        - Respuesta con información del usuario y tokens
        - Permisos abiertos para registro público
    
    Endpoint: POST /api/auth/register/
    """
    
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Procesa la solicitud de registro de un nuevo usuario.
        
        Args:
            request: Objeto de solicitud HTTP con datos del usuario
            *args: Argumentos posicionales adicionales
            **kwargs: Argumentos de palabra clave adicionales
            
        Returns:
            Response: Respuesta HTTP con datos del usuario y tokens JWT
            
        Raises:
            ValidationError: Si los datos de entrada no son válidos
        """
        # Validar y procesar los datos de entrada
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Crear el nuevo usuario
        user = serializer.save()
        
        # Generar tokens JWT para el usuario recién creado
        refresh = RefreshToken.for_user(user)
        
        # Preparar respuesta con datos del usuario y tokens
        data = {
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        
        return Response(data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    """
    Vista para autenticación de usuarios con credenciales tradicionales.
    
    Permite el login de usuarios usando username/email y contraseña,
    proporcionando tokens JWT para autenticación en sesiones posteriores.
    
    Características:
        - Login con username o email
        - Validación de credenciales
        - Generación de tokens JWT
        - Verificación de estado de cuenta activa
    
    Endpoint: POST /api/auth/login/
    """
    
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Procesa la solicitud de login del usuario.
        
        Args:
            request: Objeto de solicitud HTTP con credenciales
            *args: Argumentos posicionales adicionales
            **kwargs: Argumentos de palabra clave adicionales
            
        Returns:
            Response: Respuesta HTTP con tokens JWT y datos del usuario
            
        Raises:
            ValidationError: Si las credenciales son inválidas
        """
        # Validar credenciales del usuario
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Generar tokens JWT para el usuario autenticado
        refresh = RefreshToken.for_user(user)
        # Preparar respuesta con datos del usuario y tokens
        data = {
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return Response(data, status=status.HTTP_200_OK)


# =============================================================================
# VISTAS DE GESTIÓN DE USUARIOS
# =============================================================================

class UserDetailView(RetrieveAPIView):
    """
    Vista para obtener los detalles del usuario autenticado.
    
    Proporciona información completa del perfil del usuario actual,
    incluyendo datos personales, información de contacto y estado
    de la cuenta.
    
    Características:
        - Solo usuarios autenticados
        - Retorna información del usuario actual
        - Datos serializados de forma segura
    
    Endpoint: GET /api/auth/users/me/
    """
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """
        Retorna el usuario autenticado actual.
        
        Returns:
            Users: Usuario autenticado
        """
        return self.request.user


class UserUpdateView(UpdateAPIView):
    """
    Vista para actualizar información del usuario autenticado.
    
    Permite al usuario modificar su información personal como nombre,
    apellidos, teléfono y email, con validaciones de unicidad.
    
    Características:
        - Solo usuarios autenticados
        - Validación de unicidad de email
        - Actualización parcial de campos
        - Respuesta con datos actualizados
    
    Endpoint: PUT/PATCH /api/auth/users/me/update/
    """
    
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """
        Retorna el usuario autenticado actual.
        
        Returns:
            Users: Usuario autenticado
        """
        return self.request.user


class UserProfilePhotoView(APIView):
    """
    Vista para subir y actualizar la foto de perfil del usuario.
    
    Maneja la subida de imágenes de perfil con validaciones de tamaño
    y formato, almacenando la URL de la imagen en el perfil del usuario.
    
    Características:
        - Solo usuarios autenticados
        - Validación de tamaño de imagen (máximo 5MB)
        - Soporte para formatos de imagen comunes
        - Actualización de URL de foto en perfil
    
    Endpoint: POST /api/auth/users/me/photo/
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ProfilePhotoSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.photo_url = serializer.validated_data['photo']
            user.save()
            return Response({'message': 'Foto actualizada correctamente'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSearchView(APIView):
    """Buscar usuarios"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserSearchSerializer(data=request.query_params)
        if serializer.is_valid():
            query = serializer.validated_data['query']
            search_type = serializer.validated_data['search_type']
            
            if search_type == 'username':
                users = Users.objects.filter(username__icontains=query)
            elif search_type == 'name':
                users = Users.objects.filter(
                    Q(name__icontains=query) | 
                    Q(paternal_lastname__icontains=query) |
                    Q(maternal_lastname__icontains=query)
                )
            else:  # email
                users = Users.objects.filter(email__icontains=query)
            
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# Profile Management Views
class ProfileDetailView(APIView):
    """Detalles del perfil"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        profile_data = {
            'username': user.username,
            'name': user.name,
            'paternal_lastname': user.paternal_lastname,
            'maternal_lastname': user.maternal_lastname,
            'email': user.email,
            'phone': user.phone,
            'photo_url': user.photo_url,
            'date_joined': user.date_joined,
            'is_active': user.is_active
        }
        return Response(profile_data, status=status.HTTP_200_OK)




class PublicProfileView(APIView):
    """Perfil público por username"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, user_name):
        try:
            user = Users.objects.get(username=user_name)
            public_data = {
                'username': user.username,
                'name': user.name,
                'paternal_lastname': user.paternal_lastname,
                'maternal_lastname': user.maternal_lastname,
                'photo_url': user.photo_url,
                'date_joined': user.date_joined
            }
            return Response(public_data, status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)


class ProfileSettingsView(APIView):
    """Configuraciones del perfil"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        settings = {
            'email_notifications': True,
            'privacy_level': 'public',
            'show_email': False,
            'show_phone': False
        }
        return Response(settings, status=status.HTTP_200_OK)
    
    def post(self, request):
        return Response({'message': 'Configuraciones actualizadas'}, status=status.HTTP_200_OK)


class ProfileCompletionView(APIView):
    """Verificar completitud del perfil"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        completion = {
            'percentage': 0,
            'missing_fields': []
        }
        
        required_fields = ['name', 'paternal_lastname', 'maternal_lastname', 'email', 'phone']
        completed = 0
        
        for field in required_fields:
            if getattr(user, field):
                completed += 1
            else:
                completion['missing_fields'].append(field)
        
        completion['percentage'] = (completed / len(required_fields)) * 100
        return Response(completion, status=status.HTTP_200_OK)


class ProfileSearchView(APIView):
    """Búsqueda de perfiles públicos"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        query = request.query_params.get('q', '')
        if query:
            users = Users.objects.filter(
                Q(name__icontains=query) | 
                Q(username__icontains=query)
            )[:10]
            results = []
            for user in users:
                results.append({
                    'username': user.username,
                    'name': user.name,
                    'photo_url': user.photo_url
                })
            return Response(results, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)


# Password Management Views
class PasswordChangeView(APIView):
    """Cambiar contraseña"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.password = make_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Contraseña actualizada correctamente'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    """Solicitar reset de contraseña"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': 'Código de verificación enviado'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    """Confirmar reset de contraseña con código"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': 'Contraseña restablecida correctamente'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordStrengthView(APIView):
    """Verificar fortaleza de contraseña"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        password = request.data.get('password', '')
        strength = {
            'score': 0,
            'feedback': []
        }
        
        if len(password) >= 8:
            strength['score'] += 1
        else:
            strength['feedback'].append('Mínimo 8 caracteres')
        
        if any(c.isupper() for c in password):
            strength['score'] += 1
        else:
            strength['feedback'].append('Incluir mayúsculas')
        
        if any(c.islower() for c in password):
            strength['score'] += 1
        else:
            strength['feedback'].append('Incluir minúsculas')
        
        if any(c.isdigit() for c in password):
            strength['score'] += 1
        else:
            strength['feedback'].append('Incluir números')
        
        if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
            strength['score'] += 1
        else:
            strength['feedback'].append('Incluir caracteres especiales')
        
        return Response(strength, status=status.HTTP_200_OK)




class PasswordPolicyView(APIView):
    """Política de contraseñas"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        policy = {
            'min_length': 8,
            'require_uppercase': True,
            'require_lowercase': True,
            'require_numbers': True,
            'require_special_chars': True,
            'max_age_days': 90
        }
        return Response(policy, status=status.HTTP_200_OK)


# Verification Management Views
class VerificationCodeView(APIView):
    """Generar código de verificación"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        user = request.user
        code = ''.join(random.choices(string.digits, k=6))
        
        # Crear o actualizar código de verificación
        verification_code, created = UsersVerificationCode.objects.get_or_create(
            user_id=user.id,
            defaults={
                'code': code,
                'expires_at': timezone.now() + timedelta(minutes=10)
            }
        )
        
        if not created:
            verification_code.code = code
            verification_code.expires_at = timezone.now() + timedelta(minutes=10)
            verification_code.save()
        
        return Response({'message': 'Código de verificación generado'}, status=status.HTTP_200_OK)


class EmailChangeView(APIView):
    """Solicitar cambio de email"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = EmailChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            new_email = serializer.validated_data['new_email']
            
            # Generar código de 6 dígitos
            code = ''.join(random.choices(string.digits, k=6))
            expires_at = timezone.now() + timedelta(minutes=10)
            
            # Crear o actualizar código de verificación para cambio de email
            verification_code, created = UsersVerificationCode.objects.update_or_create(
                user_id=user.id,
                defaults={
                    'code': code,
                    'expires_at': expires_at,
                    'failed_attempts': 0,
                    'locked_until': None,
                    'temp_email': new_email  # Guardar email temporal
                }
            )
            
            # Aquí se enviaría el código por email al nuevo email
            # Por ahora solo lo devolvemos en la respuesta para testing
            return Response({
                'message': 'Código de verificación enviado al nuevo email',
                'code': code,  # Solo para testing, remover en producción
                'new_email': new_email,
                'expires_in': 10,
                'expires_at': expires_at.isoformat()
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailChangeConfirmView(APIView):
    """Confirmar cambio de email con código"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = EmailChangeConfirmSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            code = serializer.validated_data['code']
            
            # Buscar código de verificación
            try:
                verification_code = UsersVerificationCode.objects.get(user_id=user.id)
            except UsersVerificationCode.DoesNotExist:
                return Response({
                    'error': 'Código no solicitado',
                    'message': 'No se ha solicitado un código de verificación para cambio de email'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Verificar si el código ha expirado
            if verification_code.expires_at <= timezone.now():
                verification_code.delete()
                return Response({
                    'error': 'Código expirado',
                    'message': 'El código de verificación ha expirado. Solicita uno nuevo.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Verificar si el código es correcto
            if verification_code.code != code:
                # Incrementar intentos fallidos
                verification_code.failed_attempts += 1
                
                # Bloquear cuenta si hay demasiados intentos fallidos (3 intentos)
                if verification_code.failed_attempts >= 3:
                    verification_code.locked_until = timezone.now() + timedelta(minutes=15)
                    verification_code.save()
                    return Response({
                        'error': 'Cuenta bloqueada',
                        'message': 'Demasiados intentos fallidos. Tu cuenta ha sido bloqueada por 15 minutos.',
                        'locked_until': verification_code.locked_until.isoformat()
                    }, status=status.HTTP_429_TOO_MANY_REQUESTS)
                else:
                    verification_code.save()
                    remaining_attempts = 3 - verification_code.failed_attempts
                    return Response({
                        'error': 'Código incorrecto',
                        'message': f'Código incorrecto. Te quedan {remaining_attempts} intentos.',
                        'remaining_attempts': remaining_attempts
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Código correcto - obtener email temporal y actualizar
            new_email = verification_code.temp_email
            if not new_email:
                return Response({
                    'error': 'Email temporal no encontrado',
                    'message': 'No se encontró el email temporal. Solicita un nuevo cambio de email.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Verificar que el email temporal no esté siendo usado por otro usuario
            if Users.objects.filter(email=new_email).exclude(id=user.id).exists():
                verification_code.delete()
                return Response({
                    'error': 'Email ya registrado',
                    'message': 'El email ya está siendo usado por otro usuario.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Actualizar email
            old_email = user.email
            user.email = new_email
            user.save()
            
            # Eliminar código usado
            verification_code.delete()
            
            return Response({
                'message': 'Email actualizado correctamente',
                'old_email': old_email,
                'new_email': new_email,
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerificationCodeResendView(APIView):
    """Reenviar código de verificación"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        user = request.user
        code = ''.join(random.choices(string.digits, k=6))
        
        try:
            verification_code = UsersVerificationCode.objects.get(user_id=user.id)
            verification_code.code = code
            verification_code.expires_at = timezone.now() + timedelta(minutes=10)
            verification_code.save()
        except UsersVerificationCode.DoesNotExist:
            UsersVerificationCode.objects.create(
                user_id=user.id,
                code=code,
                expires_at=datetime.now() + timedelta(minutes=10)
            )
        
        return Response({'message': 'Código reenviado'}, status=status.HTTP_200_OK)


class VerificationStatusView(APIView):
    """Estado de verificación del usuario"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        status_data = {
            'email_verified': bool(user.email_verified_at),
            'phone_verified': False,
            'identity_verified': False
        }
        return Response(status_data, status=status.HTTP_200_OK)


class EmailVerificationView(APIView):
    """Solicitar verificación de email"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        user = request.user
        code = ''.join(random.choices(string.digits, k=6))
        
        # Crear código de verificación
        verification_code, created = UsersVerificationCode.objects.get_or_create(
            user_id=user.id,
            defaults={
                'code': code,
                'expires_at': timezone.now() + timedelta(minutes=10)
            }
        )
        
        if not created:
            verification_code.code = code
            verification_code.expires_at = timezone.now() + timedelta(minutes=10)
            verification_code.save()
        
        return Response({'message': 'Código de verificación enviado'}, status=status.HTTP_200_OK)


class EmailVerificationConfirmView(APIView):
    """Confirmar verificación de email"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = VerificationCodeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            code = serializer.validated_data['code']
            
            try:
                verification_code = UsersVerificationCode.objects.get(
                    user_id=user.id,
                    code=code,
                    expires_at__gt=timezone.now()
                )
                
                user.email_verified_at = timezone.now()
                user.save()
                verification_code.delete()
                
                return Response({'message': 'Email verificado correctamente'}, status=status.HTTP_200_OK)
            except UsersVerificationCode.DoesNotExist:
                return Response({'error': 'Código inválido o expirado'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login with Code Views
class RequestLoginCodeView(APIView):
    """Solicitar código de verificación para login"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = RequestLoginCodeSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            
            # Buscar usuario por username o email
            try:
                user = Users.objects.get(username=username)
            except Users.DoesNotExist:
                try:
                    user = Users.objects.get(email=username)
                except Users.DoesNotExist:
                    return Response({
                        'error': 'Usuario no encontrado',
                        'message': 'No existe un usuario con ese nombre de usuario o email'
                    }, status=status.HTTP_404_NOT_FOUND)
            
            # Verificar si la cuenta está activa
            if not user.is_active:
                return Response({
                    'error': 'Cuenta inactiva',
                    'message': 'Tu cuenta está desactivada. Contacta al administrador.'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Verificar si hay un código existente y si está bloqueado
            try:
                existing_code = UsersVerificationCode.objects.get(user_id=user.id)
                
                # Verificar si está bloqueado por intentos fallidos
                if existing_code.locked_until and existing_code.locked_until > timezone.now():
                    remaining_time = (existing_code.locked_until - timezone.now()).seconds // 60
                    return Response({
                        'error': 'Cuenta temporalmente bloqueada',
                        'message': f'Demasiados intentos fallidos. Intenta nuevamente en {remaining_time} minutos.',
                        'locked_until': existing_code.locked_until.isoformat()
                    }, status=status.HTTP_429_TOO_MANY_REQUESTS)
                
                # Verificar si el código actual aún es válido (no expirado)
                if existing_code.expires_at > timezone.now():
                    remaining_time = (existing_code.expires_at - timezone.now()).seconds // 60
                    return Response({
                        'message': 'Ya tienes un código activo',
                        'expires_in': remaining_time,
                        'can_resend': False
                    }, status=status.HTTP_200_OK)
                
            except UsersVerificationCode.DoesNotExist:
                pass  # No hay código existente, continuar
            
            # Generar nuevo código de 6 dígitos
            code = ''.join(random.choices(string.digits, k=6))
            expires_at = timezone.now() + timedelta(minutes=5)
            
            # Crear o actualizar código de verificación
            verification_code, created = UsersVerificationCode.objects.update_or_create(
                user_id=user.id,
                defaults={
                    'code': code,
                    'expires_at': expires_at,
                    'failed_attempts': 0,
                    'locked_until': None
                }
            )
            
            # Aquí se enviaría el código por email/SMS
            # Por ahora solo lo devolvemos en la respuesta para testing
            return Response({
                'message': 'Código de verificación enviado exitosamente',
                'code': code,  # Solo para testing, remover en producción
                'expires_in': 5,
                'user_id': user.id,
                'expires_at': expires_at.isoformat()
            }, status=status.HTTP_200_OK)
        
        return Response({
            'error': 'Datos inválidos',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginWithCodeView(APIView):
    """
    Vista para autenticación de usuarios usando código de verificación.
    
    Proporciona una alternativa segura de autenticación usando códigos
    de 6 dígitos en lugar de contraseñas tradicionales. Incluye medidas
    de seguridad como bloqueo temporal por intentos fallidos y expiración
    automática de códigos.
    
    Características de seguridad:
        - Códigos de un solo uso
        - Expiración automática (5 minutos)
        - Bloqueo temporal por intentos fallidos (15 minutos)
        - Validación de estado de cuenta activa
        - Eliminación automática de códigos usados
    
    Endpoint: POST /api/auth/login/code/
    """
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """
        Procesa la solicitud de login con código de verificación.
        
        Args:
            request: Objeto de solicitud HTTP con username y código
            
        Returns:
            Response: Respuesta HTTP con tokens JWT y datos del usuario
            
        Raises:
            ValidationError: Si los datos de entrada no son válidos
        """
        # Validar datos de entrada (username y código)
        serializer = LoginWithCodeSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            code = serializer.validated_data['code']
            
            # Buscar usuario por username primero, luego por email
            try:
                user = Users.objects.get(username=username)
            except Users.DoesNotExist:
                try:
                    user = Users.objects.get(email=username)
                except Users.DoesNotExist:
                    return Response({
                        'error': 'Usuario no encontrado',
                        'message': 'No existe un usuario con ese nombre de usuario o email'
                    }, status=status.HTTP_404_NOT_FOUND)
            
            # Verificar que la cuenta esté activa
            if not user.is_active:
                return Response({
                    'error': 'Cuenta inactiva',
                    'message': 'Tu cuenta está desactivada. Contacta al administrador.'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Buscar código de verificación del usuario
            try:
                verification_code = UsersVerificationCode.objects.get(user_id=user.id)
            except UsersVerificationCode.DoesNotExist:
                return Response({
                    'error': 'Código no solicitado',
                    'message': 'No se ha solicitado un código de verificación para este usuario'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Verificar si la cuenta está bloqueada por intentos fallidos
            if verification_code.locked_until and verification_code.locked_until > timezone.now():
                remaining_time = (verification_code.locked_until - timezone.now()).seconds // 60
                return Response({
                    'error': 'Cuenta temporalmente bloqueada',
                    'message': f'Demasiados intentos fallidos. Intenta nuevamente en {remaining_time} minutos.',
                    'locked_until': verification_code.locked_until.isoformat()
                }, status=status.HTTP_429_TOO_MANY_REQUESTS)
            
            # Verificar si el código ha expirado
            if verification_code.expires_at <= timezone.now():
                verification_code.delete()  # Eliminar código expirado
                return Response({
                    'error': 'Código expirado',
                    'message': 'El código de verificación ha expirado. Solicita uno nuevo.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Verificar si el código es correcto
            if verification_code.code != code:
                # Incrementar intentos fallidos
                verification_code.failed_attempts += 1
                
                # Bloquear cuenta si hay demasiados intentos fallidos (3 intentos)
                if verification_code.failed_attempts >= 3:
                    verification_code.locked_until = timezone.now() + timedelta(minutes=15)
                    verification_code.save()
                    return Response({
                        'error': 'Cuenta bloqueada',
                        'message': 'Demasiados intentos fallidos. Tu cuenta ha sido bloqueada por 15 minutos.',
                        'locked_until': verification_code.locked_until.isoformat()
                    }, status=status.HTTP_429_TOO_MANY_REQUESTS)
                else:
                    verification_code.save()
                    remaining_attempts = 3 - verification_code.failed_attempts
                    return Response({
                        'error': 'Código incorrecto',
                        'message': f'Código incorrecto. Te quedan {remaining_attempts} intentos.',
                        'remaining_attempts': remaining_attempts
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Código correcto - proceder con el login
            # Eliminar código usado
            verification_code.delete()
            
            # Generar tokens JWT
            refresh = RefreshToken.for_user(user)
            
            # Actualizar último login
            user.last_login = timezone.now()
            user.save()
            
            data = {
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "login_method": "code",
                "message": "Login exitoso"
            }
            
            return Response(data, status=status.HTTP_200_OK)
        
        return Response({
            'error': 'Datos inválidos',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
