from huggingface_hub import InferenceClient
from PIL import Image

def generate_illustration(prompt):
    """
    Menghasilkan gambar menggunakan FLUX.1-dev melalui Hugging Face Inference API.
    :param prompt: Prompt teks untuk menghasilkan gambar.
    :param hf_token: Token autentikasi Hugging Face.
    :return: PIL.Image object dengan aspek rasio 9:16.
    """
    # Initialize InferenceClient
    client = InferenceClient(
        provider="hf-inference",
        api_key="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"
    )
    
    # Generate image using FLUX.1-dev
    image = client.text_to_image(
        prompt=prompt,
        model="black-forest-labs/FLUX.1-dev"
    )
    
    # Proses gambar untuk aspek rasio 9:16
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
