"""File containing functions for working with YDL"""

from pathlib import Path
import subprocess
import youtube_dl


def download(url: str, file: Path, on_progress):
    """Performs downloading audio file for YouTube video of given URL"""
    target = file.with_suffix(".webm")

    def on_progress_hook(data):
        """Callback for hooking download progress"""
        if data["status"] == "downloading":
            on_progress(
                int(data["downloaded_bytes"]),
                int(data["total_bytes_estimate"]),
            )

    ydl_opts = {
        "format": "bestaudio/best",
        "progress_hooks": [on_progress_hook],
        "outtmpl": str(target),
        "postprocessors": [
            # Since the error is being raised:
            # ERROR: WARNING: unable to obtain file audio codec with ffprobe
            # Disable convertor because run it manually
            # {
            #     "key": "FFmpegExtractAudio",
            #     "preferredcodec": "mp3",
            #     "preferredquality": "192",
            # }
        ],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    subprocess.run(["ffmpeg", "-i", str(target), str(file)], check=True)