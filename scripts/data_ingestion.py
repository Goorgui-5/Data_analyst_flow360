
"""Simple placeholder script for data ingestion."""
import os
from pathlib import Path
from dotenv import load_dotenv
import requests

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / '.env')

RAW_DIR = BASE_DIR / 'data' / 'raw'
RAW_DIR.mkdir(parents=True, exist_ok=True)

def fetch_sample_csv(url, dest_filename='sample_matches.csv'):
    dest = RAW_DIR / dest_filename
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        with open(dest, 'wb') as f:
            f.write(r.content)
        print(f"Saved sample data to {dest}")
    except Exception as e:
        print('Could not fetch sample CSV:', e)

def main():
    # placeholder: example public CSV (open data) - replace with real APIs
    sample_url = 'https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv'
    fetch_sample_csv(sample_url)

if __name__ == '__main__':
    main()
