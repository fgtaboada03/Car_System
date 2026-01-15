from collections import deque
import random

class Songs():
    def __init__(self, playlist = deque()):
        self.queue = playlist
        self.trashbin = deque()
        self.current = None
        self.shuffle = False
        self.playing = True
        self.repeat = False
        self.time = 0
    
    def clear(self):
        self.queue.clear()
    
    def play(self, url):
        self.queue.clear()
        self.current = url
        return url

    def play_playlist(self, playlist):
        self.queue.clear()
        self.current = playlist[0]

        for url in (playlist[1:]):
            self.queue.append(url)
    
    def start(self):
        self.playing = False
        # TODO Start Current Song Playing on Device

    def stop(self):
        self.playing = False
        # TODO Stop Current Song Playing on Device
    
    def insert(self, i, url):
        self.queue.insert(i, url)

    def append(self, url):
        self.queue.append(url)
    
    def pop_index(self, i, ClearQueue = True):
        if ClearQueue:
            popped_value = self.queue[i]
            del self.queue[i]
        else:
            popped_value = self.queue[i]
            del self.trashbin[i]
        return popped_value
    
    def pop_front(self):
        self.queue.popleft()
    
    def pop_end(self):
        self.trashbin.append(self.queue.pop())

    def next(self):
        if self.repeat:
            return self.current
        if self.shuffle:
            self.current = self.pop_index(random.randint(0, len(self.queue) - 1))
            if (self.current):
                self.trashbin.append(self.current)
            if (len(self.trashbin) > 10):
                self.trashbin.popleft()
            return self.current
        else:
            self.current = self.pop_front() if self.queue else None
            if (self.current):
                self.trashbin.append(self.current)
            if (len(self.trashbin) > 10):
                self.trashbin.popleft()
            return self.current

    def toggle_shuffle(self):
        self.shuffle = not self.shuffle
    
    def reorder(self, original_index, new_index):
        self.insert(new_index, self.pop_index(original_index))
    
    def snapshot(self):
        return {
            "current": self.current,
            "queue": list(self.queue)
        }