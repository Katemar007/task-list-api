from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read the DATABASE_URL from the environment
db_url = os.getenv("SQLALCHEMY_DATABASE_URI")
print(f"Connecting to: {db_url}")

try:
    engine = create_engine(db_url)
    connection = engine.connect()
    print("✅ Connected successfully!")
    connection.close()
except Exception as e:
    print("❌ Connection failed:")
    print(e)