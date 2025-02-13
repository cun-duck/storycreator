from huggingface_hub import InferenceClient

def generate_illustration(prompt, hf_token):
    client = InferenceClient(
        provider="hf-inference",
        api_key=hf_token
    )
    image = client.text_to_image(
        prompt=prompt,
        model="black-forest-labs/FLUX.1-dev"
    )
    return image
