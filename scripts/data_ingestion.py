import requests
import os
import json
from dotenv import load_dotenv
from pathlib import Path

# Charger les variables d'environnement
load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")

BASE_URL = "https://api-football-v1.p.rapidapi.com/v3/"
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}


def fetch_players(league_id=39, season=2020, page=1):
    """Récupère les joueurs d'une ligue et saison"""
    url = f"{BASE_URL}players"
    params = {"league": league_id, "season": season, "page": page}
    r = requests.get(url, headers=HEADERS, params=params)
    if r.status_code == 200:
        data = r.json()
        file_path = RAW_DIR / f"players_league{league_id}_season{season}_page{page}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"✅ Données sauvegardées dans {file_path}")
        return data
    else:
        print(f"❌ Erreur {r.status_code}: {r.text}")
        return None


if __name__ == "__main__":
    print("Récupération des joueurs (Premier League 2020)...")
    fetch_players(league_id=39, season=2020)
