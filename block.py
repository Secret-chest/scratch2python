"""
Block class

======= CLASS INFO =======
The various files with classes are used by s2p_unpacker and the correct data is
set. Those are then used to build the project in main.py.
"""

import random

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
        self.timeDelay = 0  # wait time from the wait block
        self.target = None  # parent
        self.substack = set()  # blocks inside
        self.script = set()  # blocks below
        self.screenRefresh = False  # do a screen refresh
        self.inEventLoop = False
        self.value = None  # reported value

    # Evaluates block value (for reporters)
    def evaluateBlockValue(self):
        if self.opcode == "operator_add":  # () + ()
            self.value = float(self.getInputValue("num1")) + float(self.getInputValue("num2"))
            return self.value
        if self.opcode == "operator_subtract":  # () - ()
            self.value = float(self.getInputValue("num1")) - float(self.getInputValue("num2"))
            return self.value
        if self.opcode == "operator_multiply":  # () * ()
            self.value = float(self.getInputValue("num1")) * float(self.getInputValue("num2"))
            return self.value
        if self.opcode == "operator_divide":  # () / ()
            try:
                self.value = float(self.getInputValue("num1")) / float(self.getInputValue("num2"))
            except ZeroDivisionError:
                raise ZeroDivisionError("Project was trying to divide by 0")
            return self.value

    # Returns block input value
    def getBlockInputValue(self, inputId):
        return self.inputs[inputId.upper()][1]

    # Returns block input value
    def getInputValue(self, inputId, lookIn=(1, 1)):
        if self.inputs[inputId.upper()][lookIn[0]][0] in {4, 0, 5}:
            return self.inputs[inputId.upper()][lookIn[0]][1] or 0
        elif self.inputs[inputId.upper()][0] == 3:
            blockLink = self.inputs[inputId.upper()][1]
            return self.target.blocks[blockLink].evaluateBlockValue()
        else:
            pass

    # Returns custom block input value
    def getCustomInputValue(self, number, lookIn=(1, 1)):
        return self.inputs["arg" + str(number)][lookIn[0]][lookIn[1]]

    # Returns dropdown menu value (menus are separate blocks)
    def getMenuValue(self, menuId):
        return self.inputs[menuId.upper()][1].fields[menuId.upper()][0]

    # Returns field value (menus are separate blocks)
    def getFieldValue(self, fieldId, lookIn=0):
        return self.fields[fieldId.upper()][lookIn]
