import os
import requests
from dotenv import load_dotenv

load_dotenv()

DISCOGS_TOKEN = os.getenv("DISCOGS_TOKEN")
DISCOGS_USERNAME = os.getenv("DISCOGS_USERNAME")
HEADERS = {
    "User-Agent": "VinylFinderBot/1.0"
}

def get_wantlist():
    url = f"https://api.discogs.com/users/{DISCOGS_USERNAME}/wants"
    params = { "token": DISCOGS_TOKEN }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()["wants"]

def get_release_info(release_id):
    url = f"https://api.discogs.com/releases/{release_id}"
    params = { "token": DISCOGS_TOKEN }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

def get_master_id(release_id):
    url = f"https://api.discogs.com/releases/{release_id}"
    params = { "token": DISCOGS_TOKEN }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("master_id")

def get_master_versions(master_id, per_page=100):
    url = f"https://api.discogs.com/masters/{master_id}/versions"
    params = {
        "per_page": per_page,
        "token": DISCOGS_TOKEN
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()["versions"]
