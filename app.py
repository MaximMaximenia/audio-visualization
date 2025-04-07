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
    progress_bar = st.progress(0)  # Полоса загрузки только один раз
    for i in range(50):
        enhancer = ImageEnhance.Brightness(img)
