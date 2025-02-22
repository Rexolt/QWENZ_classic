import pygame

class AudioManagerPygame:
    def __init__(self):
        pygame.mixer.init(frequency=44100)
        self.tracks = []  # Tárolja a track fájl elérési útvonalakat
        self.current_index = -1

    def add_track(self, path):
        self.tracks.append(path)

    def remove_track(self, index):
        if 0 <= index < len(self.tracks):
            del self.tracks[index]
            if self.current_index >= len(self.tracks):
                self.current_index = len(self.tracks) - 1

    def set_current_index(self, index):
        if 0 <= index < len(self.tracks):
            self.current_index = index

    def get_current_track_file(self):
        if 0 <= self.current_index < len(self.tracks):
            return self.tracks[self.current_index]
        return ""

    def play(self):
        if not self.tracks:
            return
        if self.current_index < 0:
            self.current_index = 0
        track = self.get_current_track_file()
        try:
            pygame.mixer.music.load(track)
            pygame.mixer.music.play()
        except Exception as e:
            print("Hiba a lejátszás során:", e)

    def pause(self):
        pygame.mixer.music.pause()
        
    def is_playing(self):
        return pygame.mixer.music.get_busy()


    def unpause(self):
        pygame.mixer.music.unpause()

    def stop(self):
        pygame.mixer.music.stop()

    def next_track(self):
        if not self.tracks:
            return
        self.current_index = (self.current_index + 1) % len(self.tracks)
        self.play()

    def previous_track(self):
        if not self.tracks:
            return
        self.current_index = (self.current_index - 1) % len(self.tracks)
        self.play()

    def set_volume(self, value):
        vol = max(0, min(value, 100)) / 100.0
        pygame.mixer.music.set_volume(vol)

    def get_volume(self):
        return int(pygame.mixer.music.get_volume() * 100)

    # Itt adjuk hozzá a media_count metódust:
    def media_count(self):
        return len(self.tracks)
