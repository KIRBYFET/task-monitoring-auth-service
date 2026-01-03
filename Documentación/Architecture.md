# Arquitectura — Task Monitoring Auth Service

Este documento describe la **arquitectura del servicio Task Monitoring Auth Service**, un backend orientado a **autenticación y autorización**, diseñado para integrarse con otros servicios (por ejemplo, el sistema de monitoreo de tareas).

El proyecto demuestra buenas prácticas de **seguridad backend**, **separación de responsabilidades** y **diseño desacoplado**.

---

## 🧠 Visión general

El sistema se implementa como una **API REST** desarrollada con **FastAPI**, respaldada por una base de datos **SQLite**, y soporta dos mecanismos de autenticación diferenciados:

- **Usuarios humanos** → autenticación mediante **JWT**
- **Clientes máquina (integraciones)** → autenticación mediante **API Keys**

La autorización se basa en:

- **Roles (RBAC)** para usuarios humanos
- **Scopes** para clientes máquina

---

## 🧩 Componentes principales

### 1️⃣ API REST (FastAPI)

La API expone endpoints para:

- Autenticación de usuarios (login, perfil actual)
- Emisión y validación de tokens JWT
- Administración de usuarios y roles (solo admin)
- Administración de clientes máquina y API Keys (solo admin)

Incluye además:

- Documentación interactiva mediante **Swagger UI**
- Dependencias reutilizables para autenticación y autorización

---

### 2️⃣ Capa de seguridad (Core / Security)

Contiene la lógica central de seguridad del sistema:

- Hashing de contraseñas (bcrypt)
- Generación y validación de JWT
- Extracción de identidad desde el header `Authorization`
- Validación de API Keys desde el header `X-API-Key`
- Evaluación de roles (`ADMIN`, `USER`)
- Evaluación de scopes para clientes máquina

Esta lógica se implementa mediante **dependencias de FastAPI**, permitiendo su reutilización en múltiples endpoints.

---

### 3️⃣ Persistencia de datos (DB / Models)

El sistema utiliza **SQLite** como base de datos para almacenar:

- Usuarios humanos (`User`)
- Clientes máquina (`Client`)
- Estados de habilitación (`is_active`)
- Roles y scopes

Se utiliza un ORM (SQLAlchemy) para:

- Definición de modelos
- Gestión de sesiones
- Consultas y transacciones

---

## 🔁 Flujos de autenticación y autorización
### A) Usuario humano (JWT)

1. El usuario envía credenciales a POST /auth/login.
2. El sistema valida las credenciales contra la base de datos.
3. Se genera un JWT firmado.
4. El usuario consume endpoints protegidos enviando:
   
```
Authorization: Bearer <token>
```

5. Una dependencia valida el token y obtiene el usuario actual.
6. Se evalúan reglas adicionales (rol, estado activo).

---

### B) Cliente máquina (API Key)
1. El cliente realiza peticiones enviando:

```
X-API-Key: <api_key>
```

2. El sistema busca el cliente comparando el hash de la API Key.

3. Se valida:

    - Que el cliente esté activo

    - Que posea el scope requerido

4. La petición continúa si la validación es correcta.

---

## 🔐 Modelo de autorización
### Usuarios humanos → Roles (RBAC)
| Rol     | Descripción                                   |
| ------- | --------------------------------------------- |
| `USER`  | Acceso limitado a endpoints autorizados       |
| `ADMIN` | Administración de usuarios y clientes máquina |

Ejemplo:
- Endpoints /admin/* solo accesibles por ADMIN.

---

### Clientes máquina → Scopes
Los scopes definen acciones específicas permitidas a integraciones.

Ejemplos:
- tasks:create
- tasks:read
- tasks:close
- tasks:report

Esto permite controlar el acceso de sistemas externos de forma granular.

---

## 🔗 Integración futura con Automated Task Monitoring System
Este servicio está diseñado para integrarse con otros sistemas backend.
En una integración futura:

El Task Monitoring Auth Service:
- Emite tokens JWT
- Valida API Keys
- Define roles y scopes

El Automated Task Monitoring System:
- Protege endpoints usando JWT o API Keys
- Confía en este servicio para la autenticación y autorización

Este enfoque permite una arquitectura modular y escalable.

---

## 🚫 Limitaciones conocidas (intencionales)
- No incluye OAuth externo (Google, GitHub)
- No incluye autenticación multifactor (MFA)
- No incluye refresh tokens en esta versión
- No incluye rate limiting o WAF
- No está orientado a producción (HTTPS, secrets manager)

Estas decisiones permiten mantener el foco en los objetivos del proyecto.

---

## 📝 Notas finales
La arquitectura de este proyecto fue diseñada con fines educativos y de portafolio, priorizando:

- Claridad arquitectónica
- Separación de responsabilidades
- Facilidad de integración futura

El diseño es extensible y puede evolucionar hacia escenarios más complejos si el proyecto lo requiere.
