from openai import OpenAI
import json
from datetime import date
import os

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

api_key = os.getenv("KAAMELOTT_API")
client = OpenAI(api_key=api_key)

print(f"Appel OpenAI direct avec topic: {topic} et seed: {seed}")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Tu es un conteur expert en culture portugaise. Tu racontes des histoires courtes, fascinantes et authentiques sur le Portugal, sa culture, sa gastronomie et son histoire. Limite tes réponses à 100-150 mots maximum."},
        {"role": "user", "content": f"Raconte-moi {topic}. L'histoire doit être unique et captivante, et utilise cette seed pour la variation: {seed}"}
    ],
    temperature=0.8,
    max_tokens=300
)

story = response.choices[0].message.content

with open("story.json", "w", encoding="utf-8") as f:
    json.dump({"date": today_str, "story": story}, f, ensure_ascii=False, indent=2)
