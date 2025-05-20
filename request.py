import requests
import os
from dotenv import load_dotenv

load_dotenv()
RIOT_API_KEY = os.getenv("RIOT_API_KEY")

def make_request(url, params=None):
    response = requests.get(url, params=params, headers={"X-Riot-Token": RIOT_API_KEY})

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Example usage
if __name__ == "__main__":
    url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/" + os.getenv("RIOT_SAMPLE_USER") + "/" + os.getenv("RIOT_SAMPLE_TAG")
    data = make_request(url, None)
    print(data)