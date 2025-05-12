CREATE TABLE IF NOT EXISTS trades (
    id SERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    price NUMERIC(18, 8) NOT NULL,
    volume NUMERIC(18, 8) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    raw_message JSONB  -- ✅ optional raw message storage
);