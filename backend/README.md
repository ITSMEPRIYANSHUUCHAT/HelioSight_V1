# Solar SaaS Dashboard Backend

## Setup
1. Copy `.env.example` to `.env` and fill values.
2. Run `docker compose up -d` to start services (DB auto-inits with schema.sql).
3. Access API at http://localhost:8000/docs, Frontend at :3000, Airflow at :8080, pgAdmin at :5050.

## Run Locally (without Docker)
`uvicorn app.main:app --reload`

## Migrations (Phase 2)
`alembic init migrations`
Then generate/apply revisions.

## Deployment to AWS
Use deploy/ folders for ECS/CF templates.