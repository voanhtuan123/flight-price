# Flight Price Tracker

Search and track flight prices using Amadeus API. Automatically saves all search results to PostgreSQL database.

## What You Need
- Python 3.9 or newer
- PostgreSQL database
- Amadeus API account (free)

---

## Quick Setup (Step by Step)

### Step 1: Download the Project
```bash
git clone <repo-url>
cd flight-price
```

### Step 2: Setup Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 3: Install PostgreSQL

**Windows:**
1. Download from: https://www.postgresql.org/download/windows/
2. Run installer, click "Next" until you see password screen
3. **Set a password** (write it down! You'll need it)
4. Remember the port number (default is 5432)
5. Finish installation

**Mac:**
```bash
brew install postgresql@16
brew services start postgresql@16
```

**Linux:**
```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Step 4: Create Database

Open **pgAdmin 4** (installed with PostgreSQL):
1. It will ask for a master password - create one
2. Double-click "PostgreSQL 16" on the left
3. Enter the password you set during installation
4. Right-click "Databases" → "Create" → "Database"
5. Name it: `flight_prices`
6. Click "Save"

### Step 5: Get API Keys

1. Go to: https://developers.amadeus.com
2. Click "Register" and create free account
3. After login, go to "My Self-Service Workspace"
4. Copy your **API Key** and **API Secret**

### Step 6: Configure Environment

Create a file named `.env` in the project folder:
```env
AMADEUS_API_KEY=paste_your_api_key_here
AMADEUS_API_SECRET=paste_your_api_secret_here
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/flight_prices
```

**Important:** 
- Replace `your_password` with your PostgreSQL password
- Replace `5432` with your port if you used a different one
- If your password has `@` symbol, replace it with `%40`
  - Example: `Pass@123` becomes `Pass%40123`

### Step 7: Setup Database Tables
```bash
python scripts/init_db.py
```

You should see: `✓ Database tables created successfully!`

### Step 8: Test Everything Works
```bash
python scripts/test_flight_search.py
```

If successful, you'll see flight prices and: `✅ Saved search with X flight offers!`

---

## View Your Data

### Using pgAdmin 
1. Open pgAdmin 4
2. Expand: PostgreSQL 16 → Databases → flight_prices → Schemas → public → Tables
3. Right-click `flight_prices` → View/Edit Data → All Rows
4. You'll see all saved flights!

---

## For Team Members: Connect to Shared Database

Ask your team lead for:
- Database host/IP address
- Port number  
- Username
- Password

Update your `.env`:
```env
DATABASE_URL=postgresql://username:password@192.168.1.100:5432/flight_prices
```

Then run:
```bash
python test_connection.py
```

---

## Common Problems

**"connection refused"**
→ PostgreSQL isn't running. Windows: Search "Services", find "postgresql", right-click → Start

**"password authentication failed"**  
→ Wrong password in `.env`. Check your password and special characters.

**"database does not exist"**
→ Create database in pgAdmin (Step 4)

**"No module named 'app'"**
→ Make sure virtual environment is activated and you're in project folder

---

## What Gets Saved

Every search saves:
- Search details (origin, destination, date)
- All flight offers found
- Prices, airlines, flight numbers
- Number of stops
- Transit airports
- Timestamps

---

## Project Structure
```
flight-price/
├── app/
│   ├── db/              # Database code
│   ├── flight_search.py # Main search logic
│   └── amadeus_client.py
├── scripts/
│   ├── init_db.py       # Setup database
│   └── test_flight_search.py
├── .env                 # Your secrets (DON'T share!)
└── requirements.txt
```

---

