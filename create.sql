-- Create the projects table
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create the sensors table
CREATE TABLE sensors (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create the sensor_data table
CREATE TABLE sensor_data (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER REFERENCES sensors(id) ON DELETE CASCADE,
    timestamp TIMESTAMP NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(20),
    metadata JSONB
);

-- Create the users table (optional)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'viewer',
    created_at TIMESTAMP DEFAULT NOW()
);


