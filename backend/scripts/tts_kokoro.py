import os
from kokoro import KPipeline
import soundfile as sf
# Ajout un timestamp sur l'audio & Contrôle de la durée d'execution du script
import time

# Créer le pipeline TTS
pipeline = KPipeline(lang_code='f')  # 'a' = anglais par défaut / 'f' = français / 's' = espagnol / 'i' = italien

# Texte à convertir en audio
text = "J'aime les abeilles et les papillons"

# Debut de la mesure du temps
# start = time.time()


def generate_audio(text: str, voice="af_bella, speed=0.9") -> str:
# Générer l’audio
    generator = pipeline(text, voice='af_bella', speed=0.9)  # exemple de voix: 

# Sauvegarder les fichiers audio générés
    output_dir = "audio"
# Crée le dossier s'il n'existe pas
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







