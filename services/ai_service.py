import os
import json
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Récupérer la clé Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def analyze_match(description_offre_emploi, bio_candidat):
    #Communique avec l'API Gemini pour analyser la compatibilité.

    # URL officielle pour Gemini 1.5 Flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    prompt = f"""
    Analyse la compatibilité entre cette offre [{description_offre_emploi}] et ce candidat [{bio_candidat}]. 
    Réponds exclusivement au format JSON avec les clés 'score' (0-100) et 'justification' (max 200 caractères).
    """

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "response_mime_type": "application/json" # Garantit un JSON pur en sortie
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code != 200:
            print(f"Erreur API Gemini ({response.status_code}): {response.text}")
            return None

        data = response.json()
        
        # Extraction du texte JSON généré par l'IA
        text_response = data["candidates"][0]["content"]["parts"][0]["text"]
        
        # Conversion du texte JSON en dictionnaire Python
        return json.loads(text_response)

    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"Erreur lors du traitement de la réponse IA : {e}")
        return None
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return None