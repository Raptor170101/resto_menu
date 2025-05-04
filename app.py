from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# Configuration de la clé API
api_key = os.getenv("KAAMELOTT_API")
print(f"Clé API chargée: {'Oui' if api_key else 'Non'}")

# Initialiser le client OpenAI
client = OpenAI(api_key=api_key)

@app.route('/api/daily-story', methods=['POST'])
def get_daily_story():
    print("Requête reçue sur /api/daily-story")
    
    try:
        data = request.json
        topic = data.get('topic')
        seed = data.get('seed')
        
        print(f"Topic: {topic}, Seed: {seed}")
        
        if not api_key:
            print("ERREUR: Clé API OpenAI non configurée")
            return jsonify({"error": "Clé API OpenAI non configurée"}), 500
        
        # Utiliser la nouvelle API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un conteur expert en culture portugaise. Tu racontes des histoires courtes, fascinantes et authentiques sur le Portugal, sa culture, sa gastronomie et son histoire. Limite tes réponses à 100-150 mots maximum."
                },
                {
                    "role": "user",
                    "content": f"Raconte-moi {topic}. L'histoire doit être unique et captivante, et utilise cette seed pour la variation: {seed}"
                }
            ],
            temperature=0.8,
            max_tokens=300
        )
        
        story = response.choices[0].message.content
        print("Histoire générée avec succès")
        return jsonify({"story": story})
    
    except Exception as e:
        print(f"ERREUR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/')
def serve_menu():
    with open('menu.html', 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == '__main__':
    app.run(debug=True, port=5000)