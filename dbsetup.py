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
    foundTimestamp INT,
    lastExploredTimestamp INT,
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

queries.append(
"""
CREATE TABLE IF NOT EXISTS match(
    id TEXT,
    startTime INT,
    endTime INT,
    gameMode TEXT,
    discovererPuuid TEXT,
    PRIMARY KEY(id),
    FOREIGN KEY(discovererPuuid) REFERENCES player(puuid)
)
""")

queries.append(
"""
CREATE TABLE IF NOT EXISTS match_player(
    puuid TEXT,
    matchId TEXT,
    PRIMARY KEY(puuid, matchId),
    FOREIGN KEY(puuid) REFERENCES player(puuid),
    FOREIGN KEY(matchId) REFERENCES match(id)
)
""")

for query in queries:
    res = db.execute_query(query)
    if res["success"]:
        print("Query executed successfully")
    else:
        print(f"Error executing query: {res['error']}")