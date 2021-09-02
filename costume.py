"""
Costume class

======= CLASS INFO =======
The various files with classes are used by s2p_unpacker and the correct data is
set. Those are then used to build the project in main.py.
"""


class Costume:
    def __init__(self):
        self.md5ext = ""
        self.dataFormat = "svg"
        self.rotationCenterX = 240
        self.rotationCenterY = 180
        self.file = None
