Here’s the **updated full `README.md`** with the corrected project structure formatting using `text` fenced code blocks:

---

````markdown
# 📈 autotrade-python

autotrade-python is a modular, async crypto trading pipeline designed for real-time 
data ingestion, strategy prototyping, and backtesting. Built with aiohttp, asyncpg, 
and PostgreSQL, it ingests live trade data via WebSocket, stores it for analysis, 
and enables simplified strategy backtesting — all in a clean, testable architecture. 
Ideal for developers building automated trading systems or exploring time-series 
trading strategies.

---

## 🚀 Features

- ✅ Async WebSocket stream using `aiohttp`
- ✅ Real-time ingestion of trade data
- ✅ PostgreSQL integration via `asyncpg`
- ✅ Modular architecture for scalability
- ✅ Structured for unit testing with `pytest`
- 🔜 Strategy engine & REST API support

---

## 📦 Project Structure

```text
autotrade-python/
├── core/             # DB logic, shared core modules
├── utils/            # Helper functions (e.g., message parsing)
├── ingestion/        # WebSocket or REST data streams
├── storage/          # SQL schema and data persistence
├── tests/            # Unit tests (pytest)
├── main.py           # Entry point
├── Dockerfile        # Container setup
├── requirements.txt
└── README.md
````

---

## 🧪 Quick Start (Local)

**Install dependencies:**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Start PostgreSQL** (you can use Docker if needed):

```bash
docker-compose up db  # if configured
```

**Run the app:**

```bash
python main.py
```

**Run tests:**

```bash
pytest
```

---

## 🐳 Docker

Build and run in Docker:

```bash
docker build -t autotrade-python .
docker run --rm autotrade-python
```

To run tests:

```bash
docker run --rm autotrade-python pytest
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root with the following:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=autotrade
DB_USER=postgres
DB_PASSWORD=yourpassword
```

> 💡 Tip: Add `.env` to `.gitignore` to avoid leaking credentials.

---

## 📊 Example Trade Message (Parsed)

```json
{
  "symbol": "BTC-USD",
  "price": 42600.25,
  "volume": 0.012,
  "timestamp": "2025-05-12T15:10:21.000Z"
}
```

These messages are stored in PostgreSQL for further analysis or strategy execution.

---

## 🛠 Tech Stack

* Python 3.11+
* aiohttp
* asyncpg
* PostgreSQL
* pytest
* Docker (optional)

---

## 📌 TODO

* [ ] REST ingestion module
* [ ] Trading strategy execution
* [ ] Config management
* [ ] Logging and monitoring
* [ ] Exchange adapter abstraction

---

## 📄 License

MIT — see [LICENSE](./LICENSE)

