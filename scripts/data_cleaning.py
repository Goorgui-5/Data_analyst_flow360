import os
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# ===============================================================
#  Jour 4 - Nettoyage et standardisation des données
# ===============================================================

# Charger les variables d'environnement
load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")

# ===============================================================
#  Connexion à la base PostgreSQL
# ===============================================================
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )
    print("Connexion PostgreSQL réussie !")
except Exception as e:
    print("❌ Erreur de connexion :", e)
    exit()

# ===============================================================
#  Chargement des tables dans des DataFrames
# ===============================================================
players_df = pd.read_sql("SELECT * FROM players", conn)
matches_df = pd.read_sql("SELECT * FROM matches", conn)
performances_df = pd.read_sql("SELECT * FROM performances", conn)

print(f" Players : {len(players_df)} lignes")
print(f" Matches : {len(matches_df)} lignes")
print(f" Performances : {len(performances_df)} lignes")

# ===============================================================
#  Nettoyage et standardisation
# ===============================================================

# ---- Supprimer doublons ----
players_df.drop_duplicates(subset=['name'], inplace=True)
matches_df.drop_duplicates(subset=['date', 'home_team', 'away_team'], inplace=True)
performances_df.drop_duplicates(subset=['player_id', 'match_id'], inplace=True)

# ---- Gérer valeurs manquantes ----
players_df.fillna({'position': 'Position: Attaquant', 'current_club': 'Non défini', 'current_competition':'Non défini', 'current_pays_de_competition':'Non défini'}, inplace=True)
matches_df.fillna({'competition': 'Inconnue'}, inplace=True)
performances_df.fillna({'minutes_played': 0, 'goals': 0, 'assists': 0}, inplace=True)

# ---- Uniformiser formats ----
players_df['name'] = players_df['name'].str.strip().str.title()
players_df['nationality'] = players_df['nationality'].str.strip().str.title()
players_df['current_club'] = players_df['current_club'].str.strip().str.title()
players_df['position'] = (players_df['position'].str.replace('Position:', '', regex=False).str.strip().str.lower())


matches_df['home_team'] = matches_df['home_team'].str.strip().str.title()
matches_df['away_team'] = matches_df['away_team'].str.strip().str.title()

# ---- Conversion des dates ----
players_df['birth_date'] = pd.to_datetime(players_df['birth_date'], errors='coerce')
matches_df['date'] = pd.to_datetime(matches_df['date'], errors='coerce')

# ---- Ajouter colonne saison ----
matches_df['saison'] = matches_df['date'].apply(lambda d: f"{d.year}/{d.year+1}" if pd.notnull(d) else None)

# ---- Enrichir performances avec position et club ----
performances_df = performances_df.merge(
    players_df[['player_id', 'position', 'current_club']],
    on='player_id',
    how='left'
)

# ===============================================================
#  Tests de cohérence
# ===============================================================

invalid_perf = performances_df[
    ~performances_df['player_id'].isin(players_df['player_id']) |
    ~performances_df['match_id'].isin(matches_df['match_id'])
]
if len(invalid_perf) > 0:
    print(f"⚠️ {len(invalid_perf)} performances non valides détectées (références inexistantes).")
else:
    print("✅ Toutes les performances ont des références valides.")

# Vérification des scores
if (matches_df['home_score'] < 0).any() or (matches_df['away_score'] < 0).any():
    print("⚠️ Attention : certains scores sont négatifs.")
else:
    print("✅ Scores cohérents (>= 0).")

# ===============================================================
#  Sauvegarde des données nettoyées
# ===============================================================

# --- Créer moteur SQLAlchemy ---
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

# --- Sauvegarde dans PostgreSQL ---
players_df.to_sql("players_clean", engine, if_exists="replace", index=False)
matches_df.to_sql("matches_clean", engine, if_exists="replace", index=False)
performances_df.to_sql("performances_clean", engine, if_exists="replace", index=False)

# --- Sauvegarde en CSV ---
os.makedirs("data", exist_ok=True)
players_df.to_csv("data/players_clean.csv", index=False)
matches_df.to_csv("data/matches_clean.csv", index=False)
performances_df.to_csv("data/performances_clean.csv", index=False)

print("\n✅ Données nettoyées et enregistrées avec succès !")
print("📁 Tables : players_clean, matches_clean, performances_clean")
print("📂 CSV : data/players_clean.csv, data/matches_clean.csv, data/performances_clean.csv")

# ===============================================================
#  Fermeture de la connexion
# ===============================================================
conn.close()
