import db

queries = []


queries.append("""
CREATE TABLE IF NOT EXISTS player(
    puuid TEXT,
    gameName TEXT,
    tagLine TEXT,
    level INT,
    rank TEXT,
    tier TEXT,
    PRIMARY KEY(puuid)
)
""")
queries.append("""
CREATE TABLE IF NOT EXISTS champion(
    championName TEXT,
    PRIMARY KEY(championName)
)
""")
queries.append(
"""
CREATE TABLE IF NOT EXISTS player_champion_mastery(
    puuid TEXT,
    championName TEXT,
    masteryPoints INT,
    PRIMARY KEY(puuid, championName),
    FOREIGN KEY(puuid) REFERENCES player(puuid),
    FOREIGN KEY(championName) REFERENCES champion(championName)
)
""")
for query in queries:
    res = db.execute_query(query)
    if res is not None:
        print(res)
    else:
        print("No results returned.")