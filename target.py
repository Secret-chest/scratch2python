"""
Target(sprite) class

======= CLASS INFO =======
The various files with classes are used by s2p_unpacker and the correct data is
set. Those are then used to build the project in main.py.
"""


class Target:
    def __init__(self):
        self.isStage = False
        self.variables = {}
        self.lists = {}
        self.blocks = {}
        self.currentCostume = 0
        self.costumes = []
        self.sounds = []
        self.volume = 100
        self.layerOrder = 1  # 0 is only for the bg image, lower value = background position
        self.visible = True
        self.x = 0
        self.y = 0
        self.size = 100
        self.direction = 90
        self.draggable = False
        self.rotationStyle = "all around"  # all around, left-right or do not rotate
        self.sprite = None
