"""
Serializers de la aplicación de usuarios para el sistema de fotostudio.

Este módulo define todos los serializers necesarios para la validación,
serialización y deserialización de datos relacionados con usuarios.
Incluye serializers para autenticación, registro, gestión de perfiles,
cambio de contraseñas, verificación de códigos y más.

Autor: Sistema Fotostudio
Fecha: 2025
"""

from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

# Importación del modelo de usuarios
from .models import Users


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para la representación básica de usuarios.
    
    Este serializer se utiliza para exponer información pública del usuario
    sin incluir datos sensibles como contraseñas o tokens.
    
    Campos expuestos:
        - Información básica: id, tenant_id, username, name, apellidos
        - Información de contacto: email, phone
        - Estado: is_active, date_joined
    """
    
    class Meta:
        model = Users
        fields = (
            'id', 'tenant_id', 'username', 'name', 'paternal_lastname',
            'maternal_lastname', 'email', 'phone', 'is_active', 'date_joined'
        )
        read_only_fields = ('id', 'date_joined')


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer para el registro de nuevos usuarios.
    
    Maneja la validación y creación de nuevos usuarios en el sistema,
    incluyendo validaciones de unicidad y hashing seguro de contraseñas.
    
    Validaciones incluidas:
        - Email único en el sistema
        - Username único en el sistema
        - Contraseña mínima de 8 caracteres
        - Campos requeridos según el modelo
    """
    
    # Campo de contraseña con validación de longitud mínima
    password = serializers.CharField(
        write_only=True, 
        min_length=8,
        help_text="Contraseña del usuario (mínimo 8 caracteres)"
    )
    
    # Campo de tenant_id requerido para multi-tenancy
    tenant_id = serializers.IntegerField(
        help_text="ID del tenant para multi-tenancy"
    )

    class Meta:
        model = Users
        fields = (
            'id', 'tenant_id', 'document_number', 'name', 'paternal_lastname',
            'maternal_lastname', 'email', 'username', 'password', 'phone'
        )
        read_only_fields = ('id',)

    def validate_email(self, value):
        """
        Valida que el email no esté ya registrado en el sistema.
        
        Args:
            value (str): Email a validar
            
        Returns:
            str: Email validado
            
        Raises:
            ValidationError: Si el email ya está registrado
        """
        if Users.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email ya registrado")
        return value

    def validate_username(self, value):
        """
        Valida que el username no esté ya en uso.
        
        Args:
            value (str): Username a validar
            
        Returns:
            str: Username validado
            
        Raises:
            ValidationError: Si el username ya existe
        """
        if Users.objects.filter(username=value).exists():
            raise serializers.ValidationError("Nombre de usuario ya existe")
        return value

    def create(self, validated_data):
        """
        Crea un nuevo usuario con contraseña hasheada.
        
        Args:
            validated_data (dict): Datos validados del usuario
            
        Returns:
            Users: Usuario creado con contraseña hasheada
        """
        # Extraer contraseña en texto plano
        raw_password = validated_data.pop('password')
        
        # Hashear la contraseña usando el sistema de Django
        hashed = make_password(raw_password)
        validated_data['password'] = hashed
        
        # Establecer valores por defecto
        validated_data.setdefault('is_active', True)
        validated_data.setdefault('date_joined', timezone.now())
        
        # Crear el usuario
        user = Users.objects.create(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer para autenticación de usuarios con username/email y contraseña.
    
    Permite el login tanto con username como con email, proporcionando
    flexibilidad en el proceso de autenticación.
    
    Validaciones incluidas:
        - Usuario existe (por username o email)
        - Usuario está activo
        - Contraseña es correcta
    """
    
    username = serializers.CharField(
        help_text="Nombre de usuario o email para autenticación"
    )
    password = serializers.CharField(
        write_only=True,
        help_text="Contraseña del usuario"
    )

    def validate(self, attrs):
        """
        Valida las credenciales del usuario.
        
        Args:
            attrs (dict): Atributos del serializer (username, password)
            
        Returns:
            dict: Atributos con el usuario validado incluido
            
        Raises:
            ValidationError: Si las credenciales son inválidas
        """
        username = attrs.get('username')
        password = attrs.get('password')

        # Buscar usuario por username primero, luego por email
        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            try:
                user = Users.objects.get(email=username)
            except Users.DoesNotExist:
                raise serializers.ValidationError("Usuario o correo no encontrado")

        # Verificar que la cuenta esté activa
        if not user.is_active:
            raise serializers.ValidationError("Cuenta inactiva")

        # Verificar la contraseña
        if not check_password(password, user.password):
            raise serializers.ValidationError("Credenciales inválidas")

        # Agregar el usuario validado a los atributos
        attrs['user'] = user
        return attrs


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para actualización de información del usuario.
    
    Permite actualizar información personal del usuario como nombre,
    apellidos, teléfono y email, con validaciones de unicidad.
    """
    
    class Meta:
        model = Users
        fields = ('name', 'paternal_lastname', 'maternal_lastname', 'phone', 'email')
        
    def validate_email(self, value):
        """
        Valida que el nuevo email no esté en uso por otro usuario.
        
        Args:
            value (str): Nuevo email a validar
            
        Returns:
            str: Email validado
            
        Raises:
            ValidationError: Si el email ya está registrado
        """
        if Users.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("Email ya registrado")
        return value


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer para cambio de contraseña de usuario autenticado.
    
    Requiere la contraseña actual para autorizar el cambio y valida
    que la nueva contraseña y su confirmación coincidan.
    """
    
    old_password = serializers.CharField(
        write_only=True,
        help_text="Contraseña actual del usuario"
    )
    new_password = serializers.CharField(
        write_only=True, 
        min_length=8,
        help_text="Nueva contraseña (mínimo 8 caracteres)"
    )
    confirm_password = serializers.CharField(
        write_only=True,
        help_text="Confirmación de la nueva contraseña"
    )
    
    def validate(self, attrs):
        """
        Valida que las contraseñas nuevas coincidan.
        
        Args:
            attrs (dict): Atributos del serializer
            
        Returns:
            dict: Atributos validados
            
        Raises:
            ValidationError: Si las contraseñas no coinciden
        """
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return attrs
    
    def validate_old_password(self, value):
        """
        Valida que la contraseña actual sea correcta.
        
        Args:
            value (str): Contraseña actual a validar
            
        Returns:
            str: Contraseña validada
            
        Raises:
            ValidationError: Si la contraseña actual es incorrecta
        """
        user = self.context['request'].user
        if not check_password(value, user.password):
            raise serializers.ValidationError("Contraseña actual incorrecta")
        return value


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer para solicitar reset de contraseña.
    
    Valida que el email proporcionado exista en el sistema antes
    de enviar el código de verificación.
    """
    
    email = serializers.EmailField(
        help_text="Email del usuario para reset de contraseña"
    )
    
    def validate_email(self, value):
        """
        Valida que el email exista en el sistema.
        
        Args:
            value (str): Email a validar
            
        Returns:
            str: Email validado
            
        Raises:
            ValidationError: Si el email no existe
        """
        if not Users.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email no encontrado")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer para confirmar reset de contraseña con código.
    
    Valida que la nueva contraseña y su confirmación coincidan
    antes de proceder con el cambio.
    """
    
    new_password = serializers.CharField(
        write_only=True, 
        min_length=8,
        help_text="Nueva contraseña (mínimo 8 caracteres)"
    )
    confirm_password = serializers.CharField(
        write_only=True,
        help_text="Confirmación de la nueva contraseña"
    )
    
    def validate(self, attrs):
        """
        Valida que las contraseñas coincidan.
        
        Args:
            attrs (dict): Atributos del serializer
            
        Returns:
            dict: Atributos validados
            
        Raises:
            ValidationError: Si las contraseñas no coinciden
        """
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return attrs


class VerificationCodeSerializer(serializers.Serializer):
    """
    Serializer para códigos de verificación de 6 dígitos.
    
    Valida que el código tenga exactamente 6 dígitos numéricos.
    """
    
    code = serializers.CharField(
        max_length=6,
        help_text="Código de verificación de 6 dígitos"
    )
    
    def validate_code(self, value):
        """
        Valida el formato del código de verificación.
        
        Args:
            value (str): Código a validar
            
        Returns:
            str: Código validado
            
        Raises:
            ValidationError: Si el código no tiene el formato correcto
        """
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("Código debe ser de 6 dígitos")
        return value


class EmailChangeConfirmSerializer(serializers.Serializer):
    """
    Serializer para confirmar cambio de email con código.
    
    Este serializer solo requiere el código de verificación ya que
    el nuevo email se almacena temporalmente en el paso anterior.
    """
    
    code = serializers.CharField(
        max_length=6,
        help_text="Código de verificación de 6 dígitos para confirmar cambio de email"
    )
    
    def validate_code(self, value):
        """
        Valida el formato del código de verificación.
        
        Args:
            value (str): Código a validar
            
        Returns:
            str: Código validado
            
        Raises:
            ValidationError: Si el código no tiene el formato correcto
        """
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError("Código debe ser de 6 dígitos")
        return value


class EmailChangeSerializer(serializers.Serializer):
    """
    Serializer para solicitar cambio de email.
    
    Valida que el nuevo email no esté ya registrado en el sistema.
    """
    
    new_email = serializers.EmailField(
        help_text="Nuevo email para el usuario"
    )
    
    def validate_new_email(self, value):
        """
        Valida que el nuevo email no esté en uso.
        
        Args:
            value (str): Nuevo email a validar
            
        Returns:
            str: Email validado
            
        Raises:
            ValidationError: Si el email ya está registrado
        """
        if Users.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email ya registrado")
        return value


class UserSearchSerializer(serializers.Serializer):
    """
    Serializer para búsqueda de usuarios.
    
    Permite buscar usuarios por diferentes criterios con un tipo
    de búsqueda específico.
    """
    
    query = serializers.CharField(
        max_length=100,
        help_text="Término de búsqueda"
    )
    search_type = serializers.ChoiceField(
        choices=[('username', 'Username'), ('name', 'Nombre'), ('email', 'Email')], 
        default='username',
        help_text="Tipo de búsqueda a realizar"
    )


class ProfilePhotoSerializer(serializers.Serializer):
    """
    Serializer para subida de foto de perfil.
    
    Valida que la imagen no exceda el tamaño máximo permitido.
    """
    
    photo = serializers.ImageField(
        help_text="Imagen de perfil del usuario"
    )
    
    def validate_photo(self, value):
        """
        Valida el tamaño de la imagen de perfil.
        
        Args:
            value (ImageField): Imagen a validar
            
        Returns:
            ImageField: Imagen validada
            
        Raises:
            ValidationError: Si la imagen excede el tamaño máximo
        """
        # Límite de 5MB para imágenes de perfil
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("La imagen no puede ser mayor a 5MB")
        return value


class LoginWithCodeSerializer(serializers.Serializer):
    """
    Serializer para autenticación con código de verificación.
    
    Permite el login usando un código de 6 dígitos en lugar de contraseña,
    proporcionando una alternativa segura de autenticación.
    
    Validaciones incluidas:
        - Código de 6 dígitos numéricos
        - Usuario existe y está activo
        - Formato correcto de username/email
    """
    
    username = serializers.CharField(
        max_length=255, 
        help_text="Nombre de usuario o email para autenticación"
    )
    code = serializers.CharField(
        max_length=6, 
        min_length=6, 
        help_text="Código de verificación de 6 dígitos"
    )
    
    def validate_code(self, value):
        """
        Valida el formato del código de verificación.
        
        Args:
            value (str): Código a validar
            
        Returns:
            str: Código validado
            
        Raises:
            ValidationError: Si el código no tiene el formato correcto
        """
        if not value.isdigit():
            raise serializers.ValidationError("El código debe contener solo números")
        if len(value) != 6:
            raise serializers.ValidationError("El código debe tener exactamente 6 dígitos")
        return value
    
    def validate_username(self, value):
        """
        Valida que el username no esté vacío.
        
        Args:
            value (str): Username a validar
            
        Returns:
            str: Username validado y limpiado
            
        Raises:
            ValidationError: Si el username está vacío
        """
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre de usuario o email es requerido")
        return value.strip()
    
    def validate(self, attrs):
        """
        Valida las credenciales del usuario para login con código.
        
        Args:
            attrs (dict): Atributos del serializer (username, code)
            
        Returns:
            dict: Atributos con el usuario validado incluido
            
        Raises:
            ValidationError: Si las credenciales son inválidas
        """
        username = attrs.get('username')
        code = attrs.get('code')
        
        # Buscar usuario por username primero, luego por email
        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            try:
                user = Users.objects.get(email=username)
            except Users.DoesNotExist:
                raise serializers.ValidationError({
                    'username': 'No existe un usuario con ese nombre de usuario o email'
                })
        
        # Verificar que la cuenta esté activa
        if not user.is_active:
            raise serializers.ValidationError({
                'username': 'Tu cuenta está desactivada. Contacta al administrador.'
            })
        
        # Agregar el usuario validado a los atributos
        attrs['user'] = user
        return attrs


class RequestLoginCodeSerializer(serializers.Serializer):
    """
    Serializer para solicitar código de login.
    
    Valida que el usuario existe y está activo antes de generar
    y enviar el código de verificación para login.
    """
    
    username = serializers.CharField(
        max_length=255, 
        help_text="Nombre de usuario o email para solicitar código de login"
    )
    
    def validate_username(self, value):
        """
        Valida que el usuario existe y está activo.
        
        Args:
            value (str): Username o email a validar
            
        Returns:
            str: Username validado y limpiado
            
        Raises:
            ValidationError: Si el usuario no existe o está inactivo
        """
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre de usuario o email es requerido")
        
        value = value.strip()
        
        # Verificar que el usuario existe
        try:
            user = Users.objects.get(username=value)
        except Users.DoesNotExist:
            try:
                user = Users.objects.get(email=value)
            except Users.DoesNotExist:
                raise serializers.ValidationError("No existe un usuario con ese nombre de usuario o email")
        
        # Verificar que la cuenta esté activa
        if not user.is_active:
            raise serializers.ValidationError("Tu cuenta está desactivada. Contacta al administrador.")
        
        return value
