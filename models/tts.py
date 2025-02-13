import requests

def generate_narration(scene_text, hf_token):
    API_URL = "https://router.huggingface.co/hf-inference/v1"
    headers = {"Authorization": f"Bearer {hf_token}"}
    
    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": scene_text}
    )
    audio_data = response.json()["audio"]
    return audio_data
