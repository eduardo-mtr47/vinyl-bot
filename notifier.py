import requests

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1454440464995582047/5XyhNReXfWt6SrK3G6NkTTtlRf9KB1qJUWCDU2HIrbeoU03CijC_BfWiluBygZTL4g2A"

def send_discord_message(content):
    payload = {
        "content": content
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code != 204:
        print(f"⚠️ Erreur Discord : {response.status_code} - {response.text}")
