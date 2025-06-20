# Autotrade Python

A modular cryptocurrency trading system for learning, simulation, and (eventually) automated live trading.

## 🚀 Features

- Real-time trade ingestion via WebSocket (Coinbase)
- Candle generation from raw trades
- REST fallback (Coinbase Pro) for candle gap filling
- Asynchronous PostgreSQL storage
- Interactive CLI for backtesting
- Moving average crossover strategy
- Full historical candle backfill support
- Cron jobs for routine syncing and gap auditing
- Unit tests for core components (pytest)
- Dockerized for modularity and reproducibility

## 📁 Project Structure

```
autotrade-python/
├── backtest/           # Strategy and simulation logic
├── client/             # CLI tools and menu interface
├── ingestion/          # Live trade data streams (WebSocket)
├── services/           # Candle sync, retention, audits
├── storage/            # Database and schema logic
├── tests/              # Unit tests (pytest)
├── logs/               # Cron job and sync logs
├── docker-compose.yml  # Service orchestration
└── README.md
```

## 🛠 Getting Started

### 1. Clone and configure

```bash
git clone https://github.com/mavenson/autotrade-python.git
cd autotrade-python
cp .env.example .env  # Then edit DB credentials
```

Example `.env`:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=securepass
POSTGRES_DB=autotrade
DATABASE_URL=postgresql://postgres:securepass@db:5432/autotrade
```

### 2. Build and run the services

```bash
docker compose up -d --build
```

This starts:
- `trading-db` (PostgreSQL)
- `data-ingestion` (WebSocket collector)
- `client-menu` (CLI tool)

### 3. Use the client menu

```bash
docker compose run --rm client-menu
```

Menu options:
- Backtest strategy (moving average)
- View available trade/candle ranges
- Show stats or export results

---

## 🧭 Roadmap

### ✅ Phase 1: Reliable Data & Backtest Core (BTC-USD Only)

- [x] WebSocket ingestion + trade retention
- [x] Generate candles from trades (1m)
- [x] REST fallback/supplemental candles
- [x] Timestamp-normalized candles (REST & generated)
- [x] Daily gap detection audit
- [x] Cron-based syncing for candles
- [x] Full historical candle regeneration
- [x] Unit tests (REST sync, edge cases)
- [x] CLI client for backtesting
- 📌 **Status:** Complete & tagged for `v0.1`

---

### 🚧 Phase 2: Expand Strategy & UX

- [ ] Add more strategies (momentum, breakout, etc.)
- [ ] CLI strategy/interval selection
- [ ] Visualize candles & PnL (Textual/matplotlib)
- [ ] Save backtest results for later reuse
- [ ] Improve portfolio & PnL simulation

---

### 🧱 Phase 3: Scaling & Resilience

- [ ] Ingest multiple symbols
- [ ] Support Kraken or Binance ingestion
- [ ] Redis queue for buffering messages
- [ ] Routine database backups
- [ ] Monitoring dashboard for uptime and data health

---

### 🧠 Phase 4: Execution Engine & Simulation

- [ ] Simulated order book for realistic execution
- [ ] Add latency/slippage/fee modeling
- [ ] Live execution preview
- [ ] Optional paper trading mode

---

### 🔐 Phase 5: Production Hardening

- [ ] Live strategy execution (with safeguards)
- [ ] Autoscaling/failover-ready ingestion
- [ ] Secrets management & environment separation
- [ ] Full integration test suite

---

## 🔁 Cron Jobs

- `rest_sync.py`: Pull REST candles every 5 minutes
- `gen_candle_sync.py`: Build trade-based candles every 5 minutes
- `gap_audit.py`: Daily gap inspection (2:30 AM UTC)
- `retention_cleaner.py`: Daily cleanup of old trades

## ⚠️ Disclaimer

This project is for educational purposes only. It does not constitute financial advice or an invitation to trade.

## 📄 License

MIT
