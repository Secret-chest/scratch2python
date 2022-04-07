"""
Sound class

======= CLASS INFO =======
The various files with classes are used by s2p_unpacker and the correct data is
set. Those are then used to build the project in main.py.
"""


class Sound:
    def __init__(self):
        self.dataFormat = "wav"
        self.rate = 44100
        self.sampleCount = 1032
        self.md5ext = ""
        self.name = ""  # display name