from fastapi import FastAPI
from pydantic import BaseModel, Field 
import os

# from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from scripts.tts_kokoro import generate_audio
from fastapi import HTTPException

# Gestion de logs
import logging

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,  # minimum de messages affichés
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Servir le dossier audio en statique
app.mount("/audio", StaticFiles(directory="audio"), name="audio")

@app.get("/")
async def home():
    return {"Home Page"}

# Modèle pour la requête = texte à convertir en parole
class SentenceRequest(BaseModel):
    text: str = Field(description='Votre texte ne peut dépasser pas 400 caractères par requête.',max_length=400)

# Endpoint pour la synthèse vocale
@app.post("/tts")
async def generate_tts(request: SentenceRequest):
    texte = request.text.strip()

    # Log: nouvelle requête reçue
    logging.info(f"Nouvelle requête TTS reçue : '{texte}'")

    # Vérif : si après nettoyage c'est vide → erreur 400
    if not texte:
        logging.warning("Texte vide reçu")
        raise HTTPException(
            status_code=400,
            detail="Le texte ne peut pas être vide."
        )
    
    # Vérif : si texte trop long → erreur 400
    if len(texte) > 400:
            logging.warning(f"Texte trop long reçu ({len(texte)} caractères)")
            raise HTTPException(
                status_code=400,
                detail="Texte trop long, maximum 400 caractères"
            )    

    #Vérif: problème reponse serveur → erreur 500 
    try:
        # Appel de la fonction de génération
        audio_path = generate_audio(texte)
    except Exception as e:
        # Log: erreur lors de la génération
        logging.error(f"Erreur lors de la génération audio pour le texte '{texte}': {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération audio : {str(e)}"
        )
    
    # Extraire juste le nom du fichier (pour créer une URL statique)
    filename = os.path.basename(audio_path)
    # Log: succès génération audio
    logging.info(f"Audio généré avec succès : {filename}")
    url = f"/audio/{filename}"

    # Réponse JSON avec le texte reçu, le chemin du fichier et l'URL de téléchargement
    response = {
        "success": True,
        "message": "Synthèse réussie",
        "data": {
            "received_text": texte,
            "download_url": url
        }
    }

    return response
