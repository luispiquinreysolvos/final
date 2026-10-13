# SLV AI + Odoo 17

Entorno local con Odoo 17, OCA Helpdesk, PostgreSQL y FastAPI. La API utiliza
la instancia de Ollama que ya se ejecuta en el host.

## Estructura

```text
slv-ai/
├── addons/
│   └── helpdesk_ai_ticket_suggestion/
├── services/
│   └── tickets_ai/
│       ├── application/
│       ├── domain/
│       ├── infrastructure/
│       ├── presentation/
│       └── main.py
├── oca/
│   └── helpdesk/
├── docker/
│   └── odoo/
├── compose.yaml
└── .env.example
```

El repositorio Git de todo el proyecto está en esta raíz.

## Arranque

1. Crea la configuración local:

   ```bash
   cp .env.example .env
   ```

2. Construye y arranca los servicios:

   ```bash
   docker compose up --build
   ```

3. Abre Odoo en <http://localhost:8069> y crea una base de datos. Configura una
   contraseña maestra segura en `docker/odoo/odoo.conf` antes de iniciar Odoo.

4. Activa el modo desarrollador, actualiza la lista de aplicaciones y busca
   `Helpdesk AI Ticket Suggestion`.

La API queda disponible en <http://localhost:8000/docs>. Desde el contenedor de
Odoo, la URL de la API es `http://host.docker.internal:8000`.

Ollama debe estar iniciado en el host y el modelo configurado en `.env` debe
existir previamente. Por defecto se usa `qwen3.5:2b`.

## Comandos útiles

```bash
docker compose ps
docker compose logs -f odoo ai-api
docker compose down
```

Para borrar también la base de datos y los datos persistentes de Odoo:

```bash
docker compose down --volumes
```

Este último comando elimina datos locales y no debe usarse si se quieren
conservar.
