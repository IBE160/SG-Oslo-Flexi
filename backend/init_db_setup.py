import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def init_db():
    # Parse credentials from DATABASE_URL or hardcode for this check based on what I wrote to .env
    # URL: postgresql+asyncpg://postgres:postgres@localhost:5432/app_db
    user = "postgres"
    password = "postgres"
    host = "localhost"
    dbname = "app_db"
    
    try:
        con = psycopg2.connect(dbname='postgres', user=user, host=host, password=password)
    except Exception as e:
        print(f"Could not connect to postgres to check DB existence: {e}")
        return

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    
    cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{dbname}'")
    exists = cur.fetchone()
    if not exists:
        print(f"Creating database {dbname}...")
        cur.execute(f"CREATE DATABASE {dbname}")
    else:
        print(f"Database {dbname} already exists.")
    
    cur.close()
    con.close()

if __name__ == "__main__":
    init_db()
