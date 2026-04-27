import pandas as pd
import psycopg2

# EXTRACT
df = pd.read_csv("data.csv")

# TRANSFORM
df = df[df["age"] > 18]
df["age_group"] = df["age"].apply(lambda x: "young" if x < 30 else "adult")

# LOAD
conn = psycopg2.connect(https://rcrmdctlgpliuikyiocp.supabase.co)

cursor = conn.cursor()

# tworzenie tabeli
cursor.execute("""
CREATE TABLE IF NOT EXISTS users_clean (
    name TEXT,
    age INT,
    city TEXT,
    age_group TEXT
)
""")

# czyszczenie
cursor.execute("DELETE FROM users_clean")

# insert danych
for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO users_clean VALUES (%s, %s, %s, %s)",
        (row["name"], row["age"], row["city"], row["age_group"])
    )

conn.commit()
conn.close()

print("ETL PostgreSQL done")
