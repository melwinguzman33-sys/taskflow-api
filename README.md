# TaskFlow API

API REST para la gestión de tareas internas de empleados, desarrollada con **FastAPI** y **MySQL**, siguiendo una arquitectura en capas (Controller → Service → Repository → Modelo).

Proyecto desarrollado para TaskFlow Solutions S.A.S, basado en el documento de requerimientos del cliente.

---

## Tecnologías utilizadas

- **FastAPI** — Framework web
- **SQLAlchemy** — ORM para MySQL
- **PyMySQL** — Driver de conexión a MySQL
- **python-jose** — Generación y verificación de tokens JWT
- **passlib (bcrypt)** — Hasheo seguro de contraseñas
- **python-dotenv** — Manejo de variables de entorno

---

## Arquitectura del proyecto

```
config/         → Configuración (settings, conexión a BD)
model/          → Modelos de SQLAlchemy (tablas de la BD)
schemas/        → Esquemas Pydantic (validación de entrada/salida)
repositories/   → Acceso a datos (queries)
service/        → Lógica de negocio
controller/     → Endpoints REST
utils/          → Utilidades (seguridad, autenticación)
```

---

## Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/melwinguzman33-sys/taskflow-api.git
cd taskflow-api
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo de ejemplo y completa tus datos:

```bash
cp .env.example .env
```

Edita `.env` con tus credenciales de MySQL:

```env
DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost:3306/myprojetpython
SECRET_KEY=una-clave-secreta-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Crear la base de datos

En MySQL:

```sql
CREATE DATABASE myprojetpython;
```

Las tablas se crean automáticamente al iniciar la aplicación (no se necesita correr ningún script adicional).

### 6. Levantar el servidor

```bash
uvicorn main:app --reload
```

La API quedará disponible en `http://127.0.0.1:8000`

---

## Documentación interactiva (Swagger)

Una vez levantado el servidor, accede a:

http://127.0.0.1:8000/docs


Ahí puedes probar todos los endpoints directamente desde el navegador.

---

## Endpoints disponibles

### Autenticación (públicos)

| Método | Ruta            | Descripción              |
|--------|-----------------|---------------------------|
| POST   | `/auth/register`| Registro de usuario       |
| POST   | `/auth/login`    | Inicio de sesión (JWT)    |

### Tareas (requieren autenticación)

| Método | Ruta           | Descripción                                |
|--------|----------------|---------------------------------------------|
| POST   | `/tasks`       | Crear una tarea                             |
| GET    | `/tasks`       | Listar mis tareas                           |
| GET    | `/tasks/{id}`  | Ver detalle de una tarea propia             |
| PUT    | `/tasks/{id}`  | Actualizar una tarea propia                 |
| DELETE | `/tasks/{id}`  | Eliminar una tarea propia                   |

> Para usar los endpoints de `/tasks`, primero haz login en `/auth/login`, copia el `access_token` recibido y autoriza la sesión en Swagger usando el botón **"Authorize"**.

---

## Reglas de negocio implementadas

- Cada usuario solo puede ver, modificar y eliminar **sus propias tareas**.
- Las contraseñas se almacenan hasheadas (bcrypt), nunca en texto plano.
- Los tokens JWT tienen una duración de 30 minutos.
- Una tarea **no puede pasar directamente de `pending` a `done`**: debe pasar primero por `in_progress`.

---

## Estado del proyecto

- [x] Setup base y conexión a MySQL
- [x] Registro de usuarios
- [x] Login con JWT
- [x] CRUD de tareas con control de propiedad
- [ ] Perfil y cambio de contraseña
- [ ] Roles y administración
- [ ] Manejo de errores centralizado
