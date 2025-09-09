# 📸 FotoStudio Backend

## 🚀 Descripción General

Backend en Django para la gestión integral de un negocio de fotografía y enmarcado. Cubre módulos como pedidos, clientes, contratos, inventario, producción, agenda, reportes y dashboard. Este backend expone APIs REST que serán consumidas por el frontend existente en `MiniLabFrontend`.

## 🧱 Arquitectura y Módulos

- **users**: usuarios, roles y autenticación (JWT).
- **orders**: pedidos y su ciclo de vida.
- **clients**: clientes particulares y colegios.
- **contracts**: contratos escolares y vigencias.
- **inventory**: 7 categorías de materiales y movimientos.
- **production**: órdenes de producción y mermas.
- **products**: productos terminados y ubicaciones.
- **agenda**: citas y recordatorios.
- **reports**: reportes y exportaciones.
- **dashboard**: métricas y KPIs.

## 🏗️ Multi-tenant (Conceptual)

El sistema está preparado para operar en modo multi-tenant con MySQL, sin implementar lógica de negocio adicional todavía. La separación de datos se define de forma conceptual así:

- **Estrategia recomendada (database-based en MySQL)**:
  - Un **database (schema en MySQL)** por tenant: aislamiento fuerte, backups/restores por tenant y escalabilidad clara.
  - Resolución de tenant por subdominio o cabecera (por ejemplo, `X-Tenant-ID`).
  - El enrutamiento de conexiones selecciona la base de datos del tenant antes de ejecutar queries.

- **Alternativa (shared database + tenant_id)**:
  - Una única base de datos compartida y todas las tablas incluyen un campo `tenant_id`.
  - Filtros obligatorios por `tenant_id` en cada consulta y validación en middleware.

Nota: En esta fase solo se deja preparada la arquitectura y documentación. La lógica de resolución de tenant y enrutamiento se implementará por el equipo de desarrollo en pasos siguientes.

## 🔌 Conexión a MySQL

Configurar variables de entorno para MySQL (ejemplo):

```
DB_ENGINE=django.db.backends.mysql
DB_NAME=fotostudio
DB_USER=usuario
DB_PASSWORD=contraseña
DB_HOST=127.0.0.1
DB_PORT=3306
```

Para estrategia database-based por tenant, cada tenant tendrá su propio `DB_NAME` (p. ej. `fotostudio_tenant1`, `fotostudio_tenant2`).

## ▶️ Ejecución en Desarrollo (Backend)

1) Crear y activar entorno virtual
```
python -m venv venv
venv\Scripts\activate  # Windows
# o
source venv/bin/activate # Linux/Mac
```

2) Instalar dependencias
```
pip install -r requirements.txt
```

3) Configurar variables de entorno para MySQL y Django (ver sección anterior) y luego aplicar migraciones base
```
python manage.py migrate
```

4) Iniciar servidor
```
python manage.py runserver
```

## 🌐 Integración con el Frontend

- El frontend vive en `c:\Users\60861\Documents\MiniLabFrontend`. Este backend expone APIs REST en `http://localhost:8000/` para ser consumidas por ese frontend.
- Configurar CORS en Django para permitir el origen del frontend durante desarrollo.

## 📑 Documentación para el Equipo

- Este README explica: estructura de módulos, conexión MySQL y esquema multi-tenant a nivel conceptual (database-based recomendado en MySQL).
- No se incluye implementación de lógica; solo lineamientos para que el equipo desarrolle sobre esta base.

## 🧭 Buenas Prácticas (lineamientos)

- Usar `tenant_id` o selección de base de datos antes de cada operación, según estrategia elegida.
- Asegurar aislamiento de datos por tenant en toda consulta y escritura.
- Tests de integración con al menos dos tenants de prueba.

## 📞 Soporte interno

- Revisar documentación en `Instrucciones/` para detalles por sala (usuarios, negocio, inventario, reportes).
- Mantener consistencia con el frontend ya existente.

—

Este documento es una guía de alto nivel para el equipo de backend. Cubre la explicación del proyecto, cómo conectarlo a MySQL y cómo se estructura el multi-tenant en esta base.

