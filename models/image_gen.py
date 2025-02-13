from huggingface_hub import InferenceClient
import torch
from diffusers import FluxPipeline
from PIL import Image

def generate_illustration(prompt, hf_token=None, use_inference_api=True):
    """
    Menghasilkan gambar menggunakan FLUX.1-dev melalui Inference API atau Pipeline Lokal.
    :param prompt: Prompt teks untuk menghasilkan gambar.
    :param hf_token: Token autentikasi Hugging Face (wajib untuk Inference API, opsional untuk Pipeline Lokal).
    :param use_inference_api: Jika True, gunakan Inference API. Jika False, gunakan Pipeline Lokal.
    :return: PIL.Image object dengan aspek rasio 9:16.
    """
    if use_inference_api:
        # Gunakan Hugging Face Inference API
        client = InferenceClient(
            provider="hf-inference",
            api_key=hf_token
        )
        image = client.text_to_image(
            prompt=prompt,
            model="black-forest-labs/FLUX.1-dev"
        )
    else:
        # Gunakan Pipeline Lokal
        pipe = FluxPipeline.from_pretrained(
            "black-forest-labs/FLUX.1-dev",
            torch_dtype=torch.bfloat16,
            use_auth_token=hf_token
        )
        pipe.enable_model_cpu_offload()  # Hemat VRAM dengan offloading ke CPU
        
        # Generate image dengan aspek rasio 9:16
        image = pipe(
            prompt=prompt,
            height=1280,  # Tinggi gambar (9:16)
            width=720,   # Lebar gambar (9:16)
            guidance_scale=3.5,
            num_inference_steps=50,
            max_sequence_length=512,
            generator=torch.Generator("cpu").manual_seed(0)  # Seed for reproducibility
        ).images[0]
    
    # Pastikan gambar memiliki aspek rasio 9:16
    image = crop_to_aspect_ratio(image, aspect_ratio=(9, 16))
    return image

def crop_to_aspect_ratio(image, aspect_ratio=(9, 16)):
    """
    Memotong gambar menjadi aspek rasio tertentu.
    :param image: PIL.Image object.
    :param aspect_ratio: Tuple (width_ratio, height_ratio).
    :return: PIL.Image object dengan aspek rasio yang diinginkan.
    """
    width, height = image.size
    target_width = int(height * aspect_ratio[0] / aspect_ratio[1])
    target_height = int(width * aspect_ratio[1] / aspect_ratio[0])
    
    if width / height > aspect_ratio[0] / aspect_ratio[1]:
        # Potong lebar
        left = (width - target_width) // 2
        right = left + target_width
        top, bottom = 0, height
    else:
        # Potong tinggi
        top = (height - target_height) // 2
        bottom = top + target_height
        left, right = 0, width
    
    cropped_image = image.crop((left, top, right, bottom))
    return cropped_image
