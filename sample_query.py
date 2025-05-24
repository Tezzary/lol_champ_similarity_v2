import db
import os
from dotenv import load_dotenv

load_dotenv()

'''
result = db.execute_query(f"""
SELECT championName as champion, COALESCE(masteryPoints, 0) from player_champion_mastery
RIGHT JOIN champion ON champion.id = player_champion_mastery.championId
LEFT JOIN player ON player.puuid = player_champion_mastery.puuid
WHERE player.puuid IS NULL or player.gameName = '{os.getenv("RIOT_SAMPLE_USER")}' and player.tagLine = '{os.getenv("RIOT_SAMPLE_TAG")}'
ORDER BY player_champion_mastery.masteryPoints DESC;
""")
'''
'''
result = db.execute_query(f"""
    UPDATE player
    SET totalMasteryPoints = (
        SELECT SUM(masteryPoints)
        FROM player_champion_mastery
        WHERE player_champion_mastery.puuid = player.puuid
    );
""")
'''
'''
result = db.execute_query(f"""
    ALTER TABLE champion
    ADD i INT;
""")
'''
result = db.execute_query(f"""
SELECT * FROM champion ORDER BY championName;
""")
champions = result["data"]
i = 0
for champ in champions:
    result = db.execute_query(f"""
    UPDATE champion
    SET i = {i}
    WHERE id = {champ[0]};
    """)
    i += 1
    if not result["success"]:
        print(f"Failed to update with index {i}.")
        continue

print(result["data"])