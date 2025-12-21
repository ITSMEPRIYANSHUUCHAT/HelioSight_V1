-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- =========================
-- ENUMS
-- =========================
CREATE TYPE user_role AS ENUM ('super_admin', 'company_admin', 'end_user');

-- =========================
-- COMPANIES (EPCs)
-- =========================
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

-- =========================
-- USERS
-- =========================
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    fullname TEXT,
    role user_role NOT NULL,
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_login TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

CREATE INDEX idx_users_company_id ON users(company_id);

-- =========================
-- PROVIDER INTEGRATIONS
-- =========================
CREATE TABLE provider_integrations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    provider_type TEXT NOT NULL, -- solis, solarman, shinemonitor
    config JSONB NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_sync TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    UNIQUE(company_id, provider_type)
);

-- =========================
-- PLANTS
-- =========================
CREATE TABLE plants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    capacity_kw DECIMAL(10,2),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

CREATE INDEX idx_plants_company_id ON plants(company_id);

-- =========================
-- DEVICES / INVERTERS
-- =========================
CREATE TABLE devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plant_id UUID NOT NULL REFERENCES plants(id) ON DELETE CASCADE,
    provider_integration_id UUID NOT NULL REFERENCES provider_integrations(id),
    device_serial TEXT NOT NULL,
    model TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    last_seen TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    UNIQUE(plant_id, device_serial)
);

CREATE INDEX idx_devices_plant_id ON devices(plant_id);

-- =========================
-- USER ↔ PLANT ASSIGNMENTS
-- =========================
CREATE TABLE user_plant_assignments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plant_id UUID NOT NULL REFERENCES plants(id) ON DELETE CASCADE,
    permissions JSONB DEFAULT '{"read": true}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, plant_id)
);

-- =========================
-- 🔥 TIME SERIES METRICS (NARROW)
-- =========================
CREATE TABLE metrics (
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    plant_id UUID NOT NULL REFERENCES plants(id) ON DELETE CASCADE,
    device_id UUID NOT NULL REFERENCES devices(id) ON DELETE CASCADE,

    provider VARCHAR(50) NOT NULL,        -- solis / solarman / shinemonitor
    metric_type VARCHAR(50) NOT NULL,     -- power_kw, energy_kwh, pv01_voltage, etc

    value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(20),

    timestamp TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- 🔒 Deduplication guarantee
    CONSTRAINT uq_metric_dedup
        UNIQUE (device_id, metric_type, timestamp)
);

-- Convert to hypertable
SELECT create_hypertable(
    'metrics',
    'timestamp',
    chunk_time_interval => INTERVAL '1 day'
);

-- Indexes for query speed
CREATE INDEX idx_metrics_device_time
    ON metrics (device_id, timestamp DESC);

CREATE INDEX idx_metrics_plant_time
    ON metrics (plant_id, timestamp DESC);

CREATE INDEX idx_metrics_company_time
    ON metrics (company_id, timestamp DESC);

-- =========================
-- UPDATED_AT TRIGGER
-- =========================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
DECLARE t TEXT;
BEGIN
    FOREACH t IN ARRAY ARRAY[
        'companies','users','provider_integrations','plants','devices','user_plant_assignments'
    ]
    LOOP
        EXECUTE format(
            'CREATE TRIGGER trg_%s_updated BEFORE UPDATE ON %s FOR EACH ROW EXECUTE FUNCTION update_updated_at();',
            t, t
        );
    END LOOP;
END $$;

-- =========================
-- COMPRESSION
-- =========================
ALTER TABLE metrics SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'company_id,device_id',
    timescaledb.compress_orderby = 'time DESC'
);

SELECT add_compression_policy('metrics', INTERVAL '30 days');
