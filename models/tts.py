import requests
import os

def generate_narration(scene_text, hf_token):
    API_URL = "https://router.huggingface.co/hf-inference/v1"
    headers = {"Authorization": f"Bearer {hf_token}"}
    
    # Kirim permintaan TTS
    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": scene_text}
    )
    
    if response.status_code != 200:
        raise Exception(f"Error generating narration: {response.text}")
    
    # Simpan file audio
    audio_data = response.json()["audio"]
    audio_path = f"outputs/audios/scene_{len(os.listdir('outputs/audios'))}.mp3"
    os.makedirs("outputs/audios", exist_ok=True)
    with open(audio_path, "wb") as f:
        f.write(audio_data)
    
    return audio_path
