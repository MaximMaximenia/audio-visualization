import streamlit as st
import numpy as np
import librosa
import tempfile
import cv2
from PIL import Image
from pathlib import Path

st.set_page_config(page_title="Аудио Визуализация", layout="wide")
st.title("🎧 Аудио Визуализация под бит")

st.markdown("Загрузите изображение и аудио, чтобы сгенерировать видео с визуализацией под ритм.")

image_file = st.file_uploader("📷 Загрузите изображение", type=["jpg", "jpeg", "png"])
audio_file = st.file_uploader("🎵 Загрузите аудио", type=["mp3", "wav", "ogg"])

if image_file and audio_file:
    with st.spinner("Загружаем аудио..."):
        y, sr = librosa.load(audio_file, sr=None)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        duration = librosa.get_duration(y=y, sr=sr)
        st.success(f"Длительность аудио: {duration:.2f} секунд")
        st.success(f"Обнаружен темп: {tempo:.2f} BPM")

    with st.spinner("Обрабатываем изображение..."):
        try:
            img = Image.open(image_file).convert("RGB")
            img = img.resize((1280, 720))
            img_array = np.array(img)

            temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            video_path = temp_video.name

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(video_path, fourcc, 30.0, (1280, 720))

            for t in range(int(duration * 30)):  # 30 fps
                frame = np.array(img_array)

                shake = int(np.sin(t / 5.0) * 15)  # "под бит"
                frame = np.roll(frame, shake, axis=1)

                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
                frame[..., 0] = (frame[..., 0] + shake) % 180
                frame = cv2.cvtColor(frame, cv2.COLOR_HSV2RGB)

                # ✅ Критично: избавляемся от -1 и приводим к uint8
                frame = np.clip(frame, 0, 255).astype(np.uint8)

                out.write(frame)

            out.release()

            st.success("✅ Видео сгенерировано!")
            st.video(video_path)

            with open(video_path, "rb") as f:
                st.download_button("📥 Скачать видео", f, file_name="visualized.mp4")

        except Exception as e:
            st.error(f"Ошибка: {str(e)}")
