import os
import psycopg2
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PORT = os.getenv("POSTGRES_PORT", 5432)
DB_HOST = "localhost"

# Dossier de sortie
os.makedirs("data/raw", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

def export_table_to_csv(table_name):
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT
    )
    query = f"SELECT * FROM {table_name};"
    df = pd.read_sql(query, conn)
    path = f"data/raw/{table_name}_{timestamp}.csv"
    df.to_csv(path, index=False)
    conn.close()
    print(f"✅ {table_name} exportée vers {path}")

if __name__ == "__main__":
    for table in ["players", "matches", "performances"]:
        export_table_to_csv(table)
