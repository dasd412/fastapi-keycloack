-- Create system_setting table
CREATE TABLE IF NOT EXISTS system_setting (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    key VARCHAR NOT NULL UNIQUE,
    value VARCHAR,
    created_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'UTC'),
    updated_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'UTC')
);

-- Insert initial data
INSERT INTO system_setting (key, value) VALUES
    ('app_name', 'Keycloak POC Application'),
    ('max_login_attempts', '5');
