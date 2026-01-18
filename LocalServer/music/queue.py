from collections import deque
import random
from collections import namedtuple
from pytubefix import YouTube

Song = namedtuple("Song", ["url", "title", "thumbnail"])

from yt_dlp import YoutubeDL

class Queue():
    trashbin_size_limit = 10
    def __init__(self, playlist = None):
        self.queue = self.queue = playlist if playlist else deque()
        self.trashbin = deque()
        self.current = None
        self.shuffle = False
        self.playing = True
        self.repeat = False
        self.time = 0
    
    def getCurrent(self):
        return self.current
    
    def clear(self):
        self.queue.clear()
    
    def play(self, url):
        self.clear()
        self.current = url
        return url

    def play_playlist(self, playlist):
        self.clear()
        self.current = YouTube(playlist[0])

        for url in (playlist[1:]):
            self.queue.append(YouTube(url))
        return self.current
    
    def insert(self, i, url):
        self.queue.insert(i, YouTube(url))

    def append(self, url):
        self.queue.append(url)
    
    def pop_index(self, i, ClearQueue = True):
        value = self.queue[i]
        del self.queue[i]
        return value
    
    def pop_front(self):
        return self.queue.popleft()
    
    def pop_end(self):
        return self.trashbin.append(self.queue.pop())

    def next(self) -> str | None:
        if self.repeat:
            return self.current
        
        if (self.current):
            self.trashbin.append(self.current)
        if (len(self.trashbin) > self.trashbin_size_limit):
            self.trashbin.popleft()

        if self.queue_empty():
            self.current = None
        elif self.shuffle:
            self.current = self.pop_index(random.randint(0, len(self.queue) - 1)) if len(self.queue) else None
        else:
            self.current = self.pop_front() if len(self.queue) else None

        return self.current
    
    def previous(self):
        if self.trash_bin_size():
            self.queue.appendleft(self.current)
            self.current = self.trashbin.popleft()
        return self.current

    def toggle_shuffle(self):
        self.shuffle = not self.shuffle
    
    def reorder(self, original_index, new_index):
        self.insert(new_index, self.pop_index(original_index))
    
    def trash_bin_size(self):
        return len(self.trashbin)

    def queue_size(self):
        return len(self.queue)

    def queue_empty(self):
        return self.queue_size() == 0
    
    def trash_bin_empty(self):
        return self.trash_bin_size() == 0
    
    def snapshot(self):
        return {
            "current": self.current,
            "queue": list(self.queue)
        }