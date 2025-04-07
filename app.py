import streamlit as st
from moviepy.editor import *
from pydub import AudioSegment
from PIL import Image
import numpy as np
import random

def get_loudness_profile(audio_path, frame_rate=30):
    sound = AudioSegment.from_file(audio_path)
    samples = np.array(sound.get_array_of_samples())
    samples = samples.astype(np.float32)
    samples /= np.max(np.abs(samples))  # нормализация

    chunk_size = int(len(samples) / (frame_rate * sound.duration_seconds))
    loudness = []

    for i in range(0, len(samples), chunk_size):
        chunk = samples[i:i+chunk_size]
        energy = np.sqrt(np.mean(chunk**2))
        loudness.append(energy)

    loudness = np.array(loudness)
    return loudness / np.max(loudness)  # нормализация

def make_audio_visualization(image_path, audio_path, output_path='output.mp4', duration=None):
    img = Image.open(image_path)
    audio = AudioFileClip(audio_path)
    
    if duration is None:
        duration = audio.duration

    loudness = get_loudness_profile(audio_path, frame_rate=30)
    total_frames = int(duration * 30)

    if len(loudness) < total_frames:
        loudness = np.pad(loudness, (0, total_frames - len(loudness)), mode='edge')
    else:
        loudness = loudness[:total_frames]

    img = img.convert("RGB")
    img_w, img_h = img.size

    def make_frame(t):
        frame_idx = int(t * 30)
        intensity = loudness[frame_idx] * 10

        offset_x = random.randint(-int(intensity), int(intensity))
        offset_y = random.randint(-int(intensity), int(intensity))
        new_img = Image.new("RGB", (img_w, img_h), (0, 0, 0))
        new_img.paste(img, (offset_x, offset_y))

        return np.array(new_img)

    video = VideoClip(make_frame, duration=duration).set_audio(audio)
    video.write_videofile(output_path, fps=30)

st.title("Аудио-визуализация")
st.write("Загрузите изображение и аудио, чтобы создать видео")

image_file = st.file_uploader("Загрузите изображение", type=["jpg", "png"])
audio_file = st.file_uploader("Загрузите аудио", type=["mp3", "wav"])

if image_file and audio_file:
    image_path = "uploaded_image.jpg"
    audio_path = "uploaded_audio.mp3"

    with open(image_path, "wb") as f:
        f.write(image_file.read())
    
    with open(audio_path, "wb") as f:
        f.write(audio_file.read())
    
    output_video_path = "output_video.mp4"
    make_audio_visualization(image_path, audio_path, output_path=output_video_path)
    
    st.video(output_video_path)
    st.success("Видео готово!")
