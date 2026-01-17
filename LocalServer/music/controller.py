from pytubefix import Playlist
import vlc
from yt_dlp import YoutubeDL

from typing import Any, cast
import time
import threading

from LocalServer.music.songs import Songs

class Controller():
    def __init__(self):
        self.songs = Songs()
        self.media = None
        self.playing = True
        self.lock = threading.Lock()
        self.vlc_instance = vlc.Instance(
            "--network-caching=1000",
            "--no-video"
        )
        if self.vlc_instance is None:
            raise RuntimeError("Failed to initialize VLC instance")
    
    def update(self):
        return
    
    def is_song_over(self):
        """Check if the current song has finished playing."""
        if not self.media or not self.playing:
            return False

        try:
            # Get VLC media state
            state = self.media.get_state()
            from vlc import State

            # VLC reports the media ended
            if state == State.Ended:
                return True

            return False

        except Exception as e:
            print("Error checking if song is over:", e)
            return False
    
    def _get_best_audio_url(self, info: dict) -> str:
        formats = info.get("formats", [])
        audio_formats = [
            f for f in formats
            if f.get("acodec") != "none" and f.get("vcodec") == "none"
        ]

        if not audio_formats:
            raise RuntimeError("No audio-only streams found")

        best_audio = max(
            audio_formats,
            key=lambda f: f.get("abr", 0)
        )

        return best_audio["url"]


    def play(self, video_url, noplaylist = True):
        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "noplaylist": noplaylist,
        }

        # Stop existing media
        if self.media:
            self.media.stop()
            self.media = None

        with cast(Any, YoutubeDL)(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

        audio_url = self._get_best_audio_url(info)

        self.media = self.vlc_instance.media_player_new()
        media = self.vlc_instance.media_new(audio_url)
        self.media.set_media(media)

        self.playing = True
        self.media.play()

        # Give VLC time to start (important)
        time.sleep(1)
    
    def stop(self):
        if self.media:
            self.media.stop()
        self.playing = False

    def start_song(self, data):
        try:
            self.play(data["url"])
            

    def start_playlist(self, data):
        self.queue_playlist(data)
        self.play(self.songs.next())

    def queue_song(self, data, up_next = False):
        url = data["url"]
        if up_next:
            self.songs.insert(0, url)
        else:
            self.songs.append(url)

    def queue_playlist(self, data, up_next = False):
        url = data["url"]
        pl = Playlist(url)

        for i, url in enumerate(pl.video_urls):
            print(i, " ", url)
            if up_next:
                self.songs.insert(i, url)
            else:
                self.songs.append(url)

    def reorder_songs(self, data):
        original_index = data["original_index"]
        new_index = data["new_index"]

        self.songs.reorder(original_index, new_index)

    def delete_song(self, data):
        index_song = data["original_index"]

        self.songs.pop_index(index_song)

    def adjust_cur_time(self, data):
        seconds = data["new_time"]
        if self.media:
            self.media.set_time(int(seconds * 1000))

    def adjust_volume(self, data):
        new_volume = data["new_volume"]
        if self.media:
            self.media.audio_set_volume(new_volume)

        # I'd like to make a system call for this

    def toggle_playback(self):
        if self.media:
            self.playing = not self.playing
            self.media.pause()

    def skip_reverse(self):
       url = self.songs.previous()
       if url:
           self.play(url)

    def skip_forward(self):
        url = self.songs.next()
        if url:
            self.play(url)

    def skip_forward_x(self, x):
        url = None
        for _ in range(x):
            url = self.songs.next()
        if url:
            self.play(url)
    
    def skip_reverse_x(self, x):
        url = None
        for _ in range(x):
            url = self.songs.previous()
        if url:
            self.play(url)