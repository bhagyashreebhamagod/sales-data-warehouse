import psycopg2

print("Connecting to PostgreSQL...")

try:
    conn = psycopg2.connect(
        host="localhost",
        database="salesdb",
        user="postgres",
        password="postgres123",  # 🔴 change this to your real password
        port="5433"
    )

    cursor = conn.cursor()

    print("Connected successfully!")

    # Test query
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print("PostgreSQL Version:", version)

    cursor.close()
    conn.close()

except Exception as e:
    print("Connection failed:")
    print(e)