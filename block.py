"""
Block class

======= CLASS INFO =======
The various files with classes are used by s2p_unpacker and the correct data is
set. Those are then used to build the project in main.py.
"""

import random
import i18n
import config
import math
import pygame
import eventContainer
from scratch import KEY_MAPPING

i18n.set("locale", config.language)
i18n.set("filename_format", "{locale}.{format}")
i18n.load_path.append("lang/")
_ = i18n.t


class Block:
    def __init__(self):
        self.blockID = ""
        self.opcode = ""  # block type
        self.next = None  # next block
        self.parent = None  # previous block
        self.top = None  # script start
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
        self.substack2 = set()  # only for if then else
        self.script = set()  # blocks below
        self.screenRefresh = False  # do a screen refresh
        self.inEventLoop = False
        self.value = None  # reported value
        self.repeatCounter = None  # for repeat block
        self.canRun = None  # for if then / if then else

    # Evaluates block value (for reporters)
    def evaluateBlockValue(self, eventContainer=eventContainer.EventContainer):
        if self.opcode == "operator_add":  # () + ()
            self.value = float(self.getInputValue("num1")) + float(self.getInputValue("num2"))
            return self.value
        elif self.opcode == "operator_subtract":  # () - ()
            self.value = float(self.getInputValue("num1")) - float(self.getInputValue("num2"))
            return self.value
        elif self.opcode == "operator_multiply":  # () * ()
            self.value = float(self.getInputValue("num1")) * float(self.getInputValue("num2"))
            return self.value
        elif self.opcode == "operator_divide":  # () / ()
            try:
                self.value = float(self.getInputValue("num1")) / float(self.getInputValue("num2"))
            except ZeroDivisionError:
                raise ZeroDivisionError(_("zero-division-error"))
            return self.value

        elif self.opcode == "operator_random":  # pick random from () to ()
            decimals1 = len(str(math.modf(float(self.getInputValue("from"))))) - 2
            decimals2 = len(str(math.modf(float(self.getInputValue("to"))))) - 2
            if decimals1 > decimals2:
                decimals = decimals1
            else:
                decimals = decimals2
            self.value = random.randint(int(self.getInputValue("from")) * 10 ** decimals, int(self.getInputValue("to")) * 10 ** decimals) / 10 ** decimals
            return self.value

        elif self.opcode == "operator_equals":  # () = ()
            self.value = self.getInputValue("operand1") == self.getInputValue("operand2")
            return self.value
        elif self.opcode == "operator_lt":  # () < ()
            self.value = self.getInputValue("operand1") < self.getInputValue("operand2")
            return self.value
        elif self.opcode == "operator_gt":  # () > ()
            self.value = self.getInputValue("operand1") > self.getInputValue("operand2")
            return self.value

        elif self.opcode == "motion_xposition":  # x position
            self.value = self.target.x
            return self.value
        elif self.opcode == "motion_xposition":  # y position
            self.value = self.target.y
            return self.value
        elif self.opcode == "motion_direction":  # y position
            self.value = self.target.direction
            return self.value

        elif self.opcode == "sensing_mousex":  # mouse x
            newX, newY = pygame.mouse.get_pos()
            newX = newX - config.screenWidth // 2
            self.value = newX
            return self.value
        elif self.opcode == "sensing_mousey":  # mouse y
            newX, newY = pygame.mouse.get_pos()
            newY = newY - config.screenHeight // 2
            self.value = newY
            return self.value

        elif self.opcode == "sensing_keypressed":  # key pressed?
            self.value = KEY_MAPPING[self.getMenuValue("key_option")] in eventContainer.keys
            return self.value
        elif self.opcode == "sensing_mousedown":  # mouse down?
            self.value = pygame.mouse.get_pressed()[0]
            return self.value

        elif self.opcode == "operator_not":  # not <>
            self.value = not self.target.blocks[self.getBlockInputValue("operand")].evaluateBlockValue(eventContainer)
            return self.value
        elif self.opcode == "operator_and":  # <> and <>
            self.value = self.target.blocks[self.getBlockInputValue("operand1")].evaluateBlockValue(eventContainer) and self.target.blocks[self.getBlockInputValue("operand2")].evaluateBlockValue(eventContainer)
            return self.value
        elif self.opcode == "operator_or":  # <> or <>
            self.value = self.target.blocks[self.getBlockInputValue("operand1")].evaluateBlockValue(eventContainer) or self.target.blocks[self.getBlockInputValue("operand2")].evaluateBlockValue(eventContainer)
            return self.value

    # Returns block input value
    def getBlockInputValue(self, inputId):
        return self.inputs[inputId.upper()][1]

    # Returns block input value
    def getInputValue(self, inputId, lookIn=(1, 1), eventContainer=eventContainer.EventContainer()):
        if self.inputs[inputId.upper()][lookIn[0]][0] in {4, 0, 5, 6, 8}:
            return self.inputs[inputId.upper()][lookIn[0]][1] or 0
        elif self.inputs[inputId.upper()][0] == 3:
            blockLink = self.inputs[inputId.upper()][1]
            return self.target.blocks[blockLink].evaluateBlockValue(eventContainer)
        else:
            pass

    # Returns custom block input value
    def getCustomInputValue(self, number, lookIn=(1, 1)):
        return self.inputs["arg" + str(number)][lookIn[0]][lookIn[1]]

    # Returns dropdown menu value (menus are separate blocks)
    def getMenuValue(self, menuId):
        return self.target.blocks[self.inputs[menuId.upper()][1]].fields[menuId.upper()][0]

    # Returns field value (menus are separate blocks)
    def getFieldValue(self, fieldId, lookIn=0):
        return self.fields[fieldId.upper()][lookIn]
