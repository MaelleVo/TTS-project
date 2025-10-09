from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import logging
from app.scripts.tts_kokoro import text_to_speech

# Configurer les logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialiser FastAPI
app = FastAPI()

# Configurer CORS pour Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend-global-beryl.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint de santé
@app.get("/health")
async def health():
    return {"status": "OK", "message": "Serveur TTS prêt"}

# Modèle pour la requête TTS
class SentenceRequest(BaseModel):
    text: str = Field(..., max_length=200, description="Texte à transformer en audio")
    lang: str = Field(default="fr")
    voice: str = Field(default=None)

# Endpoint pour TTS
@app.post("/tts")
async def tts(request_data: SentenceRequest):
    text = request_data.text.strip()
    lang = request_data.lang
    voice = request_data.voice

    if not text:
        raise HTTPException(status_code=400, detail="Texte requis")
    if len(text) > 200:
        raise HTTPException(status_code=400, detail="Texte trop long, max 200 caractères")

    try:
        logger.info(f"Requête TTS reçue : {text[:50]}... | Langue: {lang} | Voix: {voice}")
        audio_buffer = text_to_speech(text, lang=lang, voice=voice)
        logger.info("Audio généré")
        return StreamingResponse(audio_buffer, media_type="audio/wav")
    except Exception as e:
        logger.error(f"Erreur TTS : {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur : {str(e)}")