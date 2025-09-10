# 🔐 SALA 1: USUARIOS Y AUTENTICACIÓN

## 👥 **EQUIPO RESPONSABLE**
- **Líder**: Desarrollador Senior Backend
- **Miembros**: 2 desarrolladores especializados en seguridad
- **Rol**: Equipo de Seguridad y Autenticación

## 🎯 **OBJETIVOS PRINCIPALES**
- Implementar sistema de autenticación robusto con JWT
- Crear gestión completa de usuarios con perfiles
- Establecer sistema de permisos granulares
- Desarrollar middleware de autenticación personalizado

## 📋 **MÓDULOS A DESARROLLAR**

### **1. App `users`**
- Modelo User personalizado con AbstractUser
- Serializers para CRUD y autenticación
- Views con DRF (ListCreate, RetrieveUpdateDestroy)
- URLs configuradas con namespace
- Admin personalizado para gestión

### **2. Autenticación JWT**
- Login con tokens JWT
- Logout con invalidación de tokens
- Refresh tokens automático
- Middleware de validación de tokens

### **3. Perfil de Usuario**
- CRUD completo de perfil
- Subida y actualización de avatar
- Cambio de contraseña seguro
- Validaciones de datos personales

### **4. Permisos y Roles**
- Sistema de permisos personalizado
- Roles de usuario (admin, staff, user)
- Permisos granulares por endpoint
- Middleware de autorización

## ✅ Plan de 3 días (Sala 1 - Usuarios y Autenticación)

Estado actual:
- [hecho] App `users` creada, migraciones iniciales del proyecto ejecutadas.
- [pendiente] Endpoints JWT, perfiles, permisos y middleware.

Día 1 (Base mínima funcional):
- [ ] Activar DRF y SimpleJWT en settings.
- [ ] Endpoints: `POST /api/auth/login/`, `POST /api/auth/refresh/`.
- [ ] `GET /api/auth/profile/` (solo lectura) para usuario autenticado.
- [ ] Swagger: describir endpoints de auth.

Día 2 (CRUD y seguridad):
- [ ] `PUT /api/auth/profile/` y `POST /api/auth/change-password/`.
- [ ] `GET/POST /api/users/`, `GET/PUT/DELETE /api/users/{id}/` (solo admin).
- [ ] Permisos por rol (admin/staff/user) y tests de permisos.

Día 3 (Harden y multi-tenant):
- [ ] Middleware JWT que inyecte/valide `tenant` en claims.
- [ ] Validaciones de seguridad (password/email) y rate limiting de login.
- [ ] Tests de integración de autenticación y actualización de Swagger.

## 🔧 **ESTRUCTURA DE CARPETAS**

```
apps/users/
├── __init__.py
├── models.py              # Modelo User personalizado
├── serializers.py         # Serializers para DRF
├── views.py              # Views con DRF
├── urls.py               # URLs de la app
├── admin.py              # Admin personalizado
├── permissions.py        # Permisos personalizados
├── signals.py            # Signals para eventos
├── services.py           # Lógica de negocio
├── middleware.py         # Middleware personalizado
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_views.py
    ├── test_serializers.py
    ├── test_services.py
    └── test_middleware.py
```

## 🌐 **ENDPOINTS A IMPLEMENTAR**

### **Autenticación**
```
POST /api/auth/login/          # Login con JWT
POST /api/auth/logout/         # Logout
POST /api/auth/refresh/        # Refresh token
```

### **Perfil de Usuario**
```
GET  /api/auth/profile/        # Obtener perfil
PUT  /api/auth/profile/        # Actualizar perfil
POST /api/auth/change-password/ # Cambiar contraseña
```

### **Gestión de Usuarios (Admin)**
```
GET    /api/users/             # Listar usuarios
POST   /api/users/             # Crear usuario
GET    /api/users/{id}/        # Detalle usuario
PUT    /api/users/{id}/        # Actualizar usuario
DELETE /api/users/{id}/        # Eliminar usuario
```

## 🧪 **TESTS OBLIGATORIOS**

### **Tests Unitarios**
- [ ] Tests de modelo User
- [ ] Tests de serializers
- [ ] Tests de views
- [ ] Tests de servicios
- [ ] Tests de middleware

### **Tests de Integración**
- [ ] Tests de autenticación completa
- [ ] Tests de permisos
- [ ] Tests con Postman
- [ ] Tests de endpoints

### **Cobertura Mínima**
- **90%** en código de producción
- **100%** en lógica de autenticación
- **100%** en validaciones de seguridad

## 📚 **DOCUMENTACIÓN REQUERIDA**

### **Swagger/OpenAPI**
- [ ] Documentación automática de todas las APIs
- [ ] Ejemplos de uso para cada endpoint
- [ ] Esquemas de datos detallados
- [ ] Códigos de error documentados
- [ ] Autenticación documentada

### **Documentación Técnica**
- [ ] README de la app
- [ ] Guías de instalación
- [ ] Ejemplos de uso
- [ ] Documentación de seguridad

## 🔒 **REQUISITOS DE SEGURIDAD**

### **Autenticación**
- [ ] JWT con refresh automático
- [ ] Tokens con expiración configurable
- [ ] Invalidación de tokens en logout
- [ ] Validación de tokens en middleware

### **Validación**
- [ ] Validación de contraseñas seguras
- [ ] Validación de emails con regex
- [ ] Sanitización de inputs
- [ ] Rate limiting para login

### **Permisos**
- [ ] Permisos granulares por endpoint
- [ ] Roles de usuario bien definidos
- [ ] Middleware de autorización
- [ ] Validación de permisos en views

## 🏗️ Contexto Multi-tenant (MySQL)

- Enfoque conceptual: database-based en MySQL (una base de datos/schema por tenant).
- Resolución de tenant sugerida por subdominio o cabecera `X-Tenant-ID`.
- Autenticación/Autorización deben validar que el usuario pertenece al tenant activo.
- No implementar lógica aquí; estos lineamientos guían al equipo para futuras fases.

## 🔄 **DEPENDENCIAS**

### **Hacia Otros Equipos**
- **Proporciona**: Sistema de autenticación JWT
- **Proporciona**: Modelo User para otras apps
- **Proporciona**: Sistema de permisos
- **Proporciona**: Middleware de autenticación

### **De Otros Equipos**
- **Ninguna**: Trabajo completamente independiente
- **Nota**: Otros equipos dependerán de este trabajo

## 📞 **CONTACTO Y SOPORTE**

- **Líder del equipo**: [Nombre del líder]
- **Email**: [email@empresa.com]
- **Slack**: #sala-1-usuarios
- **Horario de trabajo**: 8:00 AM - 6:00 PM

## 🎯 **CRITERIOS DE ACEPTACIÓN**

### **Funcionalidad**
- [ ] Login/logout funcionando correctamente
- [ ] Perfil de usuario editable
- [ ] Cambio de contraseña seguro
- [ ] Gestión de usuarios para admin
- [ ] Sistema de permisos funcional

### **Calidad**
- [ ] Tests con 90% coverage
- [ ] Documentación completa
- [ ] Código limpio y documentado
- [ ] APIs documentadas con Swagger
- [ ] Seguridad validada

### **Performance**
- [ ] Autenticación rápida (< 200ms)
- [ ] Tokens JWT eficientes
- [ ] Queries optimizadas
- [ ] Middleware sin overhead

---
**Responsable**: Sala 1 - Usuarios y Autenticación
