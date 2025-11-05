import pandas as pd
import os

RAW_DIR = "data/raw/"

def validate_file(filepath):
    print(f"\n🔍 Validation du fichier : {filepath}")
    df = pd.read_csv(filepath)

    # Vérification de base
    print(f"- {len(df)} lignes, {len(df.columns)} colonnes")

    # Valeurs manquantes
    if df.isnull().values.any():
        print("⚠️  Valeurs manquantes détectées")
        print(df.isnull().sum())

    # Doublons
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print(f"⚠️  {duplicates} doublons trouvés")

    # Types de données
    print("Types de colonnes :")
    print(df.dtypes)

    print("✅ Validation terminée\n")

if __name__ == "__main__":
    for file in os.listdir(RAW_DIR):
        if file.endswith(".csv"):
            validate_file(os.path.join(RAW_DIR, file))
