import requests
import json
from datetime import date

# Générer la seed du jour
today_str = date.today().isoformat()
seed = abs(hash(today_str)) % (2**31)

topics = [
    "une tradition culinaire portugaise méconnue",
    "une légende portugaise fascinante",
    "un fait historique surprenant sur le Portugal",
    "une anecdote sur un plat typique portugais",
    "une histoire sur la culture vinicole portugaise",
    "un récit sur les navigateurs portugais",
    "une tradition festive portugaise",
    "une histoire sur l'artisanat portugais",
    "une anecdote sur la musique fado",
    "un fait intéressant sur l'architecture portugaise"
]
topic = topics[seed % len(topics)]

print(f"Appel avec topic: {topic} et seed: {seed}")

response = requests.post(
    "http://localhost:5000/api/daily-story",
    json={"topic": topic, "seed": seed}
)

response.raise_for_status()

data = response.json()
with open("story.json", "w", encoding="utf-8") as f:
    json.dump({
        "date": today_str,
        "story": data["story"]
    }, f, ensure_ascii=False, indent=2)
