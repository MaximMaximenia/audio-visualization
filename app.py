import streamlit as st
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import os
import tempfile
from PIL import Image

# Загрузка аудио
def load_audio(file):
    try:
        audio_data = wavfile.read(file)
        return audio_data
    except Exception as e:
        st.error(f"Ошибка при загрузке аудио: {e}")
        return None

# Обработка изображения
def process_image(image_file):
    try:
        img = Image.open(image_file)
        return img
    except Exception as e:
        st.error(f"Ошибка при обработке изображения: {e}")
        return None

# Основная функция
def main():
    st.title("Визуализация под музыку")

    audio_file = st.file_uploader("Загрузите аудио файл", type=["wav", "mp3", "flac"])
    image_file = st.file_uploader("Загрузите изображение", type=["png", "jpg", "jpeg"])

    if audio_file and image_file:
        st.text("Загружаем аудио...")
        
        # Загружаем аудио
        audio_data = load_audio(audio_file)
        if audio
