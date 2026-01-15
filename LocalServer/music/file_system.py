from pytubefix import YouTube
from pathlib import Path
import subprocess
import os

def download(link):
    # Source - https://stackoverflow.com/a
    # Posted by Vsevolod
    # Retrieved 2026-01-14, License - CC BY-SA 4.0
    youtube_object = YouTube(link)

    # Get highest quality video and audio separately
    video_stream = youtube_object.streams.filter(adaptive=True, file_extension="mp4", only_video=True).order_by("resolution").desc().first()
    audio_stream = youtube_object.streams.filter(adaptive=True, file_extension="mp4", only_audio=True).order_by("abr").desc().first()

    if not video_stream or not audio_stream:
        print("No suitable streams found.")
        return

    # Define output filenames
    video_file = "video_temp.mp4"
    audio_file = "audio_temp.mp4"
    output_file = link

    # Download video and audio separately
    video_stream.download(filename=video_file)
    audio_stream.download(filename=audio_file)

    # Merge using ffmpeg
    ffmpeg_command = ["ffmpeg", "-y", "-i", video_file, "-i", audio_file, "-c", "copy", output_file]
    subprocess.run(ffmpeg_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("Download completed: " + output_file)

def clear_buffer():
    queue_path = Path("queue")
    bin_path = Path("bin")

    for file in queue_path.iterdir():
        os.remove(str(file))

    for file in bin_path.iterdir():
        os.remove(str(file))