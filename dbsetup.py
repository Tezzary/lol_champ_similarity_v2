import db
import requests
queries = []

DATA_DRAGON_VERSION = "15.10.1"

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
    id INT,
    championName TEXT,
    PRIMARY KEY(id)
)
""")

queries.append(
"""
CREATE TABLE IF NOT EXISTS player_champion_mastery(
    puuid TEXT,
    championId INT,
    masteryPoints INT,
    masteryLevel INT,
    PRIMARY KEY(puuid, championId),
    FOREIGN KEY(puuid) REFERENCES player(puuid),
    FOREIGN KEY(championId) REFERENCES champion(id)
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


#Adding champions to the database from the Riot Data Dragon API
url = f"https://ddragon.leagueoflegends.com/cdn/{DATA_DRAGON_VERSION}/data/en_US/champion.json"
result = requests.get(url)
if result.status_code != 200:
    print(f"Error fetching champion data: {result.status_code}")
    exit(1)
champion_data = result.json()
champion_data = champion_data["data"]

query = """
    INSERT INTO champion(id, championName)
    VALUES

"""
for key in champion_data:
    query += f"({champion_data[key]['key']}, '{champion_data[key]['id']}'),\n"
query = query[:-2]
queries.append(query)

for query in queries:
    res = db.execute_query(query)
    if res["success"]:
        print("Query executed successfully")
    else:
        print(f"Error executing query: {res['error']}")