# import os
# import time
# import re
# import random
# import psycopg2
# from psycopg2.extras import execute_values
# import requests
# from bs4 import BeautifulSoup
# from dotenv import load_dotenv
# from tqdm import tqdm
# import pandas as pd
# from datetime import datetime

# # Charger les variables d'environnement
# load_dotenv()

# DB_USER = os.getenv("POSTGRES_USER")
# DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
# DB_NAME = os.getenv("POSTGRES_DB")
# DB_PORT = os.getenv("POSTGRES_PORT", 5432)

# # Liste de User-Agents pour rotation (simule différents navigateurs/utilisateurs)
# USER_AGENTS = [
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
#     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0',
# ]

# # Connexion à PostgreSQL
# def get_connection():
#     return psycopg2.connect(
#         dbname=DB_NAME,
#         user=DB_USER,
#         password=DB_PASSWORD,
#         host="localhost",
#         port=DB_PORT
#     )

# def get_random_headers():
#     """Génère des headers aléatoires pour simuler différents utilisateurs"""
#     return {
#         'User-Agent': random.choice(USER_AGENTS),
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
#         'Accept-Language': random.choice(['fr-FR,fr;q=0.9,en;q=0.8', 'en-US,en;q=0.9', 'fr;q=0.9,en-US;q=0.8,en;q=0.7']),
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Connection': 'keep-alive',
#         'Upgrade-Insecure-Requests': '1',
#         'Sec-Fetch-Dest': 'document',
#         'Sec-Fetch-Mode': 'navigate',
#         'Sec-Fetch-Site': 'none',
#         'Cache-Control': 'max-age=0',
#         'DNT': '1',
#     }

# def random_delay(min_seconds=3, max_seconds=7):
#     """Pause aléatoire pour simuler un comportement humain"""
#     delay = random.uniform(min_seconds, max_seconds)
#     time.sleep(delay)

# def clean_text(text):
#     """Nettoie le texte en supprimant les espaces superflus"""
#     if text:
#         return ' '.join(text.strip().split())
#     return None

# def parse_number(text):
#     """Extrait un nombre d'un texte, retourne 0 si pas de nombre"""
#     if not text:
#         return 0
    
#     # Enlever les espaces et tirets
#     text = text.strip().replace(' ', '').replace('\n', '')
    
#     # Si c'est un tiret seul, retourner 0
#     if text == '-' or text == '':
#         return 0
    
#     # Extraire le premier nombre trouvé
#     match = re.search(r'\d+', text)
#     if match:
#         return int(match.group())
    
#     return 0

# def parse_date(date_str):
#     """Parse les dates dans différents formats"""
#     if not date_str:
#         return None
    
#     # Format: "28 déc. 2004 (20)"
#     date_match = re.search(r'(\d{1,2})\s+(\w+\.?)\s+(\d{4})', date_str)
#     if date_match:
#         day, month_abbr, year = date_match.groups()
        
#         # Mapping des mois français
#         months_fr = {
#             'janv': '01', 'févr': '02', 'mars': '03', 'avr': '04',
#             'mai': '05', 'juin': '06', 'juil': '07', 'août': '08',
#             'sept': '09', 'oct': '10', 'nov': '11', 'déc': '12'
#         }
        
#         month_key = month_abbr.replace('.', '').lower()
#         month = months_fr.get(month_key, '01')
        
#         try:
#             return f"{year}-{month}-{day.zfill(2)}"
#         except:
#             return None
    
#     return None

# def get_player_info(url, session, retry=3):
#     """Récupère les informations du joueur depuis Transfermarkt"""
    
#     for attempt in range(retry):
#         try:
#             # Headers aléatoires à chaque tentative
#             headers = get_random_headers()
            
#             # Ajouter un délai aléatoire avant la requête (sauf première tentative)
#             if attempt > 0:
#                 print(f"   ⏳ Pause de {5 + attempt * 2}s avant nouvelle tentative...")
#                 time.sleep(5 + attempt * 2)
            
#             response = session.get(url, headers=headers, timeout=25)
#             response.raise_for_status()
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             # Nom du joueur
#             name = None
#             name_elem = soup.find("h1", class_="data-header__headline-wrapper")
#             if name_elem:
#                 # Enlever le numéro de maillot
#                 name_text = name_elem.get_text()
#                 name = re.sub(r'#\d+\s*', '', name_text).strip()
            
#             # Date de naissance
#             birth_date = None
#             birth_elem = soup.find("span", itemprop="birthDate")
#             if birth_elem:
#                 birth_date = parse_date(birth_elem.get_text())
            
#             # Alternative: chercher dans la page
#             if not birth_date:
#                 birth_match = re.search(r'(\d{1,2})\s+(\w+\.?)\s+(\d{4})\s*\((\d+)\)', soup.get_text())
#                 if birth_match:
#                     birth_date = parse_date(birth_match.group(0))
            
#             # Nationalité
#             nationality = None
#             nationality_elem = soup.find("span", itemprop="nationality")
#             if nationality_elem:
#                 nationality = clean_text(nationality_elem.get_text())
            
#             # Alternative pour la nationalité
#             if not nationality:
#                 flag_imgs = soup.find_all("img", class_="flaggenrahmen")
#                 for img in flag_imgs:
#                     alt_text = img.get('alt', '')
#                     if 'Sénégal' in alt_text or 'Senegal' in alt_text:
#                         nationality = 'Sénégal'
#                         break
            
#             # Position
#             position = None
#             # Chercher dans data-header__label
#             labels = soup.find_all("li", class_="data-header__label")
#             for label in labels:
#                 text = label.get_text()
#                 # Si ça contient "Arrière", "Milieu", "Attaquant", "Gardien"
#                 if any(keyword in text for keyword in ["Arrière", "Milieu", "Attaquant", "Gardien", "Défenseur"]):
#                     position = clean_text(text)
#                     break
            
#             # Club actuel
#             club = None
#             club_elem = soup.find("span", class_="data-header__club")
#             if club_elem:
#                 club_link = club_elem.find("a")
#                 if club_link:
#                     club = clean_text(club_link.get_text())
            
#             # Compétition actuelle (ligue du club)
#             competition = None
#             competition_pays = None
            
#             # Chercher dans la section data-header__club pour la ligue
#             if club_elem:
#                 # La ligue est souvent dans un span à côté du club
#                 parent_div = club_elem.find_parent("span", class_="data-header__club")
#                 if parent_div:
#                     # Chercher les images de drapeaux pour le pays
#                     flag_img = parent_div.find("img", class_="flaggenrahmen")
#                     if flag_img and flag_img.get('title'):
#                         competition_pays = clean_text(flag_img.get('title'))
                    
#                     # Chercher le lien de la compétition
#                     comp_links = parent_div.find_all("a")
#                     for link in comp_links:
#                         link_text = clean_text(link.get_text())
#                         # Si le lien contient "Ligue", "League", "Championship", etc.
#                         if link_text and any(keyword in link_text for keyword in 
#                             ["Ligue", "League", "Liga", "Championship", "Serie", "Bundesliga", 
#                              "Première", "Division", "Super Lig", "Eredivisie"]):
#                             competition = link_text
#                             break
            
#             # Alternative: chercher dans le tableau info-table
#             if not competition or not competition_pays:
#                 info_table = soup.find("div", class_="info-table")
#                 if info_table:
#                     # Chercher les lignes du tableau
#                     rows = info_table.find_all("span", class_="info-table__content")
#                     for i, row in enumerate(rows):
#                         text = clean_text(row.get_text())
                        
#                         # Chercher le pays dans les drapeaux
#                         if not competition_pays:
#                             flag = row.find("img", class_="flaggenrahmen")
#                             if flag and flag.get('title'):
#                                 # Exclure la nationalité du joueur
#                                 flag_title = flag.get('title')
#                                 if flag_title and flag_title not in ['Sénégal', nationality]:
#                                     competition_pays = clean_text(flag_title)
                        
#                         # Chercher la compétition
#                         if text and any(keyword in text for keyword in 
#                             ["Ligue", "League", "Liga", "Championship", "Serie", "Bundesliga"]):
#                             competition = text
            
#             return {
#                 "name": name,
#                 "birth_date": birth_date,
#                 "nationality": nationality,
#                 "position": position,
#                 "current_club": club,
#                 "current_competition": competition,
#                 "current_pays_de_competition": competition_pays,
#                 "url": url
#             }
        
#         except requests.exceptions.Timeout:
#             if attempt < retry - 1:
#                 print(f"   ⏱️  Timeout (tentative {attempt + 1}/{retry})")
#                 continue
#             else:
#                 print(f"   ❌ Timeout après {retry} tentatives")
#                 return None
        
#         except requests.exceptions.RequestException as e:
#             if attempt < retry - 1:
#                 print(f"   ⚠️  Erreur réseau (tentative {attempt + 1}/{retry})")
#                 continue
#             else:
#                 print(f"   ❌ Erreur réseau: {type(e).__name__}")
#                 return None
        
#         except Exception as e:
#             print(f"   ❌ Erreur: {type(e).__name__}")
#             return None
    
#     return None

# def get_player_stats(url, session, retry=3):
#     """Récupère les statistiques de la saison EN COURS (2024/25 ou 2025/26)"""
    
#     # URL de la page des performances pour la saison 2024/25
#     # Transfermarkt utilise l'année de début de saison (2024 pour 2024/25)
#     stats_url = url.replace('/profil/', '/leistungsdatendetails/')
#     stats_url = stats_url + '/saison/2024/verein/0/liga/0/wettbewerb//pos/0/trainer_id/0/plus/1'
    
#     for attempt in range(retry):
#         try:
#             # Headers aléatoires à chaque tentative
#             headers = get_random_headers()
            
#             # Ajouter un petit délai aléatoire entre info et stats (comportement humain)
#             random_delay(2, 4)
            
#             if attempt > 0:
#                 print(f"   ⏳ Pause de {5 + attempt * 2}s avant nouvelle tentative...")
#                 time.sleep(5 + attempt * 2)
            
#             response = session.get(stats_url, headers=headers, timeout=25)
#             response.raise_for_status()
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             # Chercher le tableau avec la classe 'items'
#             table = soup.find("table", class_="items")
            
#             if not table:
#                 print("   ⚠️  Pas de données pour saison 2024/25")
#                 return None
            
#             # Vérifier qu'on a bien des données pour la saison en cours
#             season_header = soup.find("div", class_="viewport-tracking")
            
#             # Chercher d'abord dans le FOOTER (contient les totaux de la saison)
#             footer = table.find("tfoot")
            
#             if footer:
#                 cells = footer.find_all("td")
#                 footer_values = [clean_text(c.get_text()) for c in cells]
                
#                 # Structure du footer Transfermarkt:
#                 # ['', 'Total:', '', '', '176', '169', '1,38', '64', '9', '-', '73', '42', '6', '-', '2', '6', "146'", "9.326'"]
#                 # Index typiques: 4=Matchs, 7=Buts, 8=Passes décisives
                
#                 total_matches = 0
#                 total_goals = 0
#                 total_assists = 0
                
#                 # Trouver les indices des statistiques
#                 for i, val in enumerate(footer_values):
#                     num = parse_number(val)
                    
#                     # Les matchs sont généralement à l'index 4
#                     if i == 4 and num > 0:
#                         total_matches = num
#                     # Les buts à l'index 7
#                     elif i == 7 and num >= 0:
#                         total_goals = num
#                     # Les passes à l'index 8
#                     elif i == 8 and num >= 0:
#                         total_assists = num
                
#                 if total_matches > 0:
#                     print(f"   ⚽ Saison 2024/25: {total_matches} matchs | {total_goals} buts | {total_assists} passes")
                    
#                     return {
#                         "matches_played": total_matches,
#                         "goals": total_goals,
#                         "assists": total_assists,
#                         "minutes_played": total_matches * 90,
#                         "season": "2024/25"
#                     }
            
#             # Fallback: lire le tbody si pas de footer
#             tbody = table.find("tbody")
#             if tbody:
#                 rows = tbody.find_all("tr")
                
#                 total_matches = 0
#                 total_goals = 0
#                 total_assists = 0
                
#                 for row in rows:
#                     cells = row.find_all("td")
                    
#                     if len(cells) >= 5:
#                         matches = parse_number(cells[1].get_text())
#                         goals = parse_number(cells[3].get_text())
#                         assists = parse_number(cells[4].get_text())
                        
#                         total_matches += matches
#                         total_goals += goals
#                         total_assists += assists
                
#                 if total_matches > 0:
#                     print(f"   ⚽ Saison 2024/25: {total_matches} matchs | {total_goals} buts | {total_assists} passes")
                    
#                     return {
#                         "matches_played": total_matches,
#                         "goals": total_goals,
#                         "assists": total_assists,
#                         "minutes_played": total_matches * 90,
#                         "season": "2024/25"
#                     }
            
#             print("   ⚠️  Pas de stats pour saison 2024/25")
#             return None
        
#         except requests.exceptions.Timeout:
#             if attempt < retry - 1:
#                 print(f"   ⏱️  Timeout stats (tentative {attempt + 1}/{retry})")
#                 continue
#             else:
#                 print(f"   ❌ Timeout stats après {retry} tentatives")
#                 return None
        
#         except requests.exceptions.RequestException as e:
#             if attempt < retry - 1:
#                 print(f"   ⚠️  Erreur réseau stats (tentative {attempt + 1}/{retry})")
#                 continue
#             else:
#                 print(f"   ❌ Erreur réseau stats: {type(e).__name__}")
#                 return None
        
#         except Exception as e:
#             print(f"   ❌ Erreur stats: {type(e).__name__}")
#             return None
    
#     return None

# def upsert_player(conn, info, stats):
#     """Insère ou met à jour un joueur dans la base de données"""
#     if not info or not info.get('name'):
#         print("   ⚠️  Informations incomplètes")
#         return
    
#     try:
#         with conn.cursor() as cur:
#             # Vérifier si le joueur existe
#             cur.execute(
#                 "SELECT player_id FROM players WHERE name = %s",
#                 (info["name"],)
#             )
#             player = cur.fetchone()
            
#             if player:
#                 player_id = player[0]
                
#                 # Mettre à jour les infos du joueur
#                 cur.execute("""
#                     UPDATE players 
#                     SET birth_date = COALESCE(%s, birth_date),
#                         nationality = COALESCE(%s, nationality),
#                         position = COALESCE(%s, position),
#                         current_club = COALESCE(%s, current_club),
#                         current_competition = COALESCE(%s, current_competition),
#                         current_pays_de_competition = COALESCE(%s, current_pays_de_competition)
#                     WHERE player_id = %s
#                 """, (
#                     info["birth_date"],
#                     info["nationality"],
#                     info["position"],
#                     info["current_club"],
#                     info["current_competition"],
#                     info["current_pays_de_competition"],
#                     player_id
#                 ))
                
#                 # Vérifier si une performance agrégée existe déjà
#                 if stats:
#                     cur.execute("""
#                         SELECT perf_id FROM performances 
#                         WHERE player_id = %s AND match_id IS NULL
#                     """, (player_id,))
                    
#                     existing_perf = cur.fetchone()
                    
#                     if existing_perf:
#                         # Mettre à jour
#                         cur.execute("""
#                             UPDATE performances
#                             SET goals = %s,
#                                 assists = %s,
#                                 minutes_played = %s
#                             WHERE perf_id = %s
#                         """, (
#                             stats["goals"],
#                             stats["assists"],
#                             stats["minutes_played"],
#                             existing_perf[0]
#                         ))
#                     else:
#                         # Créer
#                         cur.execute("""
#                             INSERT INTO performances (player_id, match_id, minutes_played, goals, assists)
#                             VALUES (%s, NULL, %s, %s, %s)
#                         """, (
#                             player_id,
#                             stats["minutes_played"],
#                             stats["goals"],
#                             stats["assists"]
#                         ))
#             else:
#                 # Insérer un nouveau joueur
#                 cur.execute("""
#                     INSERT INTO players (name, birth_date, nationality, position, current_club, 
#                                        current_competition, current_pays_de_competition)
#                     VALUES (%s, %s, %s, %s, %s, %s, %s)
#                     RETURNING player_id
#                 """, (
#                     info["name"],
#                     info["birth_date"],
#                     info["nationality"],
#                     info["position"],
#                     info["current_club"],
#                     info["current_competition"],
#                     info["current_pays_de_competition"]
#                 ))
#                 player_id = cur.fetchone()[0]
                
#                 # Insérer les stats
#                 if stats:
#                     cur.execute("""
#                         INSERT INTO performances (player_id, match_id, minutes_played, goals, assists)
#                         VALUES (%s, NULL, %s, %s, %s)
#                     """, (
#                         player_id,
#                         stats["minutes_played"],
#                         stats["goals"],
#                         stats["assists"]
#                     ))
        
#         conn.commit()
#         print(f"   ✅ Enregistré")
        
#     except Exception as e:
#         conn.rollback()
#         print(f"   ❌ Erreur DB: {type(e).__name__}")
#         raise

# def scrape_all_players():
#     """Fonction principale de scraping"""
#     conn = get_connection()
    
#     # Créer une session pour réutiliser les connexions (plus réaliste)
#     session = requests.Session()
    
#     # CSV avec les URLs
#     players_csv = "data/raw/senegal_players_list.csv"
    
#     if not os.path.exists(players_csv):
#         print(f"❌ Fichier {players_csv} introuvable")
#         return
    
#     df_urls = pd.read_csv(players_csv)
#     print(f"\n{'='*70}")
#     print(f"🚀 SCRAPING TRANSFERMARKT - JOUEURS SÉNÉGALAIS")
#     print(f"{'='*70}")
#     print(f"📋 {len(df_urls)} joueurs à traiter")
#     print(f"📅 Saison ciblée: 2024/25")
#     print(f"🎭 Rotation de {len(USER_AGENTS)} User-Agents")
#     print(f"⏱️  Délais aléatoires: 3-7 secondes entre requêtes\n")
    
#     success_count = 0
#     error_count = 0
#     skipped_count = 0
    
#     for idx, row in df_urls.iterrows():
#         url = row["url"]
        
#         print(f"\n{'─'*70}")
#         print(f"[{idx+1}/{len(df_urls)}] 🔗 Traitement...")
        
#         try:
#             # Récupérer les infos
#             info = get_player_info(url, session)
            
#             if not info or not info.get('name'):
#                 print(f"   ⏭️  Ignoré: infos manquantes")
#                 error_count += 1
#                 random_delay(2, 4)  # Pause même en cas d'erreur
#                 continue
            
#             print(f"   👤 {info['name']}")
#             if info.get('current_competition'):
#                 print(f"   🏆 {info['current_competition']} ({info.get('current_pays_de_competition', 'N/A')})")
            
#             # Vérifier la nationalité
#             if info["nationality"] and "Sénégal" in info["nationality"]:
#                 # Récupérer les stats
#                 stats = get_player_stats(url, session)
                
#                 # Insérer dans la base
#                 upsert_player(conn, info, stats)
#                 success_count += 1
#             else:
#                 print(f"   ⏭️  Autre nationalité: {info.get('nationality', 'N/A')}")
#                 skipped_count += 1
        
#         except Exception as e:
#             print(f"   ❌ Erreur: {type(e).__name__}")
#             error_count += 1
        
#         # Pause aléatoire entre joueurs (simule comportement humain)
#         if idx < len(df_urls) - 1:  # Pas de pause après le dernier
#             delay = random.uniform(4, 8)
#             print(f"   ⏳ Pause de {delay:.1f}s avant le prochain joueur...")
#             time.sleep(delay)
    
#     session.close()
#     conn.close()
    
#     print(f"\n{'='*70}")
#     print(f"✅ SCRAPING TERMINÉ!")
#     print(f"{'='*70}")
#     print(f"   ✓ Succès:              {success_count} joueurs")
#     print(f"   ⊘ Autre nationalité:   {skipped_count} joueurs")
#     print(f"   ✗ Erreurs:             {error_count} joueurs")
#     print(f"{'='*70}\n")

# if __name__ == "__main__":
#     scrape_all_players()

import os
import time
import re
import random
import psycopg2
from psycopg2.extras import execute_values
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from tqdm import tqdm
import pandas as pd
from datetime import datetime

# Charger les variables d'environnement
load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PORT = os.getenv("POSTGRES_PORT", 5432)

# Liste de User-Agents pour rotation (simule différents navigateurs/utilisateurs)
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0',
]

# Connexion à PostgreSQL
def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host="localhost",
        port=DB_PORT
    )

def get_random_headers():
    """Génère des headers aléatoires pour simuler différents utilisateurs"""
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': random.choice(['fr-FR,fr;q=0.9,en;q=0.8', 'en-US,en;q=0.9', 'fr;q=0.9,en-US;q=0.8,en;q=0.7']),
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
    }

def random_delay(min_seconds=3, max_seconds=7):
    """Pause aléatoire pour simuler un comportement humain"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def clean_text(text):
    """Nettoie le texte en supprimant les espaces superflus"""
    if text:
        return ' '.join(text.strip().split())
    return None

def parse_number(text):
    """Extrait un nombre d'un texte, retourne 0 si pas de nombre"""
    if not text:
        return 0
    
    # Enlever les espaces et tirets
    text = text.strip().replace(' ', '').replace('\n', '')
    
    # Si c'est un tiret seul, retourner 0
    if text == '-' or text == '':
        return 0
    
    # Extraire le premier nombre trouvé
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
    
    return 0

def parse_date(date_str):
    """Parse les dates dans différents formats"""
    if not date_str:
        return None
    
    # Format: "28 déc. 2004 (20)"
    date_match = re.search(r'(\d{1,2})\s+(\w+\.?)\s+(\d{4})', date_str)
    if date_match:
        day, month_abbr, year = date_match.groups()
        
        # Mapping des mois français
        months_fr = {
            'janv': '01', 'févr': '02', 'mars': '03', 'avr': '04',
            'mai': '05', 'juin': '06', 'juil': '07', 'août': '08',
            'sept': '09', 'oct': '10', 'nov': '11', 'déc': '12'
        }
        
        month_key = month_abbr.replace('.', '').lower()
        month = months_fr.get(month_key, '01')
        
        try:
            return f"{year}-{month}-{day.zfill(2)}"
        except:
            return None
    
    return None

def get_player_info(url, session, retry=3):
    """Récupère les informations du joueur depuis Transfermarkt"""
    
    for attempt in range(retry):
        try:
            # Headers aléatoires à chaque tentative
            headers = get_random_headers()
            
            # Ajouter un délai aléatoire avant la requête (sauf première tentative)
            if attempt > 0:
                print(f"   ⏳ Pause de {5 + attempt * 2}s avant nouvelle tentative...")
                time.sleep(5 + attempt * 2)
            
            response = session.get(url, headers=headers, timeout=25)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Nom du joueur
            name = None
            name_elem = soup.find("h1", class_="data-header__headline-wrapper")
            if name_elem:
                # Enlever le numéro de maillot
                name_text = name_elem.get_text()
                name = re.sub(r'#\d+\s*', '', name_text).strip()
            
            # Date de naissance
            birth_date = None
            birth_elem = soup.find("span", itemprop="birthDate")
            if birth_elem:
                birth_date = parse_date(birth_elem.get_text())
            
            # Alternative: chercher dans la page
            if not birth_date:
                birth_match = re.search(r'(\d{1,2})\s+(\w+\.?)\s+(\d{4})\s*\((\d+)\)', soup.get_text())
                if birth_match:
                    birth_date = parse_date(birth_match.group(0))
            
            # Nationalité
            nationality = None
            nationality_elem = soup.find("span", itemprop="nationality")
            if nationality_elem:
                nationality = clean_text(nationality_elem.get_text())
            
            # Alternative pour la nationalité
            if not nationality:
                flag_imgs = soup.find_all("img", class_="flaggenrahmen")
                for img in flag_imgs:
                    alt_text = img.get('alt', '')
                    if 'Sénégal' in alt_text or 'Senegal' in alt_text:
                        nationality = 'Sénégal'
                        break
            
            # Position
            position = None
            # Chercher dans data-header__label
            labels = soup.find_all("li", class_="data-header__label")
            for label in labels:
                text = label.get_text()
                # Si ça contient "Arrière", "Milieu", "Attaquant", "Gardien"
                if any(keyword in text for keyword in ["Arrière", "Milieu", "Attaquant", "Gardien", "Défenseur"]):
                    position = clean_text(text)
                    break
            
            # === Club actuel ===
            club = None
            club_elem = soup.find("span", class_="data-header__club")
            if club_elem:
                club_link = club_elem.find("a")
                if club_link:
                    club = clean_text(club_link.get_text())
            
            # # === Compétition et pays (SECTION SÉPARÉE) ===
            # competition = None
            # competition_pays = None
            
            # # 🎯 MÉTHODE PRINCIPALE : Chercher dans data-header__league
            # league_elem = soup.find("span", class_="data-header__league")
            # if league_elem:
            #     # Récupérer le lien de la compétition
            #     league_link = league_elem.find("a", class_="data-header__league-link")
            #     if league_link:
            #         competition = clean_text(league_link.get_text())
                
            #     # Récupérer le drapeau du pays
            #     flag_img = league_elem.find("img", class_="flaggenrahmen")
            #     if flag_img:
            #         flag_title = clean_text(flag_img.get('title'))
            #         # Vérifier que ce n'est pas la nationalité du joueur
            #         if flag_title and flag_title != nationality and flag_title != 'Sénégal':
            #             competition_pays = flag_title

            # === Compétition et pays (SECTION SÉPARÉE) ===
            competition = None
            competition_pays = None

            # # 1️⃣ Chercher la compétition (comme avant)
            # league_elem = soup.find("span", class_="data-header__league")
            # if league_elem:
            #     league_link = league_elem.find("a", class_="data-header__league-link")
            #     if league_link:
            #         competition = clean_text(league_link.get_text())

            # # 2️⃣ Chercher le pays du championnat (section "Pays/Ligue")
            # pays_label = soup.find("span", string=lambda t: t and "Pays/Ligue" in t)
            # if pays_label:
            #     content_span = pays_label.find_next("span", class_="data-header__content")
            #     if content_span:
            #         img = content_span.find("img", class_="flaggenrahmen")
            #         if img and img.get("title"):
            #             competition_pays = clean_text(img["title"])

            club_elem = soup.find("span", class_="data-header__club")
            if club_elem:
                club_link = club_elem.find("a")
                if club_link:
                    club = clean_text(club_link.get_text())

                    # 👉 Aller sur la page du club pour extraire la compétition et le pays
                    club_url = "https://www.transfermarkt.fr" + club_link["href"]
                    headers = get_random_headers()
                    random_delay(2, 4)
                    club_resp = session.get(club_url, headers=headers, timeout=25)

                    if club_resp.status_code == 200:
                        club_soup = BeautifulSoup(club_resp.text, "html.parser")

                        # === Trouver la compétition actuelle du club ===
                        comp_elem = club_soup.find("span", class_="data-header__club")
                        if not comp_elem:
                            comp_elem = club_soup.find("span", class_="data-header__league")
                        
                        if comp_elem:
                            comp_link = comp_elem.find("a")
                            if comp_link:
                                competition = clean_text(comp_link.get_text())

                                # Trouver le drapeau du club → vrai pays du club
                                flag = club_soup.find("img", class_="flaggenrahmen")
                                if flag and flag.get("title"):
                                    competition_pays = clean_text(flag.get("title"))
                                else:
                                    # Si le drapeau du club n’est pas trouvé, on va chercher dans la compétition
                                    comp_url = "https://www.transfermarkt.fr" + comp_link["href"]
                                    random_delay(2, 4)
                                    comp_resp = session.get(comp_url, headers=get_random_headers(), timeout=25)
                                    if comp_resp.status_code == 200:
                                        comp_soup = BeautifulSoup(comp_resp.text, "html.parser")
                                        flag = comp_soup.find("img", class_="flaggenrahmen")
                                        if flag and flag.get("title"):
                                            competition_pays = clean_text(flag.get("title"))

            
            return {
                "name": name,
                "birth_date": birth_date,
                "nationality": nationality,
                "position": position,
                "current_club": club,
                "current_competition": competition,
                "current_pays_de_competition": competition_pays,
                "url": url
            }
        
        except requests.exceptions.Timeout:
            if attempt < retry - 1:
                print(f"   ⏱️  Timeout (tentative {attempt + 1}/{retry})")
                continue
            else:
                print(f"   ❌ Timeout après {retry} tentatives")
                return None
        
        except requests.exceptions.RequestException as e:
            if attempt < retry - 1:
                print(f"   ⚠️  Erreur réseau (tentative {attempt + 1}/{retry})")
                continue
            else:
                print(f"   ❌ Erreur réseau: {type(e).__name__}")
                return None
        
        except Exception as e:
            print(f"   ❌ Erreur: {type(e).__name__}")
            return None
    
    return None

def get_player_stats(url, session, retry=3):
    """Récupère TOUTES les statistiques du joueur (carrière complète)"""
    
    # URL de la page des performances TOUTES SAISONS confondues
    stats_url = url.replace('/profil/', '/leistungsdatendetails/')
    stats_url = stats_url + '/saison//verein/0/liga/0/wettbewerb//pos/0/trainer_id/0/plus/1'
    
    for attempt in range(retry):
        try:
            # Headers aléatoires à chaque tentative
            headers = get_random_headers()
            
            # Ajouter un petit délai aléatoire entre info et stats (comportement humain)
            random_delay(2, 4)
            
            if attempt > 0:
                print(f"   ⏳ Pause de {5 + attempt * 2}s avant nouvelle tentative...")
                time.sleep(5 + attempt * 2)
            
            response = session.get(stats_url, headers=headers, timeout=25)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Chercher le tableau avec la classe 'items'
            table = soup.find("table", class_="items")
            
            if not table:
                print("   ⚠️  Tableau de statistiques non trouvé")
                return None
            
            # Chercher d'abord dans le FOOTER (contient les totaux de TOUTE LA CARRIÈRE)
            footer = table.find("tfoot")
            
            if footer:
                cells = footer.find_all("td")
                footer_values = [clean_text(c.get_text()) for c in cells]
                
                # Structure du footer Transfermarkt:
                # ['', 'Total:', '', '', '176', '169', '1,38', '64', '9', '-', '73', '42', '6', '-', '2', '6', "146'", "9.326'"]
                # Index typiques: 4=Matchs, 7=Buts, 8=Passes décisives
                
                total_matches = 0
                total_goals = 0
                total_assists = 0
                
                # Trouver les indices des statistiques
                for i, val in enumerate(footer_values):
                    num = parse_number(val)
                    
                    # Les matchs sont généralement à l'index 4
                    if i == 4 and num > 0:
                        total_matches = num
                    # Les buts à l'index 7
                    elif i == 7 and num >= 0:
                        total_goals = num
                    # Les passes à l'index 8
                    elif i == 8 and num >= 0:
                        total_assists = num
                
                if total_matches > 0:
                    print(f"   ⚽ Carrière: {total_matches} matchs | {total_goals} buts | {total_assists} passes")
                    
                    return {
                        "matches_played": total_matches,
                        "goals": total_goals,
                        "assists": total_assists,
                        "minutes_played": total_matches * 90
                    }
            
            # Fallback: lire le tbody si pas de footer
            tbody = table.find("tbody")
            if tbody:
                rows = tbody.find_all("tr")
                
                total_matches = 0
                total_goals = 0
                total_assists = 0
                
                for row in rows:
                    cells = row.find_all("td")
                    
                    if len(cells) >= 5:
                        matches = parse_number(cells[1].get_text())
                        goals = parse_number(cells[3].get_text())
                        assists = parse_number(cells[4].get_text())
                        
                        total_matches += matches
                        total_goals += goals
                        total_assists += assists
                
                if total_matches > 0:
                    print(f"   ⚽ Carrière: {total_matches} matchs | {total_goals} buts | {total_assists} passes")
                    
                    return {
                        "matches_played": total_matches,
                        "goals": total_goals,
                        "assists": total_assists,
                        "minutes_played": total_matches * 90
                    }
            
            print("   ⚠️  Aucune statistique disponible")
            return None
        
        except requests.exceptions.Timeout:
            if attempt < retry - 1:
                print(f"   ⏱️  Timeout stats (tentative {attempt + 1}/{retry})")
                continue
            else:
                print(f"   ❌ Timeout stats après {retry} tentatives")
                return None
        
        except requests.exceptions.RequestException as e:
            if attempt < retry - 1:
                print(f"   ⚠️  Erreur réseau stats (tentative {attempt + 1}/{retry})")
                continue
            else:
                print(f"   ❌ Erreur réseau stats: {type(e).__name__}")
                return None
        
        except Exception as e:
            print(f"   ❌ Erreur stats: {type(e).__name__}")
            return None
    
    return None

def upsert_player(conn, info, stats):
    """Insère ou met à jour un joueur dans la base de données"""
    if not info or not info.get('name'):
        print("   ⚠️  Informations incomplètes")
        return
    
    try:
        with conn.cursor() as cur:
            # Vérifier si le joueur existe
            cur.execute(
                "SELECT player_id FROM players WHERE name = %s",
                (info["name"],)
            )
            player = cur.fetchone()
            
            if player:
                player_id = player[0]
                
                # Mettre à jour les infos du joueur
                cur.execute("""
                    UPDATE players 
                    SET birth_date = COALESCE(%s, birth_date),
                        nationality = COALESCE(%s, nationality),
                        position = COALESCE(%s, position),
                        current_club = COALESCE(%s, current_club),
                        current_competition = COALESCE(%s, current_competition),
                        current_pays_de_competition = COALESCE(%s, current_pays_de_competition)
                    WHERE player_id = %s
                """, (
                    info["birth_date"],
                    info["nationality"],
                    info["position"],
                    info["current_club"],
                    info["current_competition"],
                    info["current_pays_de_competition"],
                    player_id
                ))
                
                # Vérifier si une performance agrégée existe déjà
                if stats:
                    cur.execute("""
                        SELECT perf_id FROM performances 
                        WHERE player_id = %s AND match_id IS NULL
                    """, (player_id,))
                    
                    existing_perf = cur.fetchone()
                    
                    if existing_perf:
                        # Mettre à jour
                        cur.execute("""
                            UPDATE performances
                            SET goals = %s,
                                assists = %s,
                                minutes_played = %s
                            WHERE perf_id = %s
                        """, (
                            stats["goals"],
                            stats["assists"],
                            stats["minutes_played"],
                            existing_perf[0]
                        ))
                    else:
                        # Créer
                        cur.execute("""
                            INSERT INTO performances (player_id, match_id, minutes_played, goals, assists)
                            VALUES (%s, NULL, %s, %s, %s)
                        """, (
                            player_id,
                            stats["minutes_played"],
                            stats["goals"],
                            stats["assists"]
                        ))
            else:
                # Insérer un nouveau joueur
                cur.execute("""
                    INSERT INTO players (name, birth_date, nationality, position, current_club, 
                                       current_competition, current_pays_de_competition)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING player_id
                """, (
                    info["name"],
                    info["birth_date"],
                    info["nationality"],
                    info["position"],
                    info["current_club"],
                    info["current_competition"],
                    info["current_pays_de_competition"]
                ))
                player_id = cur.fetchone()[0]
                
                # Insérer les stats
                if stats:
                    cur.execute("""
                        INSERT INTO performances (player_id, match_id, minutes_played, goals, assists)
                        VALUES (%s, NULL, %s, %s, %s)
                    """, (
                        player_id,
                        stats["minutes_played"],
                        stats["goals"],
                        stats["assists"]
                    ))
        
        conn.commit()
        print(f"   ✅ Enregistré")
        
    except Exception as e:
        conn.rollback()
        print(f"   ❌ Erreur DB: {type(e).__name__}")
        raise

def scrape_all_players():
    """Fonction principale de scraping"""
    conn = get_connection()
    
    # Créer une session pour réutiliser les connexions (plus réaliste)
    session = requests.Session()
    
    # CSV avec les URLs
    players_csv = "data/raw/senegal_players_list.csv"
    
    if not os.path.exists(players_csv):
        print(f"❌ Fichier {players_csv} introuvable")
        return
    
    df_urls = pd.read_csv(players_csv)
    print(f"\n{'='*70}")
    print(f"🚀 SCRAPING TRANSFERMARKT - JOUEURS SÉNÉGALAIS")
    print(f"{'='*70}")
    print(f"📋 {len(df_urls)} joueurs à traiter")
    print(f"📅 Saison ciblée: 2024/25")
    print(f"🎭 Rotation de {len(USER_AGENTS)} User-Agents")
    print(f"⏱️  Délais aléatoires: 3-7 secondes entre requêtes\n")
    
    success_count = 0
    error_count = 0
    skipped_count = 0
    
    for idx, row in df_urls.iterrows():
        url = row["url"]
        
        print(f"\n{'─'*70}")
        print(f"[{idx+1}/{len(df_urls)}] 🔗 Traitement...")
        
        try:
            # Récupérer les infos
            info = get_player_info(url, session)
            
            if not info or not info.get('name'):
                print(f"   ⏭️  Ignoré: infos manquantes")
                error_count += 1
                random_delay(2, 4)  # Pause même en cas d'erreur
                continue
            
            print(f"   👤 {info['name']}")
            if info.get('current_competition') or info.get('current_pays_de_competition'):
                comp = info.get('current_competition', 'N/A')
                pays = info.get('current_pays_de_competition', 'N/A')
                print(f"   🏆 {comp} - {pays}")
            
            # Vérifier la nationalité
            if info["nationality"] and "Sénégal" in info["nationality"]:
                # Récupérer les stats
                stats = get_player_stats(url, session)
                
                # Insérer dans la base
                upsert_player(conn, info, stats)
                success_count += 1
            else:
                print(f"   ⏭️  Autre nationalité: {info.get('nationality', 'N/A')}")
                skipped_count += 1
        
        except Exception as e:
            print(f"   ❌ Erreur: {type(e).__name__}")
            error_count += 1
        
        # Pause aléatoire entre joueurs (simule comportement humain)
        if idx < len(df_urls) - 1:  # Pas de pause après le dernier
            delay = random.uniform(4, 8)
            print(f"   ⏳ Pause de {delay:.1f}s avant le prochain joueur...")
            time.sleep(delay)
    
    session.close()
    conn.close()
    
    print(f"\n{'='*70}")
    print(f"✅ SCRAPING TERMINÉ!")
    print(f"{'='*70}")
    print(f"   ✓ Succès:              {success_count} joueurs")
    print(f"   ⊘ Autre nationalité:   {skipped_count} joueurs")
    print(f"   ✗ Erreurs:             {error_count} joueurs")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    scrape_all_players()