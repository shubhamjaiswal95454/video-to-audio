import streamlit as st
from pydub import AudioSegment
import tempfile
import os

try:
    from pytube import YouTube
    pytube_installed = True
except ImportError:
    pytube_installed = False

st.title("Video to Audio Converter")

choice = st.radio("Choose input method:", ("Upload video file", "YouTube link"))

uploaded_file = None
video_path = None

if choice == "Upload video file":
    uploaded_file = st.file_uploader("Upload your video file", type=["mp4", "mov", "avi", "mkv"])
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            temp_video.write(uploaded_file.read())
            video_path = temp_video.name

if choice == "YouTube link":
    if not pytube_installed:
        st.error("Please install pytube: pip install pytube")
    else:
        url = st.text_input("Paste a YouTube video link")
        if url:
            try:
                yt = YouTube(url)
                stream = yt.streams.filter(only_audio=True).first()
                if stream:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
                        stream.download(filename=temp_video.name)
                        video_path = temp_video.name
                    st.success("YouTube video downloaded! Ready for extraction.")
                else:
                    st.error("Failed to find audio stream.")
            except Exception as e:
                st.error(f"Could not download video: {e}")

if video_path:
    st.write("Converting video to audio (mp3)...")
    try:
        audio = AudioSegment.from_file(video_path)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            audio.export(temp_audio.name, format="mp3")
            audio_path = temp_audio.name
        st.success("Audio extracted successfully!")
        with open(audio_path, "rb") as file:
            st.download_button(
                label="Download MP3",
                data=file,
                file_name="extracted_audio.mp3",
                mime="audio/mp3")
    except Exception as e:
        st.error(f"Error extracting audio: {e}")
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
        if 'audio_path' in locals() and os.path.exists(audio_path):
            os.remove(audio_path)
