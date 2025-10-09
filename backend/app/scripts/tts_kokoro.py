from kokoro import KPipeline
from io import BytesIO
import soundfile as sf

LANG_VOICES = {
    "fr": ["ff_siwis"],
    "en": ["af_heart", "af_bella", "am_fenrir", "am_michael"],
    "jp": ["jf_tebukuro", "jm_kumo"],
    "es": ["ef_dora", "em_alex"],
    "it": ["if_sara", "im_nicola"]
}

def text_to_speech(text: str, lang: str = "fr", voice: str = None, speed: float = 1.0) -> BytesIO:
    if lang not in LANG_VOICES:
        raise ValueError(f"Langue '{lang}' non disponible.")
    
    if voice is None:
        voice = LANG_VOICES[lang][0]

    pipeline = KPipeline(lang_code=lang[0])
    generator = pipeline(text, voice=voice, speed=speed)

    audio_buffer = BytesIO()
    for _, _, audio in generator:
        sf.write(audio_buffer, audio, 24000, format="WAV")
        audio_buffer.seek(0)
        return audio_buffer

    raise ValueError("Aucun audio généré")