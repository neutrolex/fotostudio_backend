# 🏢 FotoStudio Backend - Configuración Multi-Tenant

## 📋 Descripción General

El backend de FotoStudio ha sido configurado con una arquitectura **multi-tenant** basada en **schemas de base de datos**. Esta implementación permite que múltiples empresas de fotografía utilicen la misma aplicación de forma completamente aislada.

## 🏗️ Arquitectura Multi-Tenant

### Estrategia Implementada: Schema-Based Multi-Tenancy

- **Separación por Schemas**: Cada tenant (empresa) tiene su propio schema en PostgreSQL
- **Aislamiento Completo**: Los datos de cada tenant están completamente separados
- **Escalabilidad**: Fácil agregar nuevos tenants sin afectar los existentes
- **Mantenimiento**: Backup y restauración independiente por tenant

## 🔧 Componentes Implementados

### 1. App `tenants`
- **Modelo Tenant**: Información del negocio (nombre, tipo, plan de suscripción)
- **Modelo Domain**: Dominios/subdominios para cada tenant
- **Admin Personalizado**: Gestión de tenants desde Django Admin
- **APIs REST**: Endpoints para gestión de tenants

### 2. Middleware Personalizado
- **CustomTenantMiddleware**: Manejo automático de tenants por dominio
- **TenantLoggingMiddleware**: Logging específico por tenant
- **TenantSecurityMiddleware**: Validaciones de seguridad por tenant

### 3. Configuración de Base de Datos
- **PostgreSQL con django-tenants**: Soporte nativo para multi-tenancy
- **Router de Tenants**: Enrutamiento automático de queries
- **Migraciones por Schema**: Cada tenant tiene sus propias migraciones

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.8+
- PostgreSQL 12+
- Redis (opcional, para cache)

### 1. Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### 2. Configuración de Base de Datos
```bash
# Crear base de datos PostgreSQL
createdb fotostudio_dev

# Configurar variables de entorno
cp env.example .env
# Editar .env con tus configuraciones
```

### 3. Migraciones Iniciales
```bash
# Migrar el schema público (para tenants)
python manage.py migrate_schemas --shared

# Crear un tenant de ejemplo
python manage.py shell
>>> from tenants.models import Tenant, Domain
>>> tenant = Tenant.objects.create(name="Empresa Demo", email="demo@empresa.com")
>>> Domain.objects.create(domain="demo.localhost", tenant=tenant, is_primary=True)
```

### 4. Migrar Schemas de Tenants
```bash
# Migrar todos los schemas de tenants
python manage.py migrate_schemas
```

## 🌐 Configuración de Dominios

### Desarrollo Local
Para desarrollo local, puedes usar subdominios con `localhost`:

```
demo.localhost:8000     # Tenant "Empresa Demo"
empresa1.localhost:8000 # Tenant "Empresa 1"
empresa2.localhost:8000 # Tenant "Empresa 2"
```

### Configuración de Hosts (Windows)
Editar `C:\Windows\System32\drivers\etc\hosts`:
```
127.0.0.1 demo.localhost
127.0.0.1 empresa1.localhost
127.0.0.1 empresa2.localhost
```

### Configuración de Hosts (Linux/Mac)
Editar `/etc/hosts`:
```
127.0.0.1 demo.localhost
127.0.0.1 empresa1.localhost
127.0.0.1 empresa2.localhost
```

## 📊 Flujo de Funcionamiento

1. **Request Incoming**: Cliente hace request a subdominio (ej: empresa1.fotostudio.com)
2. **Tenant Resolution**: Middleware identifica el tenant por dominio
3. **Schema Switch**: Django cambia automáticamente al schema del tenant
4. **Data Isolation**: Todas las queries se ejecutan en el schema correcto
5. **Response**: Respuesta con datos específicos del tenant

## 🔌 APIs Multi-Tenant

### Gestión de Tenants
```
GET    /api/tenants/                    # Listar tenants (admin)
GET    /api/tenants/{id}/               # Detalle tenant
GET    /api/tenants/current/            # Tenant actual
```

### Todas las APIs de Negocio son Multi-Tenant
- Cada endpoint automáticamente filtra por tenant
- Datos completamente aislados entre tenants
- No es necesario agregar filtros manuales

## 🛠️ Comandos de Gestión

### Crear Nuevo Tenant
```bash
python manage.py shell
>>> from tenants.models import Tenant, Domain
>>> tenant = Tenant.objects.create(
...     name="Nueva Empresa",
...     email="contacto@nuevaempresa.com",
...     business_type="fotografia"
... )
>>> Domain.objects.create(
...     domain="nuevaempresa.localhost",
...     tenant=tenant,
...     is_primary=True
... )
```

### Migrar Schema de Tenant Específico
```bash
python manage.py migrate_schemas --tenant=nuevaempresa
```

### Backup de Tenant Específico
```bash
python manage.py dumpdata --schema=nuevaempresa > backup_nuevaempresa.json
```

## 🔒 Seguridad Multi-Tenant

### Aislamiento de Datos
- **Imposible acceso cruzado**: Un tenant no puede acceder a datos de otro
- **Validación automática**: Middleware valida que el tenant esté activo
- **Logging por tenant**: Todos los logs incluyen información del tenant

### Validaciones Implementadas
- Verificación de tenant activo
- Validación de límites por plan de suscripción
- Logging de intentos de acceso no autorizados

## 📈 Ventajas de la Implementación

✅ **Aislamiento Completo**: Datos de cada tenant completamente separados
✅ **Escalabilidad**: Fácil agregar nuevos tenants
✅ **Mantenimiento**: Backup/restore independiente por tenant
✅ **Seguridad**: Imposible acceso cruzado entre tenants
✅ **Performance**: Queries optimizadas por schema
✅ **Flexibilidad**: Cada tenant puede tener configuraciones diferentes

## 🐛 Troubleshooting

### Error: "Tenant not found"
- Verificar que el dominio esté configurado en la tabla `tenants_domain`
- Verificar que el tenant esté activo (`is_active=True`)

### Error: "Schema does not exist"
- Ejecutar migraciones para el tenant: `python manage.py migrate_schemas --tenant=nombre_tenant`

### Error: "Permission denied"
- Verificar que el usuario de PostgreSQL tenga permisos para crear schemas
- Verificar configuración de `ALLOWED_HOSTS` en settings

## 📚 Documentación Adicional

- [Django Tenants Documentation](https://django-tenants.readthedocs.io/)
- [PostgreSQL Schemas](https://www.postgresql.org/docs/current/ddl-schemas.html)
- [Django Multi-Tenant Best Practices](https://books.agiliq.com/projects/django-multi-tenant/en/latest/)

## 🤝 Soporte

Para soporte técnico o consultas sobre la implementación multi-tenant:
- Revisar logs en `logs/django.log`
- Verificar configuración de base de datos
- Consultar documentación de django-tenants

---

**Desarrollado con ❤️ para optimizar la gestión multi-tenant de negocios fotográficos.**

---

## 📌 Alineación con plan acelerado (3 días) y salas

- Sala responsable principal: **Sala 4 (Reportes, Configuración y Tenants)**.
- Día 1: Resolver tenant por subdominio y fallback `X-Tenant-ID` (solo DEV). Ajustar `ALLOWED_HOSTS` y `.env.example`.
- Día 2: Añadir configuración mínima (parámetros del sistema) y auditoría básica de eventos. Reportes simples en CSV (finanzas/inventario) por tenant.
- Día 3: Enforcer multi-tenant en todas las queries (filtros por `tenant`) e integración con JWT (claims con `tenant`). Tests críticos y actualización de Swagger.

Nota: Las Salas 1, 2 y 3 deben consumir el contexto de tenant y aplicar filtros de aislamiento en sus endpoints y servicios.

