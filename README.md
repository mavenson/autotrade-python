# Autotrade Python

A modular cryptocurrency trading system for learning, simulation, and (eventually) automated live trading.

## 🚀 Features

- Real-time trade ingestion via WebSocket (Coinbase)
- Asynchronous PostgreSQL storage
- Interactive CLI client for backtesting
- Moving average crossover strategy (with parameter tuning)
- Modular backtest engine and portfolio simulator
- Dockerized for reproducibility and separation of concerns

## 📁 Project Structure

```
autotrade-python/
├── backtest/           # Strategy + simulation logic
│   ├── strategy.py
│   ├── portfolio.py
│   └── run_backtest.py
├── client/             # Terminal menu + query tools
│   ├── client_menu.py
│   └── services/
│       └── queries.py
├── ingestion/          # Live trade data stream
│   └── trade_stream.py
├── storage/            # Database write logic (ingestion)
│   └── db_api.py
├── storage/sql/        # SQL schema
│   └── schema.sql
├── .env                # DB credentials (not committed)
├── Dockerfile          # Main app container
├── Dockerfile.client   # CLI menu container
├── docker-compose.yml
└── README.md
```

## 🛠 Getting Started

### 1. Clone and configure

```bash
git clone https://github.com/mavenson/autotrade-python.git
cd autotrade-python
cp .env.example .env  # Add credentials
```

Edit `.env` to match:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=securepass
POSTGRES_DB=autotrade
DATABASE_URL=postgresql://postgres:securepass@db:5432/autotrade
```

### 2. Build and run the ingestion service

```bash
docker-compose up -d --build
```

This starts:
- `trading-db` (PostgreSQL)
- `data-ingestion` (WebSocket collector)

### 3. Use the backtesting client

```bash
docker-compose build client-menu
docker-compose run --rm client-menu
```

Menu options include:
- Run backtest with custom parameters
- View trade stats
- Check available date ranges

## 🧭 Roadmap

- [x] Ingestion + storage
- [x] Client menu interface
- [x] Backtester with parameter input
- [ ] Fee structure simulation
- [ ] Order book model
- [ ] Multi-exchange support (arbitrage)
- [ ] Machine learning parameter tuning
- [ ] Tax + compliance tracker
- [ ] Live execution engine

## ⚠️ Disclaimer

This project is for educational purposes only. It does not constitute financial advice or an invitation to trade.

## 📄 License

MIT
