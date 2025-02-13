from huggingface_hub import InferenceClient

def generate_image_prompt(scene_text, hf_token):
    client = InferenceClient(
        provider="hf-inference",
        api_key=hf_token
    )
    messages = [
        {
            "role": "user",
            "content": f"Deskripsikan secara visual dalam bentuk prompt untuk model text-to-image: {scene_text}"
        }
    ]
    completion = client.chat.completions.create(
        model="Qwen/Qwen2.5-Coder-32B-Instruct",
        messages=messages,
        max_tokens=50
    )
    return completion.choices[0].message.content
