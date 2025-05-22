import db
import os
from dotenv import load_dotenv

load_dotenv()

result = db.execute_query(f"""
SELECT championName as champion, COALESCE(masteryPoints, 0) from player_champion_mastery
RIGHT JOIN champion ON champion.id = player_champion_mastery.championId
LEFT JOIN player ON player.puuid = player_champion_mastery.puuid
WHERE player.puuid IS NULL or player.gameName = '{os.getenv("RIOT_SAMPLE_USER")}' and player.tagLine = '{os.getenv("RIOT_SAMPLE_TAG")}'
ORDER BY player_champion_mastery.masteryPoints DESC;
""")

print(result["data"])