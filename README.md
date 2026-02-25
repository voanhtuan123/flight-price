# ✈️ Flight Price Tracker

A flight price tracking and analysis application using PostgreSQL, Docker, and Python.

---

## 📋 Table of Contents

- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Viewing Data](#viewing-data)
- [Useful Commands](#useful-commands)
- [Troubleshooting](#troubleshooting)

---

## 🔧 System Requirements

Before starting, ensure you have installed:

- **Docker Desktop** ([Download](https://www.docker.com/products/docker-desktop/))
  - Windows: Docker Desktop for Windows
  - Mac: Docker Desktop for Mac
  - Linux: Docker Engine + Docker Compose
- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **pgAdmin Desktop** (Optional - for database visualization) ([Download](https://www.pgadmin.org/download/))

### Verify Installation:
```bash
# Check Docker
docker --version
docker compose version

# Check Python
python --version
# or
python3 --version

# Check Git
git --version
```

**Expected Output:**
```
Docker version 24.x.x
Docker Compose version v2.x.x
Python 3.11.x
git version 2.x.x
```

---

## 🚀 Installation

### Step 1: Clone Repository
```bash
# Clone project
git clone <repository-url>
cd flight-price-tracker

# Or if you already have the source code
cd flight-price-tracker
```

---

### Step 2: Create Python Virtual Environment

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\Activate.ps1
```

**Confirm Activation:**
- Command prompt will show `(venv)` prefix
- Example: `(venv) user@computer:~/flight-price$`

---

### Step 3: Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install packages
pip install -r requirements.txt
```


---

## ⚙️ Configuration

### Step 1: Create `.env` File
```bash
# Copy template
cp .env.example .env

# Open for editing
# macOS:
nano .env

# Windows:
notepad .env
```

---

### Step 2: Configure `.env`

**`.env` File:**
```env
# ============================================================
# PostgreSQL Configuration
# ============================================================
POSTGRES_USER=postgres
POSTGRES_PASSWORD=flight_price_2024_secure
POSTGRES_DB=flight_prices
POSTGRES_PORT=5432

# Database URL (auto-constructed from above)
DATABASE_URL=postgresql+psycopg2://postgres:flight_price_2024_secure@localhost:5432/flight_prices

# ============================================================
# pgAdmin Configuration
# ============================================================
PGADMIN_EMAIL=admin@flightprice.com
PGADMIN_PASSWORD=Admin123!@#
PGADMIN_PORT=5050

# ============================================================
# Amadeus API (Flight Search)
# ============================================================
# Get your API keys from: https://developers.amadeus.com/
AMADEUS_API_KEY=your_api_key_here
AMADEUS_API_SECRET=your_api_secret_here

# ============================================================
# Application Settings
# ============================================================
DEBUG=True
```

**⚠️ IMPORTANT:**
- Replace `your_api_key_here` and `your_api_secret_here` with real API keys
- Register for free at: https://developers.amadeus.com/

---

### Step 3: Start Docker
```bash
# Start Docker Desktop (GUI)
# Open Docker Desktop application and wait for icon to turn green

# Or check if Docker is running
docker info
```

---

## 🐳 Starting the Database

### Step 1: Start Docker Containers
```bash
# Start PostgreSQL and pgAdmin
docker compose up -d

# Check status
docker compose ps
```

**Expected Output:**
```
NAME                   STATUS              PORTS
flight_price_db        Up (healthy)        0.0.0.0:5432->5432/tcp
flight_price_pgadmin   Up                  0.0.0.0:5050->80/tcp
```

---

### Step 2: Initialize Database
```bash
# Create tables in database
python scripts/init_db.py
```

**Expected Output:**
```
======================================================================
🐘 INITIALIZE DATABASE
======================================================================

📍 Database: postgresql+psycopg2://postgres:***@localhost:5432/flight_prices

Testing connection to database...
✅ Connection successful!

🔧 Creating database tables...
✅ Database initialized successfully!

📊 Tables created:
   ✓ flight_analyzes
   ✓ flight_searches

======================================================================
🎉 SETUP COMPLETE!
======================================================================
```

---

## ▶️ Running the Application

### Search and Save Flight Prices:
```bash
# Run application
python app/main.py
```

**Output:**
```
======================================================================
INITIALIZING DATABASE
======================================================================
✅ Database tables ready

======================================================================
SEARCHING FLIGHTS: YYC → YVR on 2026-02-15
======================================================================

✅ Found 10 flight offers

[1/10] Price: 112.4
        Duration: PT1H32M
        Flights: YYC - YXX
        Code: WS479

...

======================================================================
SAVING 10 FLIGHTS TO DATABASE
======================================================================

[1/10] Adding: YYC - YXX
[2/10] Adding: YYC - YXX
...

Committing to database...

======================================================================
✅ SUCCESS! All flights saved to database
======================================================================

📊 Total records in database: 10
```

---

## 👀 Viewing Data

### Method 1: pgAdmin Web UI

1. **Open browser:** http://localhost:5050
2. **Login:**
   - Email: `admin@flightprice.com`
   - Password: `Admin123!@#`
3. **Add server (first time):**
   - Right-click `Servers` → `Register` → `Server`
   - **General tab:**
     - Name: `Docker PostgreSQL`
   - **Connection tab:**
     - Host: `postgres`
     - Port: `5432`
     - Username: `postgres`
     - Password: `flight_price_2024_secure`
     - ☑️ Save password
4. **View data:**
   - Navigate: `Servers → Docker PostgreSQL → Databases → flight_prices → Schemas → public → Tables → flight_searches`
   - Right-click table → `View/Edit Data` → `All Rows`

---

### Method 2: pgAdmin Desktop App

1. **Open pgAdmin Desktop**
2. **Add server:**
   - **General:** Name = `Docker PostgreSQL`
   - **Connection:**
     - Host: `localhost` ⚠️ (NOT `postgres`)
     - Port: `5432`
     - Database: `postgres`
     - Username: `postgres`
     - Password: `flight_price_2024_secure`
3. **View data:** Same as pgAdmin Web

---

### Method 3: Terminal (psql)
```bash
# Connect to PostgreSQL
docker compose exec postgres psql -U postgres -d flight_prices

# Commands
\dt                          # List tables
\d flight_searches          # Table structure
SELECT COUNT(*) FROM flight_searches;  # Count records
SELECT * FROM flight_searches LIMIT 10; # View 10 rows
\q                          # Exit
```


---

## 🛠️ Useful Commands

### Docker
```bash
# Start services
docker compose up -d

# Stop services (keep data)
docker compose down

# Stop and remove data
docker compose down -v

# View logs
docker compose logs -f postgres
docker compose logs -f pgadmin

# Restart
docker compose restart

# Check status
docker compose ps
```

---

### Database
```bash
# Connect to PostgreSQL
docker compose exec postgres psql -U postgres -d flight_prices

# Backup database
docker compose exec postgres pg_dump -U postgres flight_prices > backup_$(date +%Y%m%d).sql

# Restore database
docker compose exec -T postgres psql -U postgres flight_prices < backup.sql

# Count records
docker compose exec postgres psql -U postgres -d flight_prices -c "SELECT COUNT(*) FROM flight_searches;"

# View latest 5 flights
docker compose exec postgres psql -U postgres -d flight_prices -c "SELECT * FROM flight_searches ORDER BY id DESC LIMIT 5;"
```

---

### Python
```bash
# Activate virtual environment
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# Deactivate
deactivate

# Install new package
pip install package_name

# Update requirements.txt
pip freeze > requirements.txt

# Run app
python -m app
```

---

## 🐛 Troubleshooting

### ❌ Problem: Port 5432 already in use

**Cause:** Local PostgreSQL is running

**Solution:**
```bash
# Mac/Linux
brew services stop postgresql

# Or change Docker port
# Edit .env:
POSTGRES_PORT=5433
DATABASE_URL=postgresql+psycopg2://postgres:flight_price_2024_secure@localhost:5433/flight_prices

# Restart
docker compose down
docker compose up -d
```

---

### ❌ Problem: Cannot connect to Docker daemon

**Cause:** Docker Desktop is not running

**Solution:**
1. Open Docker Desktop
2. Wait for Docker icon to turn green
3. Run command again

---

### ❌ Problem: ERROR: database "flight_prices" does not exist

**Solution:**
```bash
# Recreate database
docker compose down -v
docker compose up -d
python scripts/init_db.py
```

---

### ❌ Problem: ModuleNotFoundError: No module named 'app'

**Cause:** Virtual environment not activated or missing dependencies

**Solution:**
```bash
# Activate venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

---

### ❌ Problem: No data in database after running

**Check:**
```bash
# Check if data was saved
docker compose exec postgres psql -U postgres -d flight_prices -c "SELECT COUNT(*) FROM flight_searches;"

# If 0, check logs for errors
python -m app 2>&1 | grep ERROR
```

**Common causes:**
- Wrong API key or quota exceeded
- Incorrect connection string
- Code bug (check traceback)

---

### ❌ Problem: pgAdmin not showing tables

**Solution:**
1. **Refresh:** Press `F5` in pgAdmin
2. **Check correct database:** `flight_prices` (not `postgres`)
3. **Check correct schema:** `public`
4. **Expand tree fully:**
```
   Servers → Docker PostgreSQL → Databases → flight_prices → 
   Schemas → public → Tables
```

---

## 📁 Project Structure
```
flight-price-tracker/
├── app/
│   ├── __init__.py              # Main application
│   ├── flight_search.py         # API integration
│   └── db/
│       ├── database.py          # Database connection
│       └── table_models.py      # SQLAlchemy models
├── scripts/
│   ├── init_db.py               # Initialize database
│   └── view_data.py             # View data script
├── docker-compose.yml           # Docker services config
├── .env                         # Environment variables (DO NOT COMMIT)
├── .env.example                 # Template for .env
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## 📚 Example Queries

### SQL Queries (in psql):
```sql
-- Find cheapest flights
SELECT * FROM flight_searches ORDER BY price ASC LIMIT 5;

-- Direct flights only (no layovers)
SELECT * FROM flight_searches WHERE stops = 0 ORDER BY price;

-- Statistics by route
SELECT 
    flight_path,
    COUNT(*) as total_flights,
    MIN(price) as min_price,
    AVG(price)::NUMERIC(10,2) as avg_price
FROM flight_searches
GROUP BY flight_path
ORDER BY min_price;

-- Flights in a month
SELECT * FROM flight_searches 
WHERE flight_date BETWEEN '2026-02-01' AND '2026-02-28'
ORDER BY price;
```

---

### Python Queries:
```python
from app.db.database import SessionLocal
from app.db.table_models import FlightSearch
from sqlalchemy import func

db = SessionLocal()

# Cheapest flight
cheapest = db.query(FlightSearch).order_by(FlightSearch.price).first()
print(f"Cheapest: {cheapest.flight_path} - ${cheapest.price}")

# Average price by route
avg_prices = db.query(
    FlightSearch.flight_path,
    func.avg(FlightSearch.price).label('avg')
).group_by(FlightSearch.flight_path).all()

for route, avg in avg_prices:
    print(f"{route}: ${avg:.2f}")

db.close()
```

---

## 🔐 Security Notes

### ⚠️ IMPORTANT:

1. **DO NOT commit `.env` file** to Git
   - Contains passwords and API keys
   - Already added to `.gitignore`

2. **Change default passwords** in production:
```env
   POSTGRES_PASSWORD=your_strong_password_here
   PGADMIN_PASSWORD=your_admin_password_here
```

3. **Protect API keys:**
   - Do not share API keys
   - Do not commit to Git
   - Regenerate if leaked

4. **Production deployment:**
   - Do not expose port 5432 to internet
   - Use HTTPS for pgAdmin
   - Enable SSL for PostgreSQL
   - Regular backups

---

## 📞 Support

### If you encounter issues:

1. **Check logs:**
```bash
   docker compose logs postgres
   docker compose logs pgadmin
```

2. **Verify setup:**
```bash
   docker compose ps
   docker volume ls
```

3. **Reset everything:**
```bash
   docker compose down -v
   docker compose up -d
   python scripts/init_db.py
```

4. **Contact:**
   - GitHub Issues: [repository-url]/issues
   - Email: voanhtuantia@gmail.com

---

## 🎉 Quick Start Summary
```bash
# 1. Clone
git clone <repo-url>
cd flight-price-tracker

# 2. Setup Python
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# 3. Configure
cp .env.example .env
# Edit .env with your settings

# 4. Start Docker
docker compose up -d

# 5. Initialize database
python scripts/init_db.py

# 6. Run app
python -m app

# 7. View data
# pgAdmin: http://localhost:5050
# Or: docker compose exec postgres psql -U postgres -d flight_prices
```

---
