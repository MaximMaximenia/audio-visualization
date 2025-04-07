import streamlit as st
import librosa
import numpy as np
from PIL import Image, ImageEnhance
import imageio
import os
import matplotlib.pyplot as plt

def create_viz(audio_file, image_file):
    # Загрузим аудио
    y, sr = librosa.load(audio_file, sr=None)
    # Получим амплитуду аудио
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    # Создадим изображение
    img = Image.open(image_file)
    
    # Генерация кадров
    frames = []
    for i in range(50):
        enhancer = ImageEnhance.Brightness(img)
        factor = 1 + 0.2 * np.sin(i * 2 * np.pi / len(y))  # Меняем яркость
        img_frame = enhancer.enhance(factor)
        frames.append(np.array(img_frame))
    
    # Сохранение GIF
    gif_path = "/tmp/visualization.gif"
    imageio.mimsave(gif_path, frames, duration=0.1)
    return gif_path

def main():
    st.title("Audio Visualization with Image")
    
    # Загрузить аудио и изображение
    audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])
    image_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    if audio_file is not None and image_file is not None:
        gif_path = create_viz(audio_file, image_file)
        st.image(gif_path, caption="Generated Visualization", use_column_width=True)
        
        # Для скачивания GIF
        with open(gif_path, "rb") as f:
            st.download_button(
                label="Download GIF",
                data=f,
                file_name="visualization.gif",
                mime="image/gif"
            )

if __name__ == "__main__":
    main()
