"""
Sound class

======= CLASS INFO =======
The various files with classes are used by s2p_unpacker and the correct data is
set. Those are then used to build the project in main.py.
"""

import pygame.mixer

class Sound:
    def __init__(self):
        self.dataFormat = "wav"
        self.rate = 44100
        self.sampleCount = 1024
        self.md5ext = ""
        self.file = None
        self.name = ""  # display name

    def play(self):
        # TODO
        mixer = pygame.mixer.Sound(buffer=self.file)
        mixer.play()
        pygame.time.wait(int(mixer.get_length()) * 1000)
