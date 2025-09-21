from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import logging
from app.scripts.tts_kokoro import generate_audio

app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Créer le dossier audio s'il n'existe pas
if not os.path.exists("audio"):
    os.makedirs("audio")

# Servir le dossier audio en statique
app.mount("/audio", StaticFiles(directory="audio"), name="audio")

@app.get("/")
async def home():
    return {"Home Page"}

class SentenceRequest(BaseModel):
    text: str = Field(description="Votre texte ne peut dépasser pas 200 caractères par requête.", max_length=200)
    lang: str = Field(default="fr", description="Langue du TTS : fr, en, jp, es, it")
    voice: str = Field(default=None, description="Voix spécifique pour la langue choisie")

@app.post("/tts")
async def generate_tts(request: SentenceRequest):
    texte = request.text.strip()
    lang = request.lang
    voice = request.voice

    logging.info(f"Nouvelle requête TTS reçue : '{texte}' | Langue: {lang} | Voix: {voice}")

    if not texte:
        logging.warning("Texte vide reçu")
        raise HTTPException(status_code=400, detail="Le texte ne peut pas être vide.")

    if len(texte) > 200:
        logging.warning(f"Texte trop long reçu ({len(texte)} caractères)")
        raise HTTPException(status_code=400, detail="Texte trop long, maximum 200 caractères")

    try:
        audio_path = generate_audio(texte, lang=lang, voice=voice)
    except Exception as e:
        logging.error(f"Erreur lors de la génération audio pour le texte '{texte}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération audio : {str(e)}")

    filename = os.path.basename(audio_path)
    logging.info(f"Audio généré avec succès : {filename}")
    audio_url = f"/audio/{filename}"
    download_url = f"/download/{filename}"

    response = {
        "success": True,
        "message": "Synthèse réussie",
        "data": {
            "received_text": texte,
            "audio_url": audio_url,  
            "download_url": download_url  
        }
    }

    return response

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join("audio", filename)
    if not os.path.exists(file_path):
        logging.warning(f"Fichier non trouvé : {file_path}")
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    
    logging.info(f"Téléchargement du fichier : {filename}")
    return FileResponse(
        path=file_path,
        filename=filename,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )