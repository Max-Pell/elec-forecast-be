CREATE EXTENSION IF NOT EXISTS Timescaledb;

CREATE TABLE IF NOT EXISTS observations (
    ts TIMESTAMPTZ NOT NULL,
    series TEXT NOT NULL,
    value DOUBLE PRECISION,
    UNIQUE(ts,series)
);

SELECT create_hypertable('observations', by_range('ts'), if_not_exists => TRUE);
