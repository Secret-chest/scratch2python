"""
Block class

======= CLASS INFO =======
The various files with classes are used by s2p_unpacker and the correct data is
set. Those are then used to build the project in main.py.
"""


class Block:
    def __init__(self):
        self.blockID = ""
        self.opcode = ""  # block type
        self.next = None  # next block
        self.parent = None  # previous block
        self.inputs = {}  # string and number inputs
        self.fields = {}  # dropdown menus
        self.shadow = False  # if the block is a reporter or boolean block
        self.topLevel = False  # if the block is a hat block
        self.blockRan = False
        self.waiting = False
        self.executionTime = 0
        self.timeDelay = 0
        self.target = None
