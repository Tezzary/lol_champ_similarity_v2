import db
import request
import os
from dotenv import load_dotenv

load_dotenv()

db.execute_query("SELECT * FROM player")


url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/" + os.getenv("RIOT_SAMPLE_USER") + "/" + os.getenv("RIOT_SAMPLE_TAG")
data = request.make_request(url, None)

gameName = data["gameName"]
tagLine = data["tagLine"]
puuid = data["puuid"]

url = "https://oc1.api.riotgames.com/lol/league/v4/entries/by-puuid/" + puuid
data = request.make_request(url, None)

rank = data[0]["rank"]
tier = data[0]["tier"]

url = "https://oc1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/" + puuid
data = request.make_request(url, None)
level = data["summonerLevel"]

db.execute_query(f"""
INSERT OR REPLACE INTO player (puuid, gameName, tagLine, level, rank, tier)
VALUES ('{puuid}', '{gameName}', '{tagLine}', {level}, '{rank}', '{tier}')
""")

print(db.execute_query("SELECT * FROM player"))