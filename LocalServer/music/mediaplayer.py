from pytubefix import Playlist, YouTube
import vlc
from yt_dlp import YoutubeDL

from typing import Any, cast
import time
import threading

from LocalServer.music.queue import Queue

# Update Decorator
def update_clients(func):
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        payload = MediaPlayer.create_update(self)
        return payload
    return wrapper


class MediaPlayer():
    def __init__(self, audio_only = True):
        self.songs = Queue()
        self._audio_only = audio_only
        self.media_player = None
        self.playing = True
        self.cur_song = ""
        self.lock = threading.Lock()
        if self._audio_only:
            self.stream_instance = vlc.Instance(
                "--network-caching=1000",
                "--no-video"
            )
        else:
            self.stream_instance = vlc.Instance(
                "--network-caching=1000",
            )
        if self.stream_instance is None:
            raise RuntimeError("Failed to initialize VLC instance")
    
    def create_update(self):
        media = YouTube(self.cur_song)
        title = media.title
        playing  = 1 if self.playing else 0
        length = self.media_player.get_length()
        time = self.media_player.get_time()
        thumbnail_url = media.thumbnail_url

        update = {
            "title": title,
            "playing": playing,
            "length": length,
            "time": time,
            "thumbnail": thumbnail_url
        }
        return update

    def audio_only(self):
        self.stream_instance = vlc.Instance(
            "--network-caching=1000",
            "--no-video"
        )
    
    def stream_video(self):
        self.stream_instance = vlc.Instance(
            "--network-caching=1000",
        )
    
    def is_song_over(self):
        """Check if the current song has finished playing."""
        if not self.media_player or not self.playing:
            return False

        try:
            # Get VLC media state
            state = self.media_player.get_state()
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

    @update_clients
    def play(self, video_url, noplaylist = True):
        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "noplaylist": noplaylist,
        }

        with cast(Any, YoutubeDL)(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

        audio_url = self._get_best_audio_url(info)

        if not self.media_player:
            self.media_player = self.stream_instance.media_player_new()
        
        media = self.stream_instance.media_new(audio_url)
        self.media_player.set_media(media)

        self.playing = True
        self.media_player.play()
        self.cur_song = video_url

        # Give VLC time to start (important)
        time.sleep(1)
    
    @update_clients
    def stop(self):
        if self.media_player:
            self.media_player.stop()
        self.playing = False

    def start_song(self, data):
        payload = self.play(data["url"])
        return payload
            
    def start_playlist(self, data):
        self.queue_playlist(data)
        payload = self.play(self.songs.next())
        return payload

    @update_clients
    def queue_song(self, data, up_next = False):
        url = data["url"]
        if up_next:
            self.songs.insert(0, url)
        else:
            self.songs.append(url)

    @update_clients
    def queue_playlist(self, data, up_next = False):
        url = data["url"]
        pl = Playlist(url)

        for i, url in enumerate(pl.video_urls):
            print(i, " ", url)
            if up_next:
                self.songs.insert(i, url)
            else:
                self.songs.append(url)

    @update_clients
    def reorder_songs(self, data):
        original_index = data["original_index"]
        new_index = data["new_index"]
        self.songs.reorder(original_index, new_index)

    @update_clients
    def delete_song(self, data):
        index_song = data["original_index"]
        self.songs.pop_index(index_song)

    @update_clients
    def adjust_cur_time(self, data):
        seconds = data["new_time"]
        if self.media_player:
            self.media_player.set_time(int(seconds * 1000))

    @update_clients
    def adjust_volume(self, data):
        new_volume = data["new_volume"]
        if self.media_player:
            self.media_player.audio_set_volume(new_volume)

        # I'd like to make a system call for this

    @update_clients
    def toggle_playback(self):
        if self.media_player:
            self.playing = not self.playing
            self.media_player.pause()

    @update_clients
    def skip_reverse(self):
       url = self.songs.previous()
       if url:
           self.play(url)

    @update_clients
    def skip_forward(self):
        url = self.songs.next()
        if url:
            self.play(url)

    @update_clients
    def skip_forward_x(self, x):
        url = None
        for _ in range(x):
            url = self.songs.next()
        if url:
            self.play(url)
    
    @update_clients
    def skip_reverse_x(self, x):
        url = None
        for _ in range(x):
            url = self.songs.previous()
        if url:
            self.play(url)