import pandas as pd
import psycopg2

print("🚀 ETL PIPELINE STARTED")

df = pd.read_csv("data/sales.csv")
print("📥 Data Loaded")

df["status"] = df["price"].apply(
    lambda x: "High" if x > 10000 else "Medium" if x > 2000 else "Low"
)

print("🔄 Data Transformed")

conn = psycopg2.connect(
    host="localhost",
    database="salesdb",
    user="postgres",
    password="postgres123",
    port="5433"
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    order_id INT,
    customer_name TEXT,
    product_name TEXT,
    quantity INT,
    price INT,
    status TEXT
)
""")

conn.commit()

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO sales VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        row.order_id,
        row.customer_name,
        row.product_name,
        row.quantity,
        row.price,
        row.status
    ))

conn.commit()

print("📤 Data Loaded into PostgreSQL")

cursor.execute("SELECT SUM(price) FROM sales")
print("💰 Total Revenue:", cursor.fetchone()[0])

cursor.execute("""
SELECT status, COUNT(*)
FROM sales
GROUP BY status
""")

for row in cursor.fetchall():
    print("📊", row)

conn.close()

print("✅ ETL COMPLETED SUCCESSFULLY")