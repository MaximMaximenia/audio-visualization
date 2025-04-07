import streamlit as st
import librosa
import numpy as np
from PIL import Image, ImageEnhance
import imageio

st.set_page_config(page_title="Audio Visualization", page_icon="🎵", layout="centered")

def create_viz(audio_file, image_file):
    try:
        st.write("Загружаем аудио...")
        y, sr = librosa.load(audio_file, sr=None)
        st.write("Аудио загружено успешно.")
        
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        st.write(f"Темп музыки: {tempo} BPM")
        
        st.write("Обрабатываем изображение...")
        img = Image.open(image_file)
        
        frames = []
        progress_bar = st.progress(0)
        total_frames = 50
        
        for i in range(total_frames):
            enhancer = ImageEnhance.Brightness(img)
            factor = 1 + 0.2 * np.sin(i * 2 * np.pi / len(y))
            img_frame = enhancer.enhance(factor)
            frames.append(np.array(img_frame))
            
            progress = (i + 1) / total_frames
            progress_bar.progress(progress)  # Обновляем прогресс

        gif_path = "/tmp/visualization.gif"
        imageio.mimsave(gif_path, frames, duration=0.1)
        st.write("Визуализация завершена.")
        return gif_path
    except Exception as e:
        st.write(f"Ошибка: {e}")

def main():
    st.title("Create Audio Visualization 🎶")
    st.markdown("Загрузите аудиофайл и изображение, чтобы создать визуализацию.")

    audio_file = st.file_uploader("Выберите аудиофайл", type=["mp3", "wav"])
    image_file = st.file_uploader("Выберите изображение", type=["jpg", "png", "jpeg"])

    if audio_file and image_file:
        with st.spinner('Генерация визуализации...'):
            gif_path = create_viz(audio_file, image_file)
        
        if gif_path:
            st.image(gif_path, caption="Визуализация", use_container_width=True)
            with open(gif_path, "rb") as f:
                st.download_button("Скачать GIF", data=f, file_name="visualization.gif", mime="image/gif")

if __name__ == "__main__":
    main()
