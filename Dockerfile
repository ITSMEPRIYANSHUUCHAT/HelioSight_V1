FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# ✅ COPY BOTH REQUIREMENT FILES
COPY backend/requirements.txt ./requirements.txt
COPY backend/requirements-prod.txt ./requirements-prod.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements-prod.txt

# Copy backend code AFTER deps (fast rebuilds)
COPY backend/app ./app
COPY backend/migrations ./migrations
COPY backend/scripts ./scripts
COPY backend/dags ./dags

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
