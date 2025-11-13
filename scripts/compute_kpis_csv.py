import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# ------------------------------
# Charger .env
# ------------------------------
load_dotenv()

# ------------------------------
# Variables de configuration
# ------------------------------
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

# ------------------------------
# Config fichiers
# ------------------------------
PERF_CSV = "data/performances_clean.csv"
OUTPUT_CSV = "data/processed/players_kpis.csv"

# ------------------------------
# Fonctions
# ------------------------------
def compute_nb_matches(minutes):
    if minutes <= 0:
        return 0
    return (minutes // 90) + 1

def safe_div(a, b):
    return a / b if b not in (0, None) else 0

# ------------------------------
# Charger performances_clean
# ------------------------------
print(" - Chargement des données...")
perf = pd.read_csv(PERF_CSV)

# Aggregation par joueur
agg = perf.groupby("player_id").agg({
    "minutes_played": "sum",
    "goals": "sum",
    "assists": "sum"
}).reset_index()

# Calcul KPIs
agg["nb_matches"] = agg["minutes_played"].apply(compute_nb_matches)

# Efficacité en pourcentage (buts + passes décisives par match × 100)
agg["efficiency"] = agg.apply(
    lambda r: safe_div(r["goals"] + r["assists"], r["nb_matches"]) * 100,
    axis=1
)

# Score global en pourcentage
agg["score_global"] = agg["efficiency"]

# Arrondir à 2 décimales
agg["efficiency"] = agg["efficiency"].round(2)
agg["score_global"] = agg["score_global"].round(2)

# ------------------------------
# Sauvegarde CSV
# ------------------------------
os.makedirs("data/processed", exist_ok=True)
agg.to_csv(OUTPUT_CSV, index=False)

print("✅ Fichier KPI généré :", OUTPUT_CSV)

# ------------------------------
# Connexion PostgreSQL
# ------------------------------
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    print("✅ Connexion PostgreSQL réussie !")
    
except psycopg2.OperationalError as e:
    print(f"❌ Erreur de connexion PostgreSQL : {e}")
    print(f"Vérifiez votre fichier .env et que PostgreSQL est démarré")
    exit(1)
    
except Exception as e:
    print(f"❌ Erreur inattendue : {e}")
    exit(1)

# ------------------------------
# Création table KPI
# ------------------------------
try:
    cur.execute("""
    CREATE TABLE IF NOT EXISTS players_kpis (
        player_id INT PRIMARY KEY REFERENCES players_clean(player_id),
        minutes_played INT,
        goals INT,
        assists INT,
        nb_matches INT,
        efficiency FLOAT,
        score_global FLOAT
    );
    """)
    print("✅ Table players_kpis prête")
    
    # On vide avant de réinsérer
    cur.execute("DELETE FROM players_kpis;")
    print(" Table vidée")
    
except psycopg2.Error as e:
    print(f"❌ Erreur lors de la création de la table : {e}")
    conn.rollback()
    cur.close()
    conn.close()
    exit(1)

# ------------------------------
# Insertion
# ------------------------------
try:
    inserted_count = 0
    for _, row in agg.iterrows():
        cur.execute("""
            INSERT INTO players_kpis (
                player_id, minutes_played, goals, assists, nb_matches, efficiency, score_global
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (player_id)
            DO UPDATE SET
                minutes_played = EXCLUDED.minutes_played,
                goals = EXCLUDED.goals,
                assists = EXCLUDED.assists,
                nb_matches = EXCLUDED.nb_matches,
                efficiency = EXCLUDED.efficiency,
                score_global = EXCLUDED.score_global;
        """, (
            int(row["player_id"]),
            int(row["minutes_played"]),
            int(row["goals"]),
            int(row["assists"]),
            int(row["nb_matches"]),
            float(row["efficiency"]),
            float(row["score_global"])
        ))
        inserted_count += 1
    
    conn.commit()
    print(f"✅ {inserted_count} KPIs insérés dans PostgreSQL")
    
except psycopg2.Error as e:
    print(f"❌ Erreur lors de l'insertion : {e}")
    conn.rollback()
    
except Exception as e:
    print(f"❌ Erreur inattendue lors de l'insertion : {e}")
    conn.rollback()
    
finally:
    cur.close()
    conn.close()
    print(" Connexion fermée")