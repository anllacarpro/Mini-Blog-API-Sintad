# Mini-Blog API (FastAPI + SQLAlchemy async + Pydantic v2 + Poetry)

API de mini-blog con **FastAPI**, **SQLAlchemy 2.x async**, **Pydantic v2**, **Alembic**, **Pytest** y **Docker/Compose**. BD: **PostgreSQL**.

## Requisitos
- Python 3.10+
- Poetry
- Docker y Docker Compose

## Configuración rápida (Poetry)
```bash
poetry install
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload
```
Abrir: http://127.0.0.1:8000/docs

## Docker

### Construcción e inicio
```bash
docker compose up --build
```

El contenedor ejecutará automáticamente:
1. Espera a que la base de datos PostgreSQL esté lista
2. Ejecuta las migraciones de Alembic: `alembic upgrade head`
3. Inicia el servidor Uvicorn en `0.0.0.0:8000`

### Acceso
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Detener los servicios
```bash
docker compose down
```

### Resetear la base de datos (eliminar volúmenes)
```bash
docker compose down -v
docker compose up --build
```

## Pruebas

### Ejecutar todos los tests
```bash
poetry run pytest -v
```

### Ejecutar un test específico
```bash
poetry run pytest tests/test_users.py -v
```

### Tests con cobertura
```bash
poetry run pytest --cov=app
```

### Configuración de tests
Los tests utilizan **SQLite en memoria** para aislamiento de la base de datos:
- **Engine**: `sqlite+aiosqlite:///:memory:`
- **Fixtures**: Engine, Session y Client configurados con dependencias sobrescritas
- **Bases de datos**: Se crean y limpian automáticamente para cada test
- **Depuración de deprecaciones**: Se han corregido todas las deprecaciones de:
  - `pytest-asyncio` (removido fixture de event_loop personalizada)
  - `httpx` (usando ASGITransport explícito)
  - `datetime.utcnow()` (usando `datetime.now(timezone.utc)` timezone-aware)

## Características

### Manejo de errores
- **409 Conflict**: Se intenta crear un usuario con un email o username que ya existe
- **404 Not Found**: El recurso solicitado no existe
- **422 Unprocessable Entity**: Validación de datos inválida

### Base de datos
- **PostgreSQL 16** en Docker
- **Alembic** para migrations
- **SQLAlchemy 2.x** async para consultas
- Las migraciones se aplican automáticamente al iniciar el contenedor

## Endpoints de ejemplo (cURL)

### Usuarios
```bash
# Crear usuario
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"username":"miguel","email":"miguel@example.com"}'

# Obtener usuario por ID
curl http://localhost:8000/users/1
```

### Posts
```bash
# Crear post
curl -X POST http://localhost:8000/posts/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Hola","content":"Contenido","author_id":1}'

# Listar posts
curl "http://localhost:8000/posts/?limit=5"

# Obtener post por ID
curl http://localhost:8000/posts/1
```

### Comentarios
```bash
# Agregar comentario a un post
curl -X POST http://localhost:8000/posts/1/comments \
  -H "Content-Type: application/json" \
  -d '{"text":"nice!","author_id":1}'
```

## Estructura del proyecto
```
.
├── alembic/                    # Migraciones de base de datos
│   ├── versions/              # Archivos de migración
│   ├── env.py                 # Configuración de Alembic
│   └── script.py.mako         # Template para generar migraciones
├── app/
│   ├── main.py               # Entrada de la aplicación FastAPI
│   ├── core/
│   │   ├── config.py         # Configuración y variables de entorno
│   │   └── db.py             # Conexión y sesión de base de datos
│   ├── crud/                 # Lógica de base de datos
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── models/               # Modelos SQLAlchemy
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── schemas/              # Modelos Pydantic para validación
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   └── routers/              # Endpoints FastAPI
│       ├── users.py
│       ├── posts.py
│       └── comments.py
├── tests/                     # Tests pytest
│   ├── conftest.py
│   ├── test_users.py
│   └── test_posts.py
├── Dockerfile                 # Construcción del contenedor
├── docker-compose.yml         # Orquestación de servicios
├── pyproject.toml            # Dependencias con Poetry
├── alembic.ini               # Configuración de Alembic
└── README.md                 # Este archivo
```

## Generación de nuevas migraciones

Después de modificar los modelos SQLAlchemy:

```bash
poetry run alembic revision --autogenerate -m "descripción del cambio"
poetry run alembic upgrade head
```

En Docker, las migraciones se aplican automáticamente al iniciar.


## Notas importantes

- Las migraciones se versionan con Alembic y se aplican automáticamente en Docker
- No elimines archivos de migración - Alembic los usa para rastrear el estado
- Los tests no necesitan PostgreSQL - usan SQLite en memoria
- En producción, siempre ejecuta `alembic upgrade head` antes de iniciar la app

## Prompt utilizado (Fase 5 – Asistente de IA)

**Título:** Meta-Prompt — Asistente backend senior para Mini-Blog FastAPI  

**Rol / Persona:**  
Actúa como un **desarrollador backend senior** experto en **Python 3.10+**, **FastAPI**, **SQLAlchemy 2.x async**, **Pydantic v2**, **Poetry**, **Pytest** y **Alembic**.  
Tu prioridad es entregar código limpio, mantenible y alineado con buenas prácticas de arquitectura (SOLID, DRY, separación por capas).

---

### 🧩 Contexto del proyecto
API REST para un *Mini-Blog* con las entidades **User**, **Post** y **Comment**, conectada a una base de datos **PostgreSQL**.  
Stack técnico: FastAPI + SQLAlchemy async + Pydantic v2 + Poetry + Alembic + Docker + Pytest.  
El objetivo del asistente es apoyar la generación de código, pruebas y documentación con un enfoque profesional y reproducible.

---

### ⚙️ Reglas y principios

1. Cumplir con **SOLID**, **DRY** y usar **type hints** exhaustivos.  
2. Estructurar por capas: `routers/`, `schemas/`, `crud/`, `models/`, `core/`.  
3. Manejar errores con códigos HTTP adecuados y mensajes claros.  
4. **No** retornar objetos ORM directamente; usar modelos Pydantic (`response_model`).  
5. Inyección de dependencias con `Depends(get_session)`.  
6. **Migraciones** con Alembic autogeneradas (`revision --autogenerate`).  
7. Incluir **tests Pytest** para casos exitosos y de error.  
8. Respetar **Pydantic v2** y async/await en toda la capa DB.  
9. Preparar `Dockerfile` y `docker-compose.yml` (API + DB).  
10. Mantener comentarios breves, descriptivos y útiles.

---

### 🧠 Estilo de salida esperado

- Explicar primero el **diseño** (2-4 bullets), luego mostrar el **código completo**.  
- Incluir pasos de ejecución (`poetry`, `alembic`, `uvicorn`).  
- Asumir valores razonables cuando falten datos y documentarlos.  
- Entregar respuesta lista para copiar/pegar, con secciones claras: *contexto → pasos → código → pruebas*.

---

### 💬 Solicitudes típicas que debe resolver

- Generar o ajustar modelos y relaciones ORM.  
- Implementar CRUD async y endpoints FastAPI con `response_model`.  
- Escribir tests Pytest con fixtures reutilizables.  
- Configurar Alembic (env async, revision, upgrade).  
- Crear `Dockerfile` y `docker-compose.yml`.  
- Mostrar ejemplos cURL para verificación manual.

---

**Salida esperada:**  
Código y explicación listos para ejecutar, sin estilos innecesarios, alineados con buenas prácticas de backend y reproducibilidad.

---

> 🧭 Utilicé herramientas de asistencia como referencia para acelerar el desarrollo, pero todo el código fue revisado, ajustado y probado por mí. Entiendo cada parte de la arquitectura.

## 📚 Referencias sobre creación de prompts

- [OpenAI — Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)   
- [Anthropic — Prompt Crafting Tips](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)   
- [Prompting Guide (by DAIR.AI)](https://www.promptingguide.ai/)  
- [Awesome ChatGPT Prompts](https://huggingface.co/datasets/fka/awesome-chatgpt-prompts)

> *Estas fuentes se consultaron para aprender y aplicar buenas prácticas de ingeniería de prompts durante el diseño del asistente IA usado en la prueba técnica.*
