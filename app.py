import streamlit as st
import librosa
import numpy as np
from PIL import Image, ImageEnhance
import imageio
import os

# Настройка для улучшения интерфейса
st.set_page_config(page_title="Audio Visualization", page_icon="🎵", layout="centered")

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
        
        # Обновляем прогресс
        progress = (i + 1) / 50
        st.progress(progress)
    
    # Сохранение GIF
    gif_path = "/tmp/visualization.gif"
    imageio.mimsave(gif_path, frames, duration=0.1)
    return gif_path

def main():
    st.title("Create Audio Visualization 🎶")
    st.markdown("""
        Загрузите аудиофайл и изображение, и создайте визуализацию с динамическим эффектом для аудио.
        Вы получите GIF-анимированное изображение, которое будет двигаться под ритм музыки.
    """, unsafe_allow_html=True)

    # Загрузить аудио и изображение
    audio_file = st.file_uploader("Выберите аудиофайл", type=["mp3", "wav"], label_visibility="collapsed")
    image_file = st.file_uploader("Выберите изображение", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

    if audio_file is not None and image_file is not None:
        with st.spinner('Генерация визуализации...'):
            gif_path = create_viz(audio_file, image_file)
        
        st.image(gif_path, caption="Визуализация", use_container_width=True)
        
        # Кнопка для скачивания GIF
        st.markdown("<br>", unsafe_allow_html=True)
        with open(gif_path, "rb") as f:
            st.download_button(
                label="Скачать GIF",
                data=f,
                file_name="visualization.gif",
                mime="image/gif",
                use_container_width=True
            )

if __name__ == "__main__":
    main()
