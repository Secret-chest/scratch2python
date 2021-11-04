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
        self.substack = set()
        self.screenRefresh = False

    # Returns block input value
    def getInputValue(self, inputId, lookIn=(1, 1)):
        return self.inputs[inputId.upper()][lookIn[0]][lookIn[1]]

    # Returns dropdown menu value (menus are separate blocks)
    def getMenuValue(self, menuId):
        return self.inputs[menuId.upper()][1].fields[menuId.upper()][0]

    # Returns field value (menus are separate blocks)
    def getFieldValue(self, fieldId, lookIn=0):
        return self.fields[fieldId.upper()][lookIn]

    # Returns block input value
    def getBlockInputValue(self, inputId):
        return self.inputs[inputId.upper()][1]
