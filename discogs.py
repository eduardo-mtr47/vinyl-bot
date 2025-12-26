import os
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

DISCOGS_TOKEN = os.getenv("DISCOGS_TOKEN")
DISCOGS_USERNAME = os.getenv("DISCOGS_USERNAME")

HEADERS = {
    "User-Agent": "VinylFinderBot/1.0"
}


def get_wantlist():
    """Récupère la wantlist complète d’un utilisateur Discogs"""
    url = f"https://api.discogs.com/users/{DISCOGS_USERNAME}/wants"
    params = {"token": DISCOGS_TOKEN, "per_page": 100, "page": 1}
    all_wants = []

    while True:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()

        all_wants.extend(data.get("wants", []))

        if "pagination" in data and data["pagination"]["pages"] > params["page"]:
            params["page"] += 1
        else:
            break

    return all_wants


def get_release_info(release_id):
    """Retourne les infos d’une release (pas utilisé si tu scrapes)"""
    url = f"https://api.discogs.com/releases/{release_id}"
    params = {"token": DISCOGS_TOKEN}
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()


def get_master_id(release_id):
    """Récupère le master_id à partir d’une release_id"""
    url = f"https://api.discogs.com/releases/{release_id}"
    params = {"token": DISCOGS_TOKEN}
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("master_id")


def get_master_versions(master_id, per_page=100):
    """Récupère toutes les versions d’un master (si tu veux chercher par couleur, etc.)"""
    url = f"https://api.discogs.com/masters/{master_id}/versions"
    params = {
        "per_page": per_page,
        "page": 1,
        "token": DISCOGS_TOKEN
    }

    all_versions = []

    while True:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()

        all_versions.extend(data.get("versions", []))

        if data["pagination"]["page"] < data["pagination"]["pages"]:
            params["page"] += 1
        else:
            break

    return all_versions
