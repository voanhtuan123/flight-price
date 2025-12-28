# Flight Price Search (Amadeus API)

## Requirements
- Python >= 3.9

## Setup

### 1. Clone project
```bash
git clone <repo-url>
cd flight-price
```
### 2. Create virtual environment
```bash
python -m venv venv
```

***Activate***

macOS/Linux:
```bash
source venv/bin/activate
```

Windows:
```bash
venv\Scripts\activate
```

### 3.Install dependencies
```bash
pip install -r requirements.txt
```

### 4.Setup environment variables
1. Create .env file on main dir
2. Edit .env 
```
AMADEUS_CLIENT_ID=your_client_id
AMADEUS_CLIENT_SECRET=your_client_secret
```
.env is ignored by git

 **WARNING**
you have to create API key by create account on developers.amadeus.com

---
