import streamlit as st
import numpy as np
import cv2
from PIL import Image
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO
import os

def create_video(audio_file, image_file):
    try:
        st.write("Загружаем аудио...")
        audio = AudioSegment.from_file(audio_file)
        duration = len(audio) / 1000  # в секундах
        st.write(f"Длительность аудио: {duration} секунд")
        
        st.write("Обрабатываем изображение...")
        img = Image.open(image_file)
        img = img.resize((1280, 720))  # Размер изображения для видео
        
        # Настройка видео
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_path = "/tmp/visualization_video.mp4"
        out = cv2.VideoWriter(video_path, fourcc, 30.0, (1280, 720))
        
        for t in range(int(duration * 30)):  # 30 fps
            frame = np.array(img)
            
            # Добавление динамики: движение изображения (тряска)
            shake = int(np.sin(t / 10) * 20)  # Это создаст тряску
            frame = np.roll(frame, shake, axis=1)
            
            # Изменение цветов: добавление эффекта
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
            frame[..., 0] = (frame[..., 0] + shake) % 180  # Сдвиг оттенков по времени
            frame = cv2.cvtColor(frame, cv2.COLOR_HSV2RGB)
            
            # Визуальные эффекты: добавление геометрических фигур, реагирующих на бит
            if t % 30 == 0:  # Срабатывает на каждом 30 кадре
                cv2.circle(frame, (640, 360), 100, (0, 255, 0), -1)  # Зеленый круг
            
            out.write(frame)
        
        out.release()
        return video_path
    except Exception as e:
        st.write(f"Ошибка: {e}")
        return None

def main():
    st.title("Создание видео с визуализацией аудио 🎶")
    audio_file = st.file_uploader("Выберите аудиофайл", type=["mp3", "wav"])
    image_file = st.file_uploader("Выберите изображение", type=["jpg", "png", "jpeg"])

    if audio_file and image_file:
        with st.spinner('Генерация видео...'):
            video_path = create_video(audio_file, image_file)
        
        if video_path:
            st.video(video_path)
            with open(video_path, "rb") as f:
                st.download_button("Скачать видео", data=f, file_name="visualization.mp4", mime="video/mp4")

if __name__ == "__main__":
    main()
