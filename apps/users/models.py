"""
Modelos de la aplicación de usuarios para el sistema de fotostudio.

Este módulo define los modelos principales para la gestión de usuarios,
incluyendo usuarios regulares, administradores, tipos de documentos y
códigos de verificación.

Autor: Sistema Fotostudio
Fecha: 2025
"""

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class RegularUserManager(models.Manager):
    """
    Manager personalizado que excluye superusuarios de las consultas regulares.
    
    Este manager se utiliza para filtrar automáticamente los superusuarios
    de las consultas normales, manteniendo la separación entre usuarios
    regulares y administradores del sistema.
    
    Métodos:
        get_queryset(): Retorna un QuerySet filtrado sin superusuarios
    """
    
    def get_queryset(self):
        """
        Retorna un QuerySet que excluye superusuarios.
        
        Returns:
            QuerySet: QuerySet filtrado sin usuarios con is_superuser=True
        """
        return super().get_queryset().filter(is_superuser=False)


class UsersManager(BaseUserManager):
    """
    Manager personalizado para el modelo Users que implementa métodos requeridos
    por Django para la autenticación.
    """
    
    def get_by_natural_key(self, username):
        """
        Permite la autenticación por nombre de usuario.
        
        Args:
            username (str): Nombre de usuario a buscar
            
        Returns:
            Users: Usuario encontrado
        """
        return self.get(username=username)
    
    def create_superuser(self, username, email, password, **extra_fields):
        """
        Crea un superusuario con los campos requeridos.
        
        Args:
            username (str): Nombre de usuario
            email (str): Email del usuario
            password (str): Contraseña del usuario
            **extra_fields: Campos adicionales
            
        Returns:
            Users: Usuario superusuario creado
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('tenant_id', 1)  # Tenant por defecto
        extra_fields.setdefault('name', username)
        extra_fields.setdefault('paternal_lastname', 'Admin')
        extra_fields.setdefault('maternal_lastname', 'User')
        extra_fields.setdefault('document_number', f'ADMIN_{username}')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
            
        return self._create_user(username, email, password, **extra_fields)
    
    def create_user(self, username, email, password, **extra_fields):
        """
        Crea un usuario regular.
        
        Args:
            username (str): Nombre de usuario
            email (str): Email del usuario
            password (str): Contraseña del usuario
            **extra_fields: Campos adicionales
            
        Returns:
            Users: Usuario creado
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        
        return self._create_user(username, email, password, **extra_fields)
    
    def _create_user(self, username, email, password, **extra_fields):
        """
        Método interno para crear usuarios.
        
        Args:
            username (str): Nombre de usuario
            email (str): Email del usuario
            password (str): Contraseña del usuario
            **extra_fields: Campos adicionales
            
        Returns:
            Users: Usuario creado
        """
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')
            
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Admin(models.Model):
    """
    Modelo separado para administradores del sistema.
    
    Este modelo maneja los administradores de forma independiente a los
    usuarios regulares, proporcionando una separación clara de roles y
    permisos en el sistema.
    
    Atributos:
        id (AutoField): Clave primaria autoincremental
        username (CharField): Nombre de usuario único para el admin
        email (EmailField): Email único del administrador
        password (CharField): Contraseña hasheada del administrador
        first_name (CharField): Nombre del administrador
        last_name (CharField): Apellido del administrador
        is_active (BooleanField): Indica si la cuenta está activa
        is_staff (BooleanField): Indica si tiene permisos de staff
        date_joined (DateTimeField): Fecha de registro automática
        last_login (DateTimeField): Último acceso al sistema
    """
    
    # Campos principales del administrador
    id = models.AutoField(primary_key=True)
    username = models.CharField(
        unique=True, 
        max_length=150,
        help_text="Nombre de usuario único para el administrador"
    )
    email = models.EmailField(
        unique=True,
        help_text="Dirección de correo electrónico única"
    )
    password = models.CharField(
        max_length=150,
        help_text="Contraseña hasheada del administrador"
    )
    first_name = models.CharField(
        max_length=150, 
        blank=True,
        help_text="Nombre del administrador"
    )
    last_name = models.CharField(
        max_length=150, 
        blank=True,
        help_text="Apellido del administrador"
    )
    
    # Campos de estado y permisos
    is_active = models.BooleanField(
        default=True,
        help_text="Indica si la cuenta del administrador está activa"
    )
    is_staff = models.BooleanField(
        default=True,
        help_text="Indica si el administrador tiene permisos de staff"
    )
    
    # Campos de auditoría
    date_joined = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de registro del administrador"
    )
    last_login = models.DateTimeField(
        blank=True, 
        null=True,
        help_text="Fecha y hora del último acceso al sistema"
    )
    
    class Meta:
        db_table = 'admins'
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'
        ordering = ['-date_joined']
    
    def __str__(self):
        """
        Representación en string del administrador.
        
        Returns:
            str: Nombre completo o username si no hay nombre
        """
        return f"{self.first_name} {self.last_name}" if self.first_name else self.username


class DocumentTypes(models.Model):
    """
    Modelo para tipos de documentos de identidad.
    
    Este modelo almacena los diferentes tipos de documentos que pueden
    usar los usuarios para identificarse (DNI, Pasaporte, etc.).
    
    Atributos:
        id (AutoField): Clave primaria autoincremental
        name (CharField): Nombre del tipo de documento
    """
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        help_text="Nombre del tipo de documento (ej: DNI, Pasaporte, etc.)"
    )

    class Meta:
        db_table = 'document_types'
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de Documentos'
        ordering = ['name']

    def __str__(self):
        """
        Representación en string del tipo de documento.
        
        Returns:
            str: Nombre del tipo de documento
        """
        return self.name


class Users(AbstractUser):
    """
    Modelo principal de usuarios del sistema.
    
    Extiende AbstractUser de Django para proporcionar funcionalidad
    completa de autenticación con campos personalizados específicos
    para el sistema de fotostudio.
    
    Este modelo maneja tanto usuarios regulares como superusuarios,
    proporcionando un sistema de autenticación robusto con soporte
    para multi-tenancy.
    
    Atributos principales:
        tenant_id (IntegerField): ID del tenant para multi-tenancy
        document_number (CharField): Número de documento único
        name (CharField): Nombre del usuario
        paternal_lastname (CharField): Apellido paterno
        maternal_lastname (CharField): Apellido materno
        email (CharField): Email único del usuario
        phone (CharField): Número de teléfono
        photo_url (CharField): URL de la foto de perfil
    """
    
    # Clave primaria personalizada
    id = models.AutoField(primary_key=True)
    
    # Campo para multi-tenancy
    tenant_id = models.IntegerField(
        help_text="ID del tenant para soporte multi-tenancy"
    )
    
    # Managers personalizados
    objects = UsersManager()  # Manager personalizado con métodos de autenticación
    
    # Información personal del usuario
    document_number = models.CharField(
        unique=True, 
        max_length=255,
        help_text="Número de documento de identidad único"
    )
    name = models.CharField(
        max_length=255,
        help_text="Nombre del usuario"
    )
    paternal_lastname = models.CharField(
        max_length=255,
        help_text="Apellido paterno del usuario"
    )
    maternal_lastname = models.CharField(
        max_length=255,
        help_text="Apellido materno del usuario"
    )
    
    # Información de contacto
    email = models.CharField(
        unique=True, 
        max_length=255,
        help_text="Dirección de correo electrónico única"
    )
    phone = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Número de teléfono del usuario"
    )
    
    # Información de perfil
    photo_url = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        help_text="URL de la foto de perfil del usuario"
    )
    sex = models.CharField(
        max_length=1, 
        blank=True, 
        null=True,
        choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')],
        help_text="Sexo del usuario"
    )
    
    # Campos de autenticación personalizados
    username = models.CharField(
        unique=True, 
        max_length=150,
        help_text="Nombre de usuario único para login"
    )
    password_change = models.BooleanField(
        default=False,
        help_text="Indica si el usuario debe cambiar su contraseña"
    )
    
    # Campos de estado y sesión
    last_session = models.DateTimeField(
        auto_now=True,
        help_text="Fecha y hora de la última sesión activa"
    )
    account_statement = models.CharField(
        max_length=1, 
        choices=[('A', 'Activo'), ('I', 'Inactivo')], 
        default='A',
        help_text="Estado de la cuenta del usuario"
    )
    
    # Campos de verificación
    email_verified_at = models.DateTimeField(
        blank=True, 
        null=True,
        help_text="Fecha y hora de verificación del email"
    )
    
    # Campos de referencia
    document_type_id = models.IntegerField(
        blank=True, 
        null=True,
        help_text="ID del tipo de documento del usuario"
    )
    country_id = models.IntegerField(
        blank=True, 
        null=True,
        help_text="ID del país del usuario"
    )
    
    # Campos de seguridad
    remember_token = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Token para recordar sesión del usuario"
    )
    
    # Campos de auditoría
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de creación del usuario"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Fecha y hora de última actualización"
    )
    deleted_at = models.DateTimeField(
        blank=True, 
        null=True,
        help_text="Fecha y hora de eliminación lógica (soft delete)"
    )
    last_login = models.DateTimeField(
        blank=True, 
        null=True,
        help_text="Fecha y hora del último login"
    )
    
    # Campos de permisos (heredados de AbstractUser)
    is_superuser = models.BooleanField(
        default=False,
        help_text="Indica si es superusuario del sistema"
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Indica si tiene permisos de staff"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indica si la cuenta está activa"
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de registro del usuario"
    )

    class Meta:
        db_table = 'users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
            models.Index(fields=['document_number']),
            models.Index(fields=['tenant_id']),
        ]

    def __str__(self):
        """
        Representación en string del usuario.
        
        Returns:
            str: Nombre completo del usuario
        """
        return f"{self.name} {self.paternal_lastname}"
    
    @property
    def full_name(self):
        """
        Retorna el nombre completo del usuario.
        
        Returns:
            str: Nombre completo (nombre + apellidos)
        """
        return f"{self.name} {self.paternal_lastname} {self.maternal_lastname}".strip()
    
    @property
    def is_email_verified(self):
        """
        Verifica si el email del usuario está verificado.
        
        Returns:
            bool: True si el email está verificado, False en caso contrario
        """
        return self.email_verified_at is not None


class UsersVerificationCode(models.Model):
    """
    Modelo para códigos de verificación de usuarios.
    
    Este modelo almacena códigos de verificación temporales para
    diversas operaciones como cambio de email, reset de contraseña,
    login con código, etc.
    
    Características de seguridad:
    - Códigos de un solo uso
    - Expiración automática
    - Sistema de intentos fallidos con bloqueo
    - Almacenamiento temporal de datos sensibles
    
    Atributos:
        user_id (BigIntegerField): ID del usuario propietario del código
        code (CharField): Código de verificación
        expires_at (DateTimeField): Fecha y hora de expiración
        failed_attempts (IntegerField): Número de intentos fallidos
        locked_until (DateTimeField): Fecha hasta la cual está bloqueado
        temp_email (CharField): Email temporal para cambios de email
    """
    
    # Clave primaria
    id = models.AutoField(primary_key=True)
    
    # Relación con usuario
    user_id = models.BigIntegerField(
        blank=True, 
        null=True,
        help_text="ID del usuario propietario del código de verificación"
    )
    
    # Código de verificación
    code = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        help_text="Código de verificación generado"
    )
    
    # Control de expiración
    expires_at = models.DateTimeField(
        help_text="Fecha y hora de expiración del código"
    )
    
    # Sistema de seguridad
    failed_attempts = models.IntegerField(
        default=0,
        help_text="Número de intentos fallidos de verificación"
    )
    locked_until = models.DateTimeField(
        blank=True, 
        null=True,
        help_text="Fecha hasta la cual el código está bloqueado por intentos fallidos"
    )
    
    # Almacenamiento temporal de datos
    temp_email = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        help_text="Email temporal almacenado para cambios de email"
    )
    
    # Campos de auditoría
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de creación del código"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Fecha y hora de última actualización"
    )

    class Meta:
        db_table = 'users_verification_code'
        verbose_name = 'Código de Verificación'
        verbose_name_plural = 'Códigos de Verificación'
        unique_together = (('user_id',),)  # Un código por usuario
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['code']),
        ]
    
    def __str__(self):
        """
        Representación en string del código de verificación.
        
        Returns:
            str: Descripción del código con su estado
        """
        status = "Expirado" if self.is_expired else "Válido"
        return f"Código {self.code} - Usuario {self.user_id} - {status}"
    
    @property
    def is_expired(self):
        """
        Verifica si el código ha expirado.
        
        Returns:
            bool: True si el código ha expirado, False en caso contrario
        """
        from django.utils import timezone
        return self.expires_at <= timezone.now()
    
    @property
    def is_locked(self):
        """
        Verifica si el código está bloqueado por intentos fallidos.
        
        Returns:
            bool: True si está bloqueado, False en caso contrario
        """
        from django.utils import timezone
        return (self.locked_until is not None and 
                self.locked_until > timezone.now())
    
    @property
    def remaining_attempts(self):
        """
        Calcula los intentos restantes antes del bloqueo.
        
        Returns:
            int: Número de intentos restantes (máximo 3)
        """
        return max(0, 3 - self.failed_attempts)