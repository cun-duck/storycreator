from huggingface_hub import InferenceClient

def generate_full_story(theme, hf_token):
    client = InferenceClient(
        provider="hf-inference",
        api_key=hf_token
    )
    messages = [
        {
            "role": "user",
            "content": f"Tulis cerita anak-anak dengan tema {theme}. Pastikan cerita memiliki alur yang jelas dan dibagi menjadi beberapa scene."
        }
    ]
    completion = client.chat.completions.create(
        model="Qwen/Qwen2.5-Coder-32B-Instruct",
        messages=messages,
        max_tokens=1500
    )
    return completion.choices[0].message.content
