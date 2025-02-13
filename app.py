import streamlit as st
import os
import shutil
import time
from models.llm import generate_full_story
from models.image_gen import generate_illustration
from models.tts import generate_narration
from utils.story_parser import split_story_into_scenes
from utils.prompt_generator import generate_image_prompt
from utils.video_composer import combine_scenes_into_video

# Sidebar untuk input HF_TOKEN
st.sidebar.title("Konfigurasi")
hf_token = st.sidebar.text_input("Masukkan HF_TOKEN Anda:", type="password")
if not hf_token:
    st.sidebar.warning("Silakan masukkan HF_TOKEN untuk melanjutkan.")
    st.stop()

# Fitur otomatis hapus data pengguna
if "last_active_time" not in st.session_state:
    st.session_state.last_active_time = time.time()
st.session_state.last_active_time = time.time()

if time.time() - st.session_state.last_active_time > 120:
    st.warning("Anda tidak aktif selama lebih dari 2 menit. Data Anda akan dihapus.")
    shutil.rmtree("outputs", ignore_errors=True)
    st.stop()

# Main app
st.title("AI-Powered Storybook Creator for Kids")

theme = st.text_input("Masukkan tema cerita:")
num_scenes = st.slider("Jumlah Scene", min_value=3, max_value=20, value=10)

if st.button("Buat Storybook"):
    # Step 1: Generate full story using LLM
    full_story = generate_full_story(theme, hf_token)
    
    # Step 2: Split story into scenes
    scenes = split_story_into_scenes(full_story, num_scenes=num_scenes)
    
    # Step 3: Process each scene individually
    processed_scenes = []
    for i, scene in enumerate(scenes):
        # Generate image prompt
        image_prompt = generate_image_prompt(scene, HF_TOKEN)
        
        # Generate illustration
        illustration = generate_illustration(image_prompt,HF_TOKEN)
        illustration_path = f"outputs/images/scene_{i}.png"
        os.makedirs("outputs/images", exist_ok=True)
        illustration.save(illustration_path)
        
        # Generate narration
        audio_path = generate_narration(scene, hf_token)
        
        # Store scene data
        processed_scenes.append({
            "index": i,
            "image": illustration_path,
            "audio": audio_path
        })
    
    # Step 4: Combine all scenes into a video
    video_file = combine_scenes_into_video(processed_scenes, "outputs/videos/storybook.mp4")
    
    # Show individual scenes
    st.subheader("Preview Scenes")
    for i, scene in enumerate(processed_scenes):
        st.write(f"Scene {i+1}:")
        st.image(scene["image"], caption=f"Ilustrasi Scene {i+1}")
        st.audio(scene["audio"], format="audio/mp3")
    
    # Download button
    with open(video_file, "rb") as file:
        st.download_button(
            label="Download Storybook",
            data=file,
            file_name="storybook.mp4",
            mime="video/mp4"
        )
