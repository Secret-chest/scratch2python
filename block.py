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
