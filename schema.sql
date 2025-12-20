-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Enum for user roles
CREATE TYPE user_role AS ENUM ('super_admin', 'company_admin', 'end_user');

-- Companies (Tenants)
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,  -- Use bcrypt or argon2
    fullname VARCHAR(255),
    role user_role NOT NULL,
    company_id UUID REFERENCES companies(id) ON DELETE CASCADE,  -- Null for super_admins
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_login TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

-- Index for fast user lookups
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_company_id ON users(company_id) WHERE company_id IS NOT NULL;

-- Provider Integrations (Per Company, for multi-provider support)
CREATE TABLE provider_integrations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    provider_type VARCHAR(50) NOT NULL,  -- e.g., 'solis', 'solarman', 'shinemonitor'
    config JSONB NOT NULL,  -- e.g., { "api_key": "...", "endpoint": "..." }
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_sync TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    UNIQUE(company_id, provider_type)  -- One config per provider per company
);

-- Index for provider lookups
CREATE INDEX idx_provider_integrations_company_id ON provider_integrations(company_id);

-- Plants (Solar Plants, scoped to company)
CREATE TABLE plants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    location GEOGRAPHY(POINT),  -- For lat/long, optional
    capacity DECIMAL(10,2),  -- e.g., kW
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

-- Index for plant lookups
CREATE INDEX idx_plants_company_id ON plants(company_id);

-- Devices (Inverters/Devices, linked to plants and providers)
CREATE TABLE devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plant_id UUID NOT NULL REFERENCES plants(id) ON DELETE CASCADE,
    provider_integration_id UUID NOT NULL REFERENCES provider_integrations(id) ON DELETE RESTRICT,  -- Link to provider config
    device_serial VARCHAR(100) NOT NULL,  -- Provider-specific ID
    model VARCHAR(100),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_data TIMESTAMP,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    UNIQUE(plant_id, device_serial)
);

-- Index for device lookups
CREATE INDEX idx_devices_plant_id ON devices(plant_id);
CREATE INDEX idx_devices_provider_integration_id ON devices(provider_integration_id);

-- Time-Series Metrics (Hypertable)
-- Standard table first, then convert to hypertable
CREATE TABLE metrics (
    timestamp TIMESTAMPTZ NOT NULL,
    device_id UUID NOT NULL REFERENCES devices(id) ON DELETE CASCADE,
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,  -- For partitioning and isolation
    power_output DECIMAL(10,2),  -- kW
    energy_generated DECIMAL(10,2),  -- kWh cumulative
    voltage DECIMAL(10,2),
    current DECIMAL(10,2),
    temperature DECIMAL(5,2),
    status VARCHAR(50),  -- e.g., 'online', 'fault'
    raw_data JSONB  -- Raw provider response for debugging (Super Admin only)
);

-- Convert to hypertable, partitioned by time (1 day chunks) and company_id (for tenant isolation)
SELECT create_hypertable('metrics', 'timestamp', chunk_time_interval => INTERVAL '1 day', partitioning_column => 'company_id', number_partitions => 10);

-- Indexes for efficient queries
CREATE INDEX idx_metrics_device_id_timestamp ON metrics(device_id, timestamp DESC);
CREATE INDEX idx_metrics_company_id_timestamp ON metrics(company_id, timestamp DESC);

-- User-Plant Assignments (For end_users to access specific plants)
CREATE TABLE user_plant_assignments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plant_id UUID NOT NULL REFERENCES plants(id) ON DELETE CASCADE,
    permissions JSONB NOT NULL DEFAULT '{"read": true, "write": false}',  -- Granular perms
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, plant_id)
);

-- Audit Logs (For compliance, optional but recommended for production)
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(50) NOT NULL,  -- e.g., 'create_plant', 'update_user'
    entity_id UUID,
    details JSONB,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
DECLARE
    t text;
BEGIN
    FOREACH t IN ARRAY ARRAY['companies', 'users', 'provider_integrations', 'plants', 'devices', 'user_plant_assignments']
    LOOP
        EXECUTE format('CREATE TRIGGER trigger_update_%s BEFORE UPDATE ON %s FOR EACH ROW EXECUTE PROCEDURE update_updated_at();', t, t);
    END LOOP;
END;
$$;

-- Compression policy for hypertable (enable after 30 days, compress old data)
ALTER TABLE metrics SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'company_id',
    timescaledb.compress_orderby = 'timestamp DESC'
);
SELECT add_compression_policy('metrics', INTERVAL '30 days');