import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Get database info from .env file
db_url = os.getenv("DATABASE_URL")

print("Testing PostgreSQL connection...")
print("-" * 50)

try:
    # Extract connection details from DATABASE_URL
    # Format: postgresql://username:password@host:port/database
    
    # Simple test using the connection string directly
    conn = psycopg2.connect(db_url)
    
    print("✅ Successfully connected to PostgreSQL!")
    
    # Test a simple query
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"\nPostgreSQL version:")
    print(version[0])
    
    # Check if our tables exist
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    
    tables = cursor.fetchall()
    if tables:
        print(f"\n✅ Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")
    else:
        print("\n⚠️  No tables found. Run: python scripts/init_db.py")
    
    cursor.close()
    conn.close()
    print("\n" + "-" * 50)
    print("Connection test completed!")
    
except Exception as e:
    print(f"\n❌ Error connecting to PostgreSQL:")
    print(f"   {e}")
    print("\nTroubleshooting:")
    print("  1. Check PostgreSQL is running")
    print("  2. Verify .env file has correct DATABASE_URL")
    print("  3. Check password and port number")