import sqlite3
con = sqlite3.connect("database.db")

cur = con.cursor()

def execute_query(query):
    try:
        res = cur.execute(query)
        con.commit()
        if (res is not None):
            return {"success": True, "data": res.fetchall()}
        return {"success": True, "data": None}
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return {"success": False, "data": str(e)}

def get_num_players():
    query = "SELECT COUNT(*) FROM player"
    result = execute_query(query)
    if result["success"]:
        return result["data"][0][0]
    return 0
def get_player(player_id):
    query = f"SELECT * FROM player ORDER BY puuid"
    result = execute_query(query)
    if result["success"]:
        return result["data"][player_id]
    return None

def get_players(count):
    #select random players from the database
    query = f"SELECT * FROM player ORDER BY RANDOM() LIMIT {count}"
    result = execute_query(query)
    if result["success"]:
        players = []
        for player in result["data"]:
            player_object = {
                "puuid": player[0],
                "gameName": player[1],
                "tagLine": player[2],
                "level": player[3],
                "rank": player[4],
                "tier": player[5],
                "foundTimestamp": player[6],
                "lastExploredTimestamp": player[7],
                "totalMasteryPoints": player[8]
            }
            players.append(player_object)
        return players
    return []

def get_player_champions(puuid, count):
    query = f"""
    SELECT champion.i, champion.id, champion.championName, player_champion_mastery.masteryPoints, player_champion_mastery.masteryLevel
    FROM player_champion_mastery
    JOIN champion ON player_champion_mastery.championId = champion.id
    WHERE player_champion_mastery.puuid = '{puuid}'
    ORDER BY player_champion_mastery.masteryPoints DESC
    LIMIT {count}
    """
    result = execute_query(query)
    if result["success"]:
        champions = []
        for row in result["data"]:
            champion_object = {
                "i": row[0],
                "id": row[1],
                "championName": row[2],
                "masteryPoints": row[3],
                "masteryLevel": row[4]
            }
            champions.append(champion_object)
        return champions
    return []

def get_mastery(player, champion_id):
    query = f"""
    SELECT masteryPoints, masteryLevel
    FROM player_champion_mastery
    WHERE puuid = '{player['puuid']}' AND championId = {champion_id}
    """
    result = execute_query(query)
    if result["success"] and result["data"]:
        return result["data"][0][0]  # masteryPoints
    return 0  # Default to 0 if no mastery found

def get_champions():
    query = "SELECT i, id, championName FROM champion ORDER BY i ASC"
    result = execute_query(query)
    if result["success"]:
        champions = []
        for row in result["data"]:
            champion_object = {
                "i": row[0],
                "id": row[1],
                "championName": row[2]
            }
            champions.append(champion_object)
        return champions
    return []
if __name__ == "__main__":
    print(get_num_players())
    print(get_player(1))
    print(get_players())