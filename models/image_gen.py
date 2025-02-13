import torch
from diffusers import FluxPipeline
from PIL import Image

def generate_illustration(prompt, hf_token=None):
    # Load the FLUX.1-dev pipeline
    pipe = FluxPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-dev",
        torch_dtype=torch.bfloat16,
        use_auth_token=hf_token  # Optional: Use HF token if required
    )
    
    # Enable CPU offloading to save VRAM
    pipe.enable_model_cpu_offload()
    
    # Generate image with 9:16 aspect ratio (e.g., 720x1280 pixels)
    image = pipe(
        prompt=prompt,
        height=1280,  # Tinggi gambar (9:16)
        width=720,   # Lebar gambar (9:16)
        guidance_scale=3.5,
        num_inference_steps=50,
        max_sequence_length=512,
        generator=torch.Generator("cpu").manual_seed(0)  # Seed for reproducibility
    ).images[0]
    
    return image
