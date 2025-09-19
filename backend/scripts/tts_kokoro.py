import os
from kokoro import KPipeline
import soundfile as sf
import time

# Créer le pipeline TTS
pipeline = KPipeline(lang_code='f')  # 'a' = anglais par défaut / 'f' = français / 's' = espagnol / 'i' = italien

LANG_VOICES = {
    "fr": ["ff_siwis"],
    "en": ["af_heart", "af_bella", "am_fenrir", "am_michael"],
    "jp": ["jf_tebukuro","jm_kumo"],
    "es": ["ef_dora","em_alex"],
    "it": ["if_sara", "im_nicola"]
}


# Fonction de génération audio
def generate_audio(text: str, lang: str = "fr", voice: str = None, speed: float = 1.0) -> str:
    # Vérifie si la langue est disponible
    if lang not in LANG_VOICES:
        raise ValueError(f"Langue '{lang}' non disponible.")
    
    # Si pas de voix spécifiée, prend la première voix disponible pour la langue
    if voice is None:
        voice = LANG_VOICES[lang][0]

    # Crée le pipeline
    pipeline = KPipeline(lang_code=lang[0])  # 'f' pour français, 'a' pour anglais, etc.

    # Générer l’audio
    generator = pipeline(text, voice=voice, speed=speed)

    # Sauvegarder les fichiers audio
    output_dir = "audio"
    os.makedirs(output_dir, exist_ok=True)

    for i, (gs, ps, audio) in enumerate(generator):
        timestamp = int(time.time())
        filename = os.path.join(output_dir, f'test_{timestamp}_{i}.wav')
        sf.write(filename, audio, 24000)
        return filename
        # print(f"Fichier audio généré : {filename}")

    # print("Test terminé ! Écoute les fichiers .wav dans le dossier TTS-project")

# Fin de la mesure du temps
# end = time.time()
# print("Temps de génération :", end - start, "secondes")







