import streamlit as st
from pydub import AudioSegment
import tempfile
import os

try:
    from pytube import YouTube
    pytube_installed = True
except ImportError:
    pytube_installed = False

def main():
    st.title("Video to Audio Converter")

    input_type = st.radio("Input source:", ["Upload Video File", "YouTube Link"])

    video_path = None

    if input_type == "Upload Video File":
        uploaded_file = st.file_uploader(
            "Upload your video file",
            type=['mp4', 'mov', 'avi', 'mkv', 'webm']
        )
        if uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
                temp_video.write(uploaded_file.read())
                video_path = temp_video.name

    elif input_type == "YouTube Link":
        if not pytube_installed:
            st.warning("To use YouTube links, please install pytube: pip install pytube")
        else:
            yt_url = st.text_input("Paste YouTube video link here")
            if yt_url:
                try:
                    yt = YouTube(yt_url)
                    stream = yt.streams.get_audio_only()
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
                        out_file = stream.download(filename=temp_video.name)
                        video_path = temp_video.name
                    st.success("YouTube audio stream downloaded!")
                except Exception as e:
                    st.error(f"YouTube download error: {e}")

    if video_path:
        try:
            st.info("Extracting audio...")
            audio = AudioSegment.from_file(video_path)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                audio.export(temp_audio.name, format="mp3")
                audio_path = temp_audio.name
            st.success("Audio extracted! Download below:")
            with open(audio_path, "rb") as f:
                st.download_button(
                    label="Download MP3",
                    data=f,
                    file_name="extracted_audio.mp3",
                    mime="audio/mp3"
                )
        except Exception as e:
            st.error(f"Extraction error: {e}")
        finally:
            if os.path.exists(video_path):
                os.remove(video_path)
            if 'audio_path' in locals() and os.path.exists(audio_path):
                os.remove(audio_path)

if __name__ == "__main__":
    main()
