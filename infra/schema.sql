
-- Exempe table pour joueurs
CREATE TABLE IF NOT EXISTS players (
    player_id SERIAL PRIMARY KEY,
    name TEXT,
    birth_date DATE,
    nationality TEXT,
    position TEXT,
    current_club TEXT
);

-- Exemple table pour matchs
CREATE TABLE IF NOT EXISTS matches (
    match_id SERIAL PRIMARY KEY,
    date DATE,
    competition TEXT,
    home_team TEXT,
    away_team TEXT,
    home_score INT,
    away_score INT
);

-- Exemple table pour performances des joueurs dans les matchs
CREATE TABLE IF NOT EXISTS performances (
    perf_id SERIAL PRIMARY KEY,
    player_id INT REFERENCES players(player_id),
    match_id INT REFERENCES matches(match_id),
    minutes_played INT,
    goals INT,
    assists INT
);
