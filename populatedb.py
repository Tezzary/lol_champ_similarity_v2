import db
import request
import os
from dotenv import load_dotenv

load_dotenv()

MATCHES_PER_PLAYER = 5
PLAYERS_TO_EXPLORE = 5

def add_user_if_not_exists(puuid):
    result = db.execute_query(f"""
    SELECT gameName, tagLine FROM player WHERE puuid = '{puuid}'
    """)

    if len(result["data"]) > 0:
        result = result["data"]
        print(f"User {result[0][0]}#{result[0][1]} already exists in the database, skipping...")
        return
    else:
        print("User does not exist in the database. Adding user...")
    
    url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/" + puuid
    data = request.make_request(url, None)

    gameName = data["gameName"]
    tagLine = data["tagLine"]

    url = "https://oc1.api.riotgames.com/lol/league/v4/entries/by-puuid/" + puuid
    data = request.make_request(url, None)

    rank = data[0]["rank"]
    tier = data[0]["tier"]

    url = "https://oc1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/" + puuid
    data = request.make_request(url, None)
    level = data["summonerLevel"]
    #place current timestamp in foundTimestamp and lastExploredTimestamp
    db.execute_query(f"""
    INSERT INTO player (puuid, gameName, tagLine, level, rank, tier, foundTimestamp, lastExploredTimestamp)
    VALUES ('{puuid}', '{gameName}', '{tagLine}', {level}, '{rank}', '{tier}', unixepoch(), NULL)
    """)

def explore_matches(puuid):
    url = f"https://sea.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start=0&count={MATCHES_PER_PLAYER}"
    data = request.make_request(url, None)
    if len(data) == 0:
        print(f"No matches found for {puuid}.")
        return
    for matchId in data:
        url = f"https://sea.api.riotgames.com/lol/match/v5/matches/{matchId}"
        matchData = request.make_request(url, None)
        if matchData is None:
            print(f"Match data for {matchId} is None.")
            continue
        startTime = matchData["info"]["gameStartTimestamp"]
        endTime = matchData["info"]["gameEndTimestamp"]
        gameMode = matchData["info"]["gameMode"]
        result = db.execute_query(f"""
        INSERT INTO match (id, startTime, endTime, gameMode, discovererPuuid)
        VALUES ('{matchId}', {startTime}, {endTime}, '{gameMode}', '{puuid}')
        """)
        if not result["success"]:
            print(f"Match {matchId} already exists in the database, skipping...")
            continue
        for player in matchData["info"]["participants"]:
            puuid = player["puuid"]
            add_user_if_not_exists(puuid)
            db.execute_query(f"""
            INSERT INTO match_player (puuid, matchId)
            VALUES ('{puuid}', '{matchId}')
            """)
    print(f"Explored {MATCHES_PER_PLAYER} matches for {puuid}.")


def populate_db():
    for _ in range(PLAYERS_TO_EXPLORE):
        result = db.execute_query("""
        SELECT player.puuid FROM player
        WHERE player.lastExploredTimestamp IS NULL
        """)
        result = result["data"]
        if len(result) == 0:
            print("All players have been searched. Exiting...")
            return
        player = result[0]
        puuid = player[0]

        db.execute_query(f"""
            UPDATE player SET lastExploredTimestamp = unixepoch() WHERE puuid = '{puuid}'
        """)
        
        try:
            explore_matches(puuid)
        except Exception as e:
            print(f"Error exploring matches for {puuid}: {e}")
            continue

if __name__ == "__main__":
    url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/" + os.getenv("RIOT_SAMPLE_USER") + "/" + os.getenv("RIOT_SAMPLE_TAG")
    data = request.make_request(url, None)
    print(data)
    add_user_if_not_exists(data["puuid"])
    populate_db()
    #print(db.execute_query("SELECT puuid, gameName, tagLine, level, rank, tier, strftime('%d/%m/%Y', datetime(foundTimestamp, 'unixepoch')), strftime('%d/%m/%Y', datetime(lastExploredTimestamp, 'unixepoch')) FROM player"))
    print(db.execute_query("SELECT gameName, tagLine FROM player"))