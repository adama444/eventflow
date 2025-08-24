import psycopg2
from psycopg2.extras import RealDictCursor
from app.core.config import settings


def get_connection():
    """Create and return a new database connection."""
    conn = psycopg2.connect(settings.database_url, cursor_factory=RealDictCursor)
    return conn


def test_connection():
    """Simple test to validate DB connection."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        print("Connected to PostgreSQL:", db_version)
        cur.close()
        conn.close()
    except Exception as e:
        print("Database connection failed:", e)
