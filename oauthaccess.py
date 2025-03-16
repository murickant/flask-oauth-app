import psycopg2

DB_CONFIG = {
    "dbname": "epic_mvp",
    "user": "thomas.murickan",  # Replace with your actual PostgreSQL user
    "password": "1234",  # Replace with your actual password
    "host": "localhost",
    "port": "5432"
}

def get_access_token():
    """Fetches the latest access token from PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Retrieve the most recent token
        cursor.execute("SELECT token FROM access_tokens ORDER BY created_at DESC LIMIT 1;")
        token = cursor.fetchone()
        conn.close()

        if token:
            print(f"🔑 Retrieved Access Token: {token[0]}")
            return token[0]
        else:
            print("❌ No access token found in the database.")
            return None

    except Exception as e:
        print(f"❌ Database error: {e}")
        return None

# Test if token retrieval works
if __name__ == "__main__":
    get_access_token()
