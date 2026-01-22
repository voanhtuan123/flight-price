import os
import sys
from pathlib import Path

# Setup path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

from app.db.database import engine, Base
from app.db import table_models 


def main():
    print()
    print("=" * 70)
    print("INITIALIZE DATABASE")
    print("=" * 70)
    print()
    
    # Show database URL
    db_url = os.getenv("DATABASE_URL", "No set!")
    print(f"📍 Database: {db_url}")
    print()
    
    try:
        # Test connection
        print("Testing connection to database...")
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        print("Connection successful!")
        print()
        
        # Create tables
        print("Initializing tables...")
        Base.metadata.create_all(bind=engine)
        
        # Show tables
        print("Tables initialized:")
        print()
        print("Tables:")
        for table_name in sorted(Base.metadata.tables.keys()):
            print(f"   ✓ {table_name}")
        
        print()
        print("=" * 70)
        print("Database initialization complete!")
        print("=" * 70)
        print()
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("💡 Troubleshooting Suggestions:")
        print("   1. Docker: docker compose ps")
        print("   2. Start: docker compose up -d")
        print("   3. Driver: pip install psycopg2-binary")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())