
# DataAnalystFlow360 – Football Sénégalais

## Objectif
Développer un pipeline data complet et automatisé pour collecter, transformer et visualiser les performances des joueurs sénégalais.

## Structure du projet
- data/raw/           : données brutes
- data/processed/     : données transformées prêtes à l'analyse
- notebooks/          : notebooks d'exploration (EDA)
- scripts/            : scripts Python (ingestion, nettoyage, transformation)
- infra/              : fichiers d'infrastructure (docker-compose, sql)
- docs/               : documentation, diagrammes, etc.
- .github/workflows/  : CI/CD GitHub Actions

## Quickstart (local)
1. Copier `.env.example` vers `.env` et remplir les valeurs :
   ```bash
   cp .env.example .env
   ```

2. Démarrer les services Docker (Postgres) :
   ```bash
   docker-compose up -d
   ```

3. Installer dépendances Python (préparer un venv) :
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. Lancer l'ingestion (exemple) :
   ```bash
   python scripts/data_ingestion.py
   ```

## Architecture (résumé)
Collecte -> Transformation (ETL) -> Data Warehouse (Postgres/BigQuery) -> BI (Power BI/Streamlit) -> CI/CD & Monitoring

## Licence
MIT
