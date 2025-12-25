from discogs import get_wantlist, get_release_info

def main():
    print("📦 Lecture de ta wantlist Discogs...\n")
    items = get_wantlist()

    for idx, item in enumerate(items, 1):
        release = item["basic_information"]
        title = release["title"]
        release_id = release["id"]
        year = release.get("year", "N/A")
        artists = ", ".join([a["name"] for a in release["artists"]])
        print(f"{idx}. 🎵 {artists} – {title} ({year}) | Release ID: {release_id}")

    print("\n✅ Liste récupérée. Prochaine étape : chercher les meilleures offres...")

if __name__ == "__main__":
    main()
