Módulos Identificados del Sistema:

    1. Dashboard            - Panel de control centralizado                 - SALA-2
    2. Pedidos              - Gestión de órdenes de trabajo                 - SALA-2
    3. Clientes             - Gestión de clientes particulares y colegios   - SALA-2
    4. Contratos            - Gestión de contratos con colegios             - SALA-2
    5. Inventario           - Control de 7 categorías de materiales         - SALA-3
    6. Orden de Producción  - Control de producción y mermas                - SALA-3
    7. Productos Terminados - Gestión de cuadros y productos finales        - SALA-3
    7. Agenda               - Programación de citas y entregas              - SALA-2
    8. Reportes             - Análisis financiero y de producción           - SALA-4
    9. Configuración        - Parámetros del sistema                        - SALA-4
    10. Perfil de Usuario   - FALTA IMPLEMENTAR                             - SALA-1
    11. tenants             - Falta por desarrollar                         - SALA-4
ESTRUCTURA IDEAL DEL PROYECTO DJANGO CON MULTI-TENANT:

fotostudio_backend/
├── manage.py
├── requirements.txt
├── env.example                         # Configuración de entorno
├── .gitignore
├── README.md
├── fotostudio/                         # Configuración principal
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py                     # Configuración base con multi-tenant
│   │   ├── development.py              # Configuración desarrollo
│   │   ├── production.py               # Configuración producción
│   │   └── testing.py                  # Configuración testing
│   ├── urls.py                         # URLs principales
│   ├── wsgi.py
│   └── asgi.py
├── tenants/                            # App de multi-tenancy
│   ├── __init__.py
│   ├── models.py                       # Modelos Tenant y Domain
│   ├── admin.py                        # Admin de tenants
│   ├── views.py                        # Vistas de tenants
│   ├── serializers.py                  # Serializers de tenants
│   ├── urls.py                         # URLs de tenants
│   └── tests.py                        # Tests de tenants
├── middlewares/                        # Middlewares personalizados
│   ├── __init__.py
│   ├── tenant_middleware.py            # Middleware multi-tenant
│   ├── authentication.py               # Middleware de autenticación
│   ├── logging.py                      # Middleware de logging
│   └── cors.py                         # Middleware CORS
├── apps/                               # Apps de negocio
│   ├── __init__.py
│   ├── users/                          # Gestión de usuarios
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── permissions.py
│   │   ├── signals.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_models.py
│   │       ├── test_views.py
│   │       └── test_serializers.py
│   ├── tenants/                         # Tenant
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── services.py
│   │   └── tests/
│   ├── orders/                         # Gestión de pedidos
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── services.py
│   │   └── tests/
│   ├── clients/                        # Gestión de clientes
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── tests/
│   ├── contracts/                      # Gestión de contratos
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── tests/
│   ├── inventory/                      # Gestión de inventario
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── services.py
│   │   ├── signals.py
│   │   └── tests/
│   ├── production/                     # Gestión de producción
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── services.py
│   │   └── tests/
│   ├── products/                       # Productos terminados
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── tests/
│   ├── agenda/                         # Gestión de agenda
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── tests/
│   ├── reports/                        # Reportes y análisis
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── services.py
│   │   └── tests/
│   └── dashboard/                      # Dashboard y métricas
│       ├── __init__.py
│       ├── views.py
│       ├── urls.py
│       ├── services.py
│       └── tests/
├── utils/                              # Utilidades compartidas
│   ├── __init__.py
│   ├── permissions.py                  # Permisos personalizados
│   ├── pagination.py                   # Paginación personalizada
│   ├── filters.py                      # Filtros para APIs
│   ├── exceptions.py                   # Excepciones personalizadas
│   ├── validators.py                   # Validadores personalizados
│   └── helpers.py                      # Funciones auxiliares
├── config/                             # Configuraciones
│   ├── __init__.py
│   ├── celery.py                       # Configuración Celery
│   ├── cache.py                        # Configuración cache
│   └── database.py                     # Configuración BD
├── middlewares/                        # Middlewares personalizados
│   ├── __init__.py
│   ├── authentication.py               # Middleware de autenticación
│   ├── logging.py                      # Middleware de logging
│   └── cors.py                         # Middleware CORS
├── docs/                               # Documentación
│   ├── api/                            # Documentación API
│   ├── deployment/                     # Guías de despliegue
│   └── development/                    # Guías de desarrollo
└── tests/                              # Tests de integración
    ├── __init__.py
    ├── conftest.py
    ├── fixtures/
    └── integration/

Función de Cada Módulo
Apps de Negocio:
    -users: Autenticación, perfiles, permisos y gestión de usuarios
    -orders: CRUD de pedidos, estados, cálculos y seguimiento
    -clients: Gestión de clientes particulares y colegios
    -contracts: Contratos con colegios, términos y condiciones
    -inventory: 7 categorías de materiales, stock, alertas y movimientos
    -production: Órdenes de producción, mermas y trazabilidad
    -products: Productos terminados, estados y ubicaciones
    -agenda: Citas, entregas y programación
    -reports: Reportes financieros, análisis y exportación
    -dashboard: Métricas, KPIs y resúmenes ejecutivos

Módulos de Soporte:
    -utils: Funciones compartidas, permisos, paginación y validadores
    -config: Configuraciones de Celery, cache y base de datos
    -middlewares: Autenticación, logging y CORS
    -docs: Documentación API, despliegue y desarrollo

🏢 ARQUITECTURA MULTI-TENANT IMPLEMENTADA

## 🏗️ **CONFIGURACIÓN MULTI-TENANT**

### **Estrategia Implementada: Schema-Based Multi-Tenancy**
- **Separación por Schemas**: Cada tenant tiene su propio schema en PostgreSQL
- **Aislamiento de Datos**: Datos completamente separados entre tenants
- **Escalabilidad**: Fácil agregar nuevos tenants sin afectar existentes
- **Mantenimiento**: Backup y restauración independiente por tenant

Nota (alineación con MySQL): A nivel conceptual, este proyecto operará de forma multi-tenant sobre MySQL con enfoque database-based (una base de datos/schema por tenant). La resolución de tenant se sugiere por subdominio o cabecera y el enrutamiento seleccionará la base de datos del tenant antes de ejecutar consultas. Este documento solo define lineamientos; la implementación se hará en fases de desarrollo.

### **Componentes Multi-Tenant Implementados**

#### **1. App `tenants`**
- **Modelo Tenant**: Información del negocio (nombre, tipo, plan de suscripción)
- **Modelo Domain**: Dominios/subdominios para cada tenant
- **Admin Personalizado**: Gestión de tenants desde Django Admin
- **APIs REST**: Endpoints para gestión de tenants

#### **2. Middleware Personalizado**
- **CustomTenantMiddleware**: Manejo automático de tenants por dominio
- **TenantLoggingMiddleware**: Logging específico por tenant
- **TenantSecurityMiddleware**: Validaciones de seguridad por tenant

#### **3. Configuración de Base de Datos**
- **PostgreSQL con django-tenants**: Soporte nativo para multi-tenancy
- **Router de Tenants**: Enrutamiento automático de queries
- **Migraciones por Schema**: Cada tenant tiene sus propias migraciones

### **Flujo de Funcionamiento Multi-Tenant**

1. **Request Incoming**: Cliente hace request a subdominio (ej: empresa1.fotostudio.com)
2. **Tenant Resolution**: Middleware identifica el tenant por dominio
3. **Schema Switch**: Django cambia automáticamente al schema del tenant
4. **Data Isolation**: Todas las queries se ejecutan en el schema correcto
5. **Response**: Respuesta con datos específicos del tenant

### **Configuración de Entornos**

#### **Desarrollo**
- Base de datos local PostgreSQL
- Cache en memoria
- Logging detallado
- CORS permisivo

#### **Producción**
- Base de datos PostgreSQL en servidor
- Cache Redis
- Logging optimizado
- Seguridad SSL/TLS

### **APIs Multi-Tenant Implementadas**

#### **Gestión de Tenants**
```
GET    /api/tenants/                    # Listar tenants (admin)
GET    /api/tenants/{id}/               # Detalle tenant
GET    /api/tenants/current/            # Tenant actual
```

#### **Todas las APIs de Negocio son Multi-Tenant**
- Cada endpoint automáticamente filtra por tenant
- Datos completamente aislados entre tenants
- No es necesario agregar filtros manuales

### **Ventajas de la Implementación**

✅ **Aislamiento Completo**: Datos de cada tenant completamente separados
✅ **Escalabilidad**: Fácil agregar nuevos tenants
✅ **Mantenimiento**: Backup/restore independiente por tenant
✅ **Seguridad**: Imposible acceso cruzado entre tenants
✅ **Performance**: Queries optimizadas por schema
✅ **Flexibilidad**: Cada tenant puede tener configuraciones diferentes

🏢 DIVISIÓN EN 4 SALAS DE DESARROLLO

SALA 1: USUARIOS Y AUTENTICACIÓN 🔐
Responsable: Equipo de Seguridad y Autenticación
Módulos a Desarrollar:
    ✅ App users - Modelo, serializers, views, URLs
    ✅ Autenticación JWT - Login, logout, refresh tokens
    ✅ Perfil de usuario - CRUD completo con avatar
    ✅ Permisos y roles - Sistema de permisos personalizado
    ✅ Middleware de autenticación - Validación de tokens

Dependencias:
    Hacia otros equipos: Proporciona sistema de autenticación
    De otros equipos: Ninguna (trabajo independiente)

SALA 2: GESTIÓN DE NEGOCIO 📋
Responsable: Equipo de Lógica de Negocio
Módulos a Desarrollar:
    ✅ App orders - Gestión de pedidos
    ✅ App clients - Gestión de clientes y colegios
    ✅ App contracts - Gestión de contratos
    ✅ App agenda - Programación de citas
    ✅ App dashboard - Métricas y KPIs

Dependencias:
    Hacia otros equipos: Proporciona modelos de negocio
    De otros equipos: Sistema de autenticación (Sala 1)

SALA 3: INVENTARIO Y PRODUCCIÓN 🏭
Responsable: Equipo de Operaciones
Módulos a Desarrollar:
    ✅ App inventory - 7 categorías de materiales
    ✅ App production - Órdenes de producción
    ✅ App products - Productos terminados
    ✅ Sistema de alertas - Stock bajo y mermas
    ✅ Trazabilidad completa - Movimientos de inventario

Dependencias:
    Hacia otros equipos: Proporciona datos de inventario
    De otros equipos: Sistema de autenticación (Sala 1), Modelos de pedidos (Sala 2)

SALA 4: REPORTES Y CONFIGURACIÓN 📊
Responsable: Equipo de Análisis y Configuración
Módulos a Desarrollar:
    ✅ App reports - Reportes financieros y análisis
    ✅ App config - Configuración del sistema
    ✅ Sistema de exportación - PDF, Excel, CSV
    ✅ APIs de métricas - KPIs y dashboards
    ✅ Configuración por entornos - Dev, Prod, Test
    ✅ App tenants - Multi-tenant (infraestructura, MySQL database-based)
        - Modelos Tenant/Domain (definición de inquilinos y dominios)
        - Resolución de tenant por subdominio o cabecera
        - Enrutamiento a BD del tenant (selección de base de datos por request)
        - Middleware base de contexto de tenant (sin lógica de negocio)
        - Comandos/lineamientos de gestión (crear tenant, migraciones por tenant)

Dependencias:
    Hacia otros equipos: Proporciona reportes y configuración
    De otros equipos: Todas las apps anteriores (Sala 1, 2, 3)
    Colaboraciones específicas para multi-tenant:
        - Sala 1 (Usuarios): incluir/validar `tenant` en autenticación (claims JWT) y permisos
        - Sala 2 (Negocio): consumir contexto de tenant en servicios/queries (sin mezclar datos)
        - Sala 3 (Inventario/Producción): validar pertenencia al tenant en operaciones y reportes

📅 PLAN DE TRABAJO CONDENSADO - 3 DÍAS


Estado actual (resumen):
- [hecho] Estructura de apps creada (`users`, `clients`, `contracts`, `inventory`, `materials`, `orders`, `production`, `agenda`, `dashboard`, `tenants`).
- [hecho] Modelos base con migraciones iniciales (muchos con `managed=False`, apuntando a tablas existentes).
- [hecho] Rutas principales configuradas en `fotostudio/urls.py` para `users` y `tenants`.
- [hecho] Endpoints básicos en `tenants`: `list`, `detail` y `current` (JSON).
- [pendiente] Autenticación JWT funcional y perfiles (SALA 1).
- [pendiente] CRUDs y servicios de negocio (SALA 2).
- [pendiente] Endpoints de inventario/producción completos (SALA 3).
- [pendiente] Reportes, configuración y documentación (SALA 4).

DÍA 1: BASE FUNCIONAL TRANSVERSAL
Horario: 8:00 AM - 6:00 PM
08:00 - 10:00 Configuración y verificación
    [ ] Sala 1: Activar DRF y JWT en settings; endpoints auth mínimos (`login`, `refresh`).
    [ ] Sala 4: Configurar `ALLOWED_HOSTS`, `.env` ejemplo y `Swagger` básico.
10:00 - 13:00 Usuarios y multi-tenant mínimo viable
    [ ] Sala 1: `LoginView`, `RefreshView`, `ProfileView` (lectura) usando `apps.users` existente.
    [ ] Sala 4: Ajustar `tenants/current` para subdominio/cabecera `X-Tenant-ID` y manejo de errores.
13:00 - 14:00 Pausa
14:00 - 17:00 Rutas y seeds mínimos
    [ ] Sala 2: Exponer listados read-only: `orders`, `clients`, `contracts` (query simple).
    [ ] Sala 3: Exponer listados read-only: `inventory` (categorías), `production` (órdenes).
17:00 - 18:00 Smoke tests y documentación rápida
    [ ] Todas: Probar endpoints clave con Postman; documentar en Swagger los read-only.

DÍA 2: CRUDS PRINCIPALES Y LÓGICA BÁSICA
Horario: 8:00 AM - 6:00 PM
08:00 - 10:00 Usuarios completos
    [ ] Sala 1: `UserListCreate`, `UserDetail`, `ChangePassword`, `Profile` (update), permisos básicos.
10:00 - 13:00 Negocio básico
    [ ] Sala 2: CRUD `clients`, `orders`; filtros por estado/fecha; paginación.
    [ ] Sala 2: `dashboard` básico: totales y métricas simples.
13:00 - 14:00 Pausa
14:00 - 17:00 Inventario y producción
    [ ] Sala 3: CRUD de 2 categorías críticas (p.ej. varillas y impresión) con stock y `movements`.
    [ ] Sala 3: `production` crear/cerrar orden; cálculo simple de mermas.
17:00 - 18:00 Integración y pruebas
    [ ] Todas: Integrar auth en todos los endpoints; pruebas de permisos; actualizar Swagger.

DÍA 3: REPORTES, HARDENING Y CIERRE
Horario: 8:00 AM - 6:00 PM
08:00 - 10:00 Reportes y config
    [ ] Sala 4: Endpoints de reportes mínimos (finanzas/inventario) y exportación CSV.
    [ ] Sala 4: Configuración del sistema (parámetros básicos, e.g. umbrales de stock).
10:00 - 13:00 Multi-tenant y seguridad
    [ ] Sala 4 + Sala 1: Resolver tenant por subdominio o cabecera; inyectar `tenant` en claims JWT.
    [ ] Todas: Enforcer multi-tenant en queries (filtros por `tenant`).
13:00 - 14:00 Pausa
14:00 - 17:00 Calidad y performance
    [ ] Todas: Paginación, `select_related/prefetch_related`, validaciones.
    [ ] Todas: Tests críticos (auth, CRUDs, reportes) con cobertura razonable.
17:00 - 18:00 Cierre y entrega
    [ ] Todas: Swagger completo, README actualizados, scripts de arranque, checklist de despliegue.

NOTAS DE IMPLEMENTACIÓN Y RESPONSABILIDADES POR SALA
- Sala 1 (Usuarios y Autenticación): Auth JWT, perfiles, permisos, middleware.
- Sala 2 (Negocio): Clients, Orders, Contracts, Agenda, Dashboard.
- Sala 3 (Inventario/Producción): Inventario (2 categorías críticas), Movements, Production.
- Sala 4 (Reportes/Config/Tenants): Reportes mínimos, Config parámetros, Tenants (resolución y enforcer).

CRITERIOS DE SALIDA AL DÍA 3
    [ ] Login/refresh/profile funcionando con JWT.
    [ ] CRUD básico de `clients` y `orders` con filtros y paginación.
    [ ] Inventario mínimo (2 categorías) con movimientos y stock.
    [ ] Producción: crear/cerrar órdenes y registrar mermas.
    [ ] Reportes CSV (finanzas simple, inventario) y configuración básica.
    [ ] Multi-tenant activo por subdominio/cabecera; endpoints filtrando por `tenant`.
    [ ] Swagger actualizado y README de salas al día.

ALCANCE POSTERIOR (OPCIONAL SI HAY TIEMPO)
    [ ] Extender inventario a 7 categorías.
    [ ] Exportación PDF/Excel además de CSV.
    [ ] Métricas avanzadas y dashboards enriquecidos.

ENTREGABLES Y SOPORTE
    [ ] Postman collection actualizada.
    [ ] Instrucciones de arranque local (README raíz).
    [ ] Notas de despliegue básico (entorno PROD) y variables de entorno.

MÉTRICAS DE CALIDAD (MÍNIMAS EN 3 DÍAS)
    [ ] Autenticación y permisos probados.
    [ ] Paginación y filtros en listados.
    [ ] Validaciones esenciales en serializers.
    [ ] Logs de errores y manejo de excepciones homogéneo.

RIESGOS Y MITIGACIONES
    [ ] Datos legacy (managed=False): validar compatibilidad de campos y llaves.
    [ ] Multi-tenant por subdominio: definir fallback `X-Tenant-ID` durante DEV.
    [ ] Tiempo: priorizar vertical mínima funcional por sala y dejar extras como alcance posterior.

✅ BUENAS PRÁCTICAS OBLIGATORIAS

🔒 REGLAS DE SEGURIDAD
Autenticación y Autorización
    ✅ JWT obligatorio para todas las APIs
    ✅ Permisos granulares por endpoint
    ✅ Validación de tokens en middleware
    ✅ Rate limiting para prevenir ataques
    ✅ CORS configurado correctamente

Validación de Datos
    ✅ Serializers con validaciones estrictas
    ✅ Sanitización de inputs para prevenir XSS
    ✅ Validación de tipos de datos
    ✅ Límites de tamaño para archivos
    ✅ Validación de email con regex

🧪 TESTING OBLIGATORIO
Cobertura Mínima
    ✅ 90% coverage en código de producción
    ✅ Tests unitarios para todos los modelos
    ✅ Tests de integración para APIs
    ✅ Tests con Postman para endpoints
    ✅ Tests de autenticación y permisos

📚 DOCUMENTACIÓN OBLIGATORIA
Swagger/OpenAPI
    ✅ Documentación automática de todas las APIs
    ✅ Ejemplos de uso para cada endpoint
    ✅ Esquemas de datos detallados
    ✅ Códigos de error documentados
    ✅ Autenticación documentada
Código
    ✅ Docstrings en todas las funciones
    ✅ Comentarios en lógica compleja
    ✅ README por cada app
    ✅ Guías de instalación y configuración
��️ MANEJO DE BASE DE DATOS
Migraciones
    ✅ Migraciones organizadas por app
    ✅ Rollback siempre posible
    ✅ Datos de prueba con fixtures
    ✅ Backup antes de migraciones
    ✅ Índices en campos de búsqueda
Queries
    ✅ select_related y prefetch_related
    ✅ Evitar N+1 queries
    ✅ Paginación en listados
    ✅ Filtros eficientes
    ✅ Transacciones para operaciones críticas

🚫 RESTRICCIONES Y PROHIBICIONES
Lenguajes Prohibidos
    ❌ PHP, Node.js, JavaScript (excepto para testing)
    ❌ Java, C#, .NET, Ruby, Go, Rust
    ❌ Frontend frameworks (React, Angular, Vue)
    ❌ HTML, CSS (excepto para documentación)
Prácticas Prohibidas
    ❌ Hardcoding de credenciales
    ❌ SQL queries directas sin ORM
    ❌ Código sin tests
    ❌ APIs sin documentación
    ❌ Migraciones sin rollback

🎯 RESULTADO FINAL ESPERADO

🏗️ ARQUITECTURA FINAL DEL SISTEMA
Backend Django Completo
    ✅ 10 apps Django completamente funcionales
    ✅ API REST robusta con DRF
    ✅ Autenticación JWT implementada
    ✅ Base de datos MySQL optimizada
    ✅ Documentación Swagger completa
    ✅ Tests con 90% coverage
    ✅ Configuración por entornos

Módulos Implementados:
    Users - Autenticación, perfiles, permisos
    Orders - Gestión completa de pedidos
    Clients - Clientes particulares y colegios
    Contracts - Contratos y términos
    Inventory - 7 categorías de materiales
    Production - Órdenes de producción
    Products - Productos terminados
    Agenda - Programación de citas
    Reports - Reportes y análisis
    Dashboard - Métricas y KPIs

🔌 APIs REST Implementadas una vez que este elaborado

1.Autenticación:
    POST /api/auth/login/          # Login con JWT
    POST /api/auth/logout/         # Logout
    POST /api/auth/refresh/        # Refresh token
    GET  /api/auth/profile/        # Perfil del usuario
    PUT  /api/auth/profile/        # Actualizar perfil
    POST /api/auth/change-password/ # Cambiar contraseña

2.Gestión de Usuarios (Admin)
    GET    /api/users/             # Listar usuarios
    POST   /api/users/             # Crear usuario
    GET    /api/users/{id}/        # Detalle usuario
    PUT    /api/users/{id}/        # Actualizar usuario
    DELETE /api/users/{id}/        # Eliminar usuario

3.Pedidos
    GET    /api/orders/            # Listar pedidos
    POST   /api/orders/            # Crear pedido
    GET    /api/orders/{id}/       # Detalle pedido
    PUT    /api/orders/{id}/       # Actualizar pedido
    DELETE /api/orders/{id}/       # Eliminar pedido
    GET    /api/orders/search/     # Buscar pedidos

4.Clientes
    GET    /api/clients/           # Listar clientes
    POST   /api/clients/           # Crear cliente
    GET    /api/clients/{id}/      # Detalle cliente
    PUT    /api/clients/{id}/      # Actualizar cliente
    DELETE /api/clients/{id}/      # Eliminar cliente
    GET    /api/clients/schools/   # Listar colegios

5.Inventario
    GET    /api/inventory/varillas/        # Varillas
    GET    /api/inventory/pinturas/        # Pinturas
    GET    /api/inventory/impresion/       # Materiales impresión
    GET    /api/inventory/recordatorio/    # Materiales recordatorio
    GET    /api/inventory/software/        # Software y equipos
    GET    /api/inventory/pintura/         # Materiales pintura
    GET    /api/inventory/diseno/          # Materiales diseño
    GET    /api/inventory/alerts/          # Alertas de stock

6.Producción
    GET    /api/production/orders/         # Órdenes de producción
    POST   /api/production/orders/         # Crear orden
    GET    /api/production/orders/{id}/    # Detalle orden
    PUT    /api/production/orders/{id}/    # Actualizar orden
    POST   /api/production/register/       # Registrar producción

7.Reportes
    GET    /api/reports/financial/         # Reportes financieros
    GET    /api/reports/inventory/         # Reportes de inventario
    GET    /api/reports/production/        # Reportes de producción
    GET    /api/reports/export/pdf/        # Exportar PDF
    GET    /api/reports/export/excel/      # Exportar Excel

8.Contratos 
    GET    /api/contracts/              # Listar contratos
    POST   /api/contracts/              # Crear contrato
    GET    /api/contracts/{id}/         # Detalle contrato
    PUT    /api/contracts/{id}/         # Actualizar contrato
    DELETE /api/contracts/{id}/         # Eliminar contrato
    GET    /api/contracts/expiring/     # Contratos por vencer

9.Agenda
    GET    /api/appointments/               # Listar citas
    POST   /api/appointments/               # Crear cita
    GET    /api/appointments/{id}/          # Detalle cita
    PUT    /api/appointments/{id}/          # Actualizar cita
    DELETE /api/appointments/{id}/          # Eliminar cita
    GET    /api/appointments/calendar/      # Citas por fecha

10.Dashboard
    GET    /api/dashboard/              # Métricas principales
    GET    /api/dashboard/orders/       # Métricas de pedidos
    GET    /api/dashboard/clients/      # Métricas de clientes
    GET    /api/dashboard/revenue/      # Métricas de ingresos 

11.Productos
    GET    /api/products/                       # Productos terminados
    POST   /api/products/                       # Crear producto
    GET    /api/products/{id}/                  # Detalle producto
    PUT    /api/products/{id}/                  # Actualizar producto
    DELETE /api/products/{id}/                  # Eliminar producto
    GET    /api/products/status/{status}/       # Productos por estado
    GET    /api/products/location/{location}/   # Productos por ubicación
    POST   /api/products/sell/{id}/             # Marcar como vendido

12.Configuración
    GET    /api/config/                     # Listar configuraciones
    POST   /api/config/                     # Crear configuración
    GET    /api/config/{id}/                # Detalle configuración
    PUT    /api/config/{id}/                # Actualizar configuración
    DELETE /api/config/{id}/                # Eliminar configuración
    GET    /api/config/system/              # Configuración del sistema
    GET    /api/config/alerts/              # Configuración de alertas
    GET    /api/config/backup/              # Configuración de backup

13.Métricas y KPIs
    GET    /api/metrics/                    # Listar métricas
    POST   /api/metrics/                    # Crear métrica
    GET    /api/metrics/{id}/               # Detalle métrica
    PUT    /api/metrics/{id}/               # Actualizar métrica
    DELETE /api/metrics/{id}/               # Eliminar métrica
    GET    /api/metrics/revenue/            # Métricas de ingresos
    GET    /api/metrics/orders/             # Métricas de pedidos
    GET    /api/metrics/clients/            # Métricas de clientes
    GET    /api/metrics/inventory/          # Métricas de inventario
    GET    /api/metrics/production/         # Métricas de producción
    GET    /api/metrics/efficiency/         # Métricas de eficiencia
    GET    /api/metrics/dashboard/          # KPIs para dashboard
    GET    /api/metrics/trends/             # Análisis de tendencias
    GET    /api/metrics/comparison/         # Comparativas

14.Auditoría
    GET    /api/audit/                      # Listar logs de auditoría
    GET    /api/audit/user/{user_id}/       # Logs por usuario
    GET    /api/audit/action/{action}/      # Logs por acción
    GET    /api/audit/model/{model}/        # Logs por modelo
    GET    /api/audit/date-range/           # Logs por rango de fechas

Dashboard y Métricas
KPIs Principales
    Ingresos por servicio (mensual/anual)
    Stock bajo (alertas automáticas)
    Eficiencia de producción (mermas vs producción)
    Clientes activos (nuevos vs recurrentes)
    Pedidos pendientes (por estado)
    Tiempo promedio de entrega
Gráficos y Visualizaciones
    Gráficos de barras para ingresos
    Gráficos de líneas para tendencias
    Gráficos de pastel para distribución
    Tablas dinámicas con filtros
    Alertas visuales para stock bajo

Monitoreo
    ✅ Logging estructurado
    ✅ Métricas de performance
    ✅ Alertas automáticas
    ✅ Health checks para APIs
    ✅ Monitoring de base de datos

Sistema Listo para Producción una vez terminado
Características Finales
    ✅ Backend Django 100% funcional
    ✅ APIs REST completamente implementadas
    ✅ Autenticación de usuarios lista
    ✅ Perfil de usuario editable con avatar
    ✅ Reportes implementados y funcionales
    ✅ Escalable y listo para producción
    ✅ Documentado completamente
    ✅ Testeado con alta cobertura

Integración con Frontend
    ✅ APIs compatibles con frontend existente
    ✅ Endpoints que coinciden con necesidades
    ✅ Autenticación integrada
    ✅ Datos en formato JSON
    ✅ CORS configurado para frontend