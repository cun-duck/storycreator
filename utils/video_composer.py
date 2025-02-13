import subprocess
import os

def combine_scenes_into_video(scenes, output_file):
    # Buat file teks untuk daftar input FFmpeg
    with open("inputs.txt", "w") as f:
        for scene in scenes:
            f.write(f"file '{scene['image']}'\n")
            f.write(f"duration {get_audio_duration(scene['audio'])}\n")
    
    # Jalankan FFmpeg untuk menggabungkan gambar dan audio
    ffmpeg_path = os.path.join(os.getcwd(), "bin", "ffmpeg")
    subprocess.run([
        ffmpeg_path,
        "-f", "concat",
        "-safe", "0",
        "-i", "inputs.txt",
        "-vf", "fps=24",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_file
    ])
