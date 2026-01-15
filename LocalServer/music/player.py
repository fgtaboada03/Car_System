from pathlib import Path
import os

from pytubefix import YouTube
from pytubefix import Playlist
import subprocess
import vlc

from playlist import Songs
from file_system import download, clear_buffer

SONGS = Songs()

class Player():
    def __init__(self):
        self.songs = Songs()

    def clear_buffer(self):
        queue_folder = Path("queue")
        trashbin_folder = Path("trashbin")

        for file in queue_folder.iterdir():
            os.remove(str(file))
        
        for file in trashbin_folder.iterdir():
            os.remove(str(file))

    def play(self, target_url):
        queue_path = Path("queue")
        for url in queue_path.iterdir():
            if (target_url == url.name):
                os.startfile(url)

    def start_song(self, data):
        url = data["url"]
        download(url)

    def start_playlist(self, data):
        url = data["url"]
        pl = Playlist(url)
        SONGS.clear()
        clear_buffer()

        for url in pl.video_urls[1:]:
            SONGS.append(url)

        for url in pl.video_urls[:4]:
            download(url)


    def queue_song(self, data, up_next = False):
        url = data["url"]
        SONGS.append(url)

    def queue_playlist(self, data, up_next = False):
        url = data["url"]
        pl = Playlist(url)

        for url in pl.video_urls[1:]:
            SONGS.append(url)

    def reorder_songs(self, data):
        original_index = data["original_index"]
        new_index = data["new_index"]

        SONGS.reorder(original_index, new_index)

    def delete_song(self, data):
        index_song = data["original_index"]

        SONGS.pop_index(index_song)

    def adjust_cur_time(self, data):
        return

    def adjust_volume(self, data):
        return

    def toggle_playback(self):
        return

    def skip_reverse(self):
        return

    def skip_forward(self):
        return