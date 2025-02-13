from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import os

def combine_scenes_into_video(scenes, output_file):
    clips = []
    for scene in scenes:
        # Load gambar dan audio untuk scene
        img_clip = ImageClip(scene["image"]).set_duration(get_audio_duration(scene["audio"]))
        audio_clip = AudioFileClip(scene["audio"])
        
        # Gabungkan gambar dan audio
        img_clip = img_clip.set_audio(audio_clip)
        clips.append(img_clip)
    
    # Gabungkan semua scene menjadi satu video
    final_clip = concatenate_videoclips(clips)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    final_clip.write_videofile(output_file, fps=24)
    return output_file

def get_audio_duration(audio_path):
    from pydub import AudioSegment
    audio = AudioSegment.from_file(audio_path)
    return len(audio) / 1000  # Durasi dalam detik
