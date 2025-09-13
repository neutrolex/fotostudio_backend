"""
Sistema de permisos personalizado para el sistema de fotostudio.

Este módulo define los permisos y roles del sistema, incluyendo:
- Administradores: Acceso completo al sistema
- Empleados: Acceso a módulos específicos
- Usuarios: Acceso limitado a sus propios datos

Autor: Sistema Fotostudio
Fecha: 2025
"""

from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Permiso personalizado para verificar si el usuario es administrador.
    
    Un usuario es considerado administrador si:
    - is_superuser = True
    - is_staff = True
    - Pertenece al modelo Admin
    """
    
    def has_permission(self, request, view):
        """
        Verifica si el usuario tiene permisos de administrador.
        
        Args:
            request: Objeto de solicitud HTTP
            view: Vista que está siendo accedida
            
        Returns:
            bool: True si el usuario es administrador, False en caso contrario
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Verificar si es superusuario
        if request.user.is_superuser and request.user.is_staff:
            return True
        
        # Verificar si existe en el modelo Admin
        try:
            from .models import Admin
            return Admin.objects.filter(
                username=request.user.username,
                is_active=True
            ).exists()
        except:
            return False


class IsEmployeeUser(permissions.BasePermission):
    """
    Permiso personalizado para verificar si el usuario es empleado.
    
    Un usuario es considerado empleado si:
    - is_staff = True (pero no necesariamente superusuario)
    - Tiene permisos específicos de empleado
    """
    
    def has_permission(self, request, view):
        """
        Verifica si el usuario tiene permisos de empleado.
        
        Args:
            request: Objeto de solicitud HTTP
            view: Vista que está siendo accedida
            
        Returns:
            bool: True si el usuario es empleado o administrador, False en caso contrario
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Los administradores también son empleados
        if request.user.is_superuser and request.user.is_staff:
            return True
        
        # Verificar si es empleado (staff pero no superusuario)
        return request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir solo a los propietarios editar sus objetos.
    
    Los usuarios pueden:
    - Leer todos los objetos
    - Editar solo los objetos que les pertenecen
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Verifica si el usuario tiene permisos sobre un objeto específico.
        
        Args:
            request: Objeto de solicitud HTTP
            view: Vista que está siendo accedida
            obj: Objeto sobre el cual se verifica el permiso
            
        Returns:
            bool: True si el usuario tiene permisos, False en caso contrario
        """
        # Permisos de lectura para todos los usuarios autenticados
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Permisos de escritura solo para el propietario
        return obj.created_by == request.user


class IsAdminOrEmployee(permissions.BasePermission):
    """
    Permiso que permite acceso a administradores y empleados.
    """
    
    def has_permission(self, request, view):
        """
        Verifica si el usuario es administrador o empleado.
        
        Args:
            request: Objeto de solicitud HTTP
            view: Vista que está siendo accedida
            
        Returns:
            bool: True si el usuario es admin o empleado, False en caso contrario
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Administradores tienen acceso completo
        if request.user.is_superuser and request.user.is_staff:
            return True
        
        # Empleados tienen acceso limitado
        return request.user.is_staff


class IsAdminOrOwner(permissions.BasePermission):
    """
    Permiso que permite acceso a administradores o al propietario del objeto.
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Verifica si el usuario es administrador o propietario del objeto.
        
        Args:
            request: Objeto de solicitud HTTP
            view: Vista que está siendo accedida
            obj: Objeto sobre el cual se verifica el permiso
            
        Returns:
            bool: True si el usuario es admin o propietario, False en caso contrario
        """
        # Administradores tienen acceso completo
        if request.user.is_superuser and request.user.is_staff:
            return True
        
        # Propietarios pueden acceder a sus objetos
        return obj.created_by == request.user


class CanManageClients(permissions.BasePermission):
    """
    Permiso específico para gestión de clientes.
    
    Permite:
    - Administradores: Acceso completo
    - Empleados: Acceso completo
    - Usuarios regulares: Solo lectura
    """
    
    def has_permission(self, request, view):
        """
        Verifica si el usuario puede gestionar clientes.
        
        Args:
            request: Objeto de solicitud HTTP
            view: Vista que está siendo accedida
            
        Returns:
            bool: True si el usuario puede gestionar clientes, False en caso contrario
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Administradores y empleados tienen acceso completo
        if request.user.is_staff:
            return True
        
        # Usuarios regulares solo pueden leer
        return request.method in permissions.SAFE_METHODS


class CanManageOrders(permissions.BasePermission):
    """
    Permiso específico para gestión de pedidos.
    
    Permite:
    - Administradores: Acceso completo
    - Empleados: Acceso completo
    - Usuarios regulares: Solo lectura
    """
    
    def has_permission(self, request, view):
        """
        Verifica si el usuario puede gestionar pedidos.
        
        Args:
            request: Objeto de solicitud HTTP
            view: Vista que está siendo accedida
            
        Returns:
            bool: True si el usuario puede gestionar pedidos, False en caso contrario
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Administradores y empleados tienen acceso completo
        if request.user.is_staff:
            return True
        
        # Usuarios regulares solo pueden leer
        return request.method in permissions.SAFE_METHODS


class CanManageInventory(permissions.BasePermission):
    """
    Permiso específico para gestión de inventario.
    
    Permite:
    - Administradores: Acceso completo
    - Empleados: Acceso completo
    - Usuarios regulares: Solo lectura
    """
    
    def has_permission(self, request, view):
        """
        Verifica si el usuario puede gestionar inventario.
        
        Args:
            request: Objeto de solicitud HTTP
            view: Vista que está siendo accedida
            
        Returns:
            bool: True si el usuario puede gestionar inventario, False en caso contrario
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Administradores y empleados tienen acceso completo
        if request.user.is_staff:
            return True
        
        # Usuarios regulares solo pueden leer
        return request.method in permissions.SAFE_METHODS


class CanManageProduction(permissions.BasePermission):
    """
    Permiso específico para gestión de producción.
    
    Permite:
    - Administradores: Acceso completo
    - Empleados: Acceso completo
    - Usuarios regulares: Solo lectura
    """
    
    def has_permission(self, request, view):
        """
        Verifica si el usuario puede gestionar producción.
        
        Args:
            request: Objeto de solicitud HTTP
            view: Vista que está siendo accedida
            
        Returns:
            bool: True si el usuario puede gestionar producción, False en caso contrario
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Administradores y empleados tienen acceso completo
        if request.user.is_staff:
            return True
        
        # Usuarios regulares solo pueden leer
        return request.method in permissions.SAFE_METHODS


class CanManageContracts(permissions.BasePermission):
    """
    Permiso específico para gestión de contratos.
    
    Permite:
    - Administradores: Acceso completo
    - Empleados: Acceso completo
    - Usuarios regulares: Solo lectura
    """
    
    def has_permission(self, request, view):
        """
        Verifica si el usuario puede gestionar contratos.
        
        Args:
            request: Objeto de solicitud HTTP
            view: Vista que está siendo accedida
            
        Returns:
            bool: True si el usuario puede gestionar contratos, False en caso contrario
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Administradores y empleados tienen acceso completo
        if request.user.is_staff:
            return True
        
        # Usuarios regulares solo pueden leer
        return request.method in permissions.SAFE_METHODS


class CanManageAgenda(permissions.BasePermission):
    """
    Permiso específico para gestión de agenda.
    
    Permite:
    - Administradores: Acceso completo
    - Empleados: Acceso completo
    - Usuarios regulares: Solo lectura
    """
    
    def has_permission(self, request, view):
        """
        Verifica si el usuario puede gestionar agenda.
        
        Args:
            request: Objeto de solicitud HTTP
            view: Vista que está siendo accedida
            
        Returns:
            bool: True si el usuario puede gestionar agenda, False en caso contrario
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Administradores y empleados tienen acceso completo
        if request.user.is_staff:
            return True
        
        # Usuarios regulares solo pueden leer
        return request.method in permissions.SAFE_METHODS


class CanViewReports(permissions.BasePermission):
    """
    Permiso específico para visualización de reportes.
    
    Permite:
    - Administradores: Acceso completo
    - Empleados: Acceso completo
    - Usuarios regulares: Sin acceso
    """
    
    def has_permission(self, request, view):
        """
        Verifica si el usuario puede ver reportes.
        
        Args:
            request: Objeto de solicitud HTTP
            view: Vista que está siendo accedida
            
        Returns:
            bool: True si el usuario puede ver reportes, False en caso contrario
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Solo administradores y empleados pueden ver reportes
        return request.user.is_staff


class CanManageUsers(permissions.BasePermission):
    """
    Permiso específico para gestión de usuarios.
    
    Permite:
    - Administradores: Acceso completo
    - Empleados: Sin acceso
    - Usuarios regulares: Sin acceso
    """
    
    def has_permission(self, request, view):
        """
        Verifica si el usuario puede gestionar otros usuarios.
        
        Args:
            request: Objeto de solicitud HTTP
            view: Vista que está siendo accedida
            
        Returns:
            bool: True si el usuario puede gestionar usuarios, False en caso contrario
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Solo administradores pueden gestionar usuarios
        return request.user.is_superuser and request.user.is_staff


# Permisos predefinidos para facilitar el uso
ADMIN_ONLY = [IsAdminUser]
EMPLOYEE_OR_ADMIN = [IsAdminOrEmployee]
AUTHENTICATED_ONLY = [permissions.IsAuthenticated]
CLIENT_MANAGEMENT = [CanManageClients]
ORDER_MANAGEMENT = [CanManageOrders]
INVENTORY_MANAGEMENT = [CanManageInventory]
PRODUCTION_MANAGEMENT = [CanManageProduction]
REPORT_ACCESS = [CanViewReports]
USER_MANAGEMENT = [CanManageUsers]

