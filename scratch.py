"""
This module runs Scratch blocks on demand.
Basically it emulates Scratch in Pygame, hence the name.
"""
import sys
import os
import random
import pygame.time
import cairosvg
import io
import config
import i18n
import targetSprite
import bs4
import time
from datetime import datetime
import eventContainer
from pathlib import Path
import tkinter as tk
import downloader
from tkinter import filedialog
import tkinter.simpledialog

__version__ = "v0.8.0"
__author__ = "Secret-chest"

i18n.set("locale", config.language)
i18n.set("filename_format", "{locale}.{format}")
i18n.load_path.append("lang/")
_ = i18n.t


class SpriteNotFoundError(Exception):
    pass


if not config.enableDebugMessages:
    sys.stderr = open(os.devnull, "w")
if not config.enableTerminalOutput:
    sys.stdout = open(os.devnull, "w")


# Start tkinter for showing some popups, and hide main window
mainWindow = tk.Tk()
mainWindow.withdraw()


# Get project file name based on options and arguments
if len(sys.argv) > 1:
    setProject = sys.argv[1]
else:
    if config.testMode:
        if not config.projectFileName.endswith(".sb3"):
            if "http" not in config.projectFileName\
               or "https" not in config.projectFileName:
                setProject = downloader.downloadByID(config.projectFileName, "./download")
            else:
                setProject = downloader.downloadByURL(config.projectFileName, "./download")
        else:
            setProject = config.projectFileName
    else:
        fileTypes = [(_("sb3-desc"), ".sb3"), (_("all-files-desc"), ".*")]
        setProject = filedialog.askopenfilename(parent=mainWindow,
                                                initialdir=os.getcwd(),
                                                title=_("choose-project-title"),
                                                filetypes=fileTypes)


HEIGHT = config.projectScreenHeight
WIDTH = config.projectScreenWidth

# Create project player and window
projectName = Path(setProject).stem
icon = pygame.image.load("icon.svg")
display = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(_("window-title", projectName=projectName, s2pVersionString="Scratch2Python " + __version__))
pygame.display.set_icon(icon)

# Key maps to convert the key option in blocks to Pygame constants
KEY_MAPPING = {
    "up arrow": pygame.K_UP,
    "down arrow": pygame.K_DOWN,
    "left arrow": pygame.K_LEFT,
    "right arrow": pygame.K_RIGHT,
    "space": pygame.K_SPACE,
    "a": pygame.K_a,
    "b": pygame.K_b,
    "c": pygame.K_c,
    "d": pygame.K_d,
    "e": pygame.K_e,
    "f": pygame.K_f,
    "g": pygame.K_g,
    "h": pygame.K_h,
    "i": pygame.K_i,
    "j": pygame.K_j,
    "k": pygame.K_k,
    "l": pygame.K_l,
    "m": pygame.K_m,
    "n": pygame.K_n,
    "o": pygame.K_o,
    "p": pygame.K_p,
    "q": pygame.K_q,
    "r": pygame.K_r,
    "s": pygame.K_s,
    "t": pygame.K_t,
    "u": pygame.K_u,
    "v": pygame.K_v,
    "w": pygame.K_w,
    "x": pygame.K_x,
    "y": pygame.K_y,
    "z": pygame.K_z,
    "0": pygame.K_0,
    "1": pygame.K_1,
    "2": pygame.K_2,
    "3": pygame.K_3,
    "4": pygame.K_4,
    "5": pygame.K_5,
    "6": pygame.K_6,
    "7": pygame.K_7,
    "8": pygame.K_8,
    "9": pygame.K_9,

    # Scratch supports these keys internally
    "enter": pygame.K_RETURN,
    "<": pygame.K_LESS,
    ">": pygame.K_GREATER,
    "+": pygame.K_PLUS,
    "-": pygame.K_MINUS,
    "=": pygame.K_EQUALS,
    ".": pygame.K_PERIOD,
    ",": pygame.K_COMMA,
    "%": pygame.K_PERCENT,
    "$": pygame.K_DOLLAR,
    "#": pygame.K_HASH,
    "@": pygame.K_AT,
    "!": pygame.K_EXCLAIM,
    "^": pygame.K_CARET,
    "&": pygame.K_AMPERSAND,
    "*": pygame.K_ASTERISK,
    "(": pygame.K_LEFTPAREN,
    ")": pygame.K_RIGHTPAREN,
    "[": pygame.K_LEFTBRACKET,
    "]": pygame.K_RIGHTBRACKET,
    "?": pygame.K_QUESTION,
    "\\": pygame.K_BACKSLASH,
    "/": pygame.K_SLASH,
    "'": pygame.K_QUOTE,
    "\"": pygame.K_QUOTEDBL,
    "`": pygame.K_BACKQUOTE,

    # Scratch2Python only
    "backspace": pygame.K_BACKSPACE,
    "escape": pygame.K_ESCAPE,
    "f1": pygame.K_F1,
    "f2": pygame.K_F2,
    "f3": pygame.K_F3,
    "f4": pygame.K_F4,
    "f5": pygame.K_F5,
    "f6": pygame.K_F6,
    "f7": pygame.K_F7,
    "f8": pygame.K_F8,
    "f9": pygame.K_F9,
    "f10": pygame.K_F10,
    "f11": pygame.K_F11,
    "f12": pygame.K_F12,
}


# Load SVG
def loadSvg(svgBytes):
    svg = bs4.BeautifulSoup(svgBytes, "lxml-xml")
    if svg.find("svg")["width"] == "0" or svg.find("svg")["height"] == "0":
        svg.find("svg")["width"], svg.find("svg")["height"] = 1, 1
    newBytes = cairosvg.svg2png(bytestring=str(svg))
    byteIo = io.BytesIO(newBytes)
    return pygame.image.load(byteIo)


# Refresh screen resolution
def refreshScreenResolution():
    global HEIGHT
    global WIDTH
    HEIGHT = config.projectScreenHeight
    WIDTH = config.projectScreenWidth


# Get the stage sprite in the current project
def getStage():
    for s in targetSprite.sprites:
        if s.isStage:
            return s
    raise SpriteNotFoundError(_("stage-not-found"))


# Run the given block object
def execute(block, s, events=eventContainer.EventContainer()):
    # Get block values
    opcode = block.opcode
    blockRan = block.blockRan
    inputs = block.inputs
    fields = block.fields
    shadow = block.shadow
    nextBlock = None

    # Get keys
    keys = events.keys
    keyEvents = events.keyEvents

    if opcode == "motion_gotoxy":  # go to x: () y: ()
        s.setXy(float(block.getInputValue("x", eventContainer=events)), float(block.getInputValue("y", eventContainer=events)))

    elif opcode == "motion_goto":
        nextBlock = block.getBlockInputValue("to")
        return s.target.blocks[nextBlock]

    elif opcode == "motion_goto_menu":
        if block.getFieldValue("to") == "_mouse_":  # go to [mouse pointer v]
            newX, newY = pygame.mouse.get_pos()
            newX = newX - WIDTH // 2
            newY = HEIGHT // 2 - newY
            s.setXy(newX, newY)
            if s.target.blocks[block.parent].next:
                return s.target.blocks[s.target.blocks[block.parent].next]
            return

        elif block.getFieldValue("to") == "_random_":  # go to [random position v]
            minX = 0 - WIDTH // 2
            maxX = WIDTH // 2
            minY = 0 - HEIGHT // 2
            maxY = HEIGHT // 2
            newX, newY = (random.randint(minX, maxX), random.randint(minY, maxY))
            s.setXy(newX, newY)
            if s.target.blocks[block.parent].next:
                return s.target.blocks[s.target.blocks[block.parent].next]
            return

    elif opcode == "motion_setx":  # set x to ()
        s.setXy(float(block.getInputValue("x", eventContainer=events)), s.y)

    elif opcode == "motion_changexby":  # change x by ( )
        s.setXyDelta(float(block.getInputValue("dx", eventContainer=events)), 0)

    elif opcode == "motion_sety":  # set y to ()
        s.setXy(s.x, float(block.getInputValue("y", eventContainer=events)))

    elif opcode == "motion_changeyby":  # change y by ()
        s.setXyDelta(0, float(block.getInputValue("dy", eventContainer=events)))

    elif opcode == "motion_turnleft":  # turn ccw () degrees
        s.setRotDelta(0 - float(block.getInputValue("degrees", eventContainer=events)))

    elif opcode == "motion_turnright":  # turn cw () degrees
        s.setRotDelta(float(block.getInputValue("degrees", eventContainer=events)))

    elif opcode == "motion_pointindirection":  # point in direction ()
        s.setRot(float(block.getInputValue("direction", eventContainer=events)))

    elif opcode == "control_wait":  # wait () seconds
        block.screenRefresh = True
        if not block.waiting:
            # Get time delay and convert it to milliseconds
            block.timeDelay = int(round(float(float(block.getInputValue("duration", eventContainer=events))) * 1000))
            block.waiting = True
            block.executionTime = 0
            print(_("debug-prefix"), _("block-waiting", time=block.timeDelay), file=sys.stderr)
        return block

    elif opcode == "control_wait_until":  # wait until <>
        block.screenRefresh = True
        truth = block.target.blocks[inputs["CONDITION"][1]].evaluateBlockValue(events)
        if truth:
            block.blockRan = True
            nextBlock = s.target.blocks[block.next]
            return nextBlock
        else:
            return block

    elif opcode == "event_whenflagclicked":  # when green flag clicked
        pass

    elif opcode == "event_whenkeypressed":
        # print(time.time_ns(), "in whenkeypressed")

        # print("Handling key event")
        # if not block.waiting:
        #     # Get time delay and convert it to milliseconds
        #     block.timeDelay = 500
        #     block.waiting = True
        #     block.executionTime = 0
        #     print("DEBUG: Waiting for", block.timeDelay, "ms")
        key = block.getFieldValue("key_option", lookIn=0)
        # print(key)

        if key == "any":  # when key [any v] pressed
            if keyEvents and keys and block.next:
                print(_("debug-prefix"), _("keypress-handling", keyName=_("key-any")), file=sys.stderr)
                # print(time.time_ns() // 1000000, keyName)
                for b in block.script:
                    s.target.blocks[b].blockRan = False
                nb = block  # s.target.blocks[block.next]
                # nb.blockRan = False
                block.script.add(nb.blockID)
                nb = s.target.blocks[nb.next]
                while nb.next and nb.next != block.blockID:
                    # Reset block
                    nb.blockRan = False
                    nb.timeDelay = 0
                    nb.executionTime = 0

                    block.script.add(nb.blockID)
                    nb = s.target.blocks[nb.next]
                    if not nb.next:
                        nb.next = block.blockID
                if nb:
                    block.script.add(nb.blockID)
                block.script.remove(block.blockID)
                nb.blockRan = False
                nextBlock = s.target.blocks[block.next]
                return nextBlock
        elif KEY_MAPPING[key] in keyEvents and block.next:  # when key [. . . v] pressed
            # print(keyEvents, "received in execute()")
            if key == "left arrow":
                keyName = _("key-left")
            elif key == "right arrow":
                keyName = _("key-right")
            elif key == "up arrow":
                keyName = _("key-up")
            elif key == "down arrow":
                keyName = _("key-down")
            elif key == "space":
                keyName = _("key-space")
            else:
                keyName = key
            print(_("debug-prefix"), _("keypress-handling", keyName=keyName), file=sys.stderr)
            # print(time.time_ns() // 1000000, keyName)
            for b in block.script:
                s.target.blocks[b].blockRan = False
            nb = block  # s.target.blocks[block.next]
            # nb.blockRan = False
            block.script.add(nb.blockID)
            nb = s.target.blocks[nb.next]
            while nb.next and nb.next != block.blockID:
                # Reset block
                nb.blockRan = False
                nb.timeDelay = 0
                nb.executionTime = 0

                block.script.add(nb.blockID)
                nb = s.target.blocks[nb.next]
                if not nb.next:
                    nb.next = block.blockID
            if nb:
                block.script.add(nb.blockID)
            block.script.remove(block.blockID)
            nb.blockRan = False
            nextBlock = s.target.blocks[block.next]
            return nextBlock
        else:
            pass

        block.blockRan = False
        return None

    elif opcode == "control_forever":  # forever {..}
        # Don't mark the loop as ran, and do a screen refresh
        block.blockRan = False
        block.screenRefresh = True

        # If there are blocks, get them
        if inputs["SUBSTACK"][1]:
            # No blocks will be flagged as ran inside a forever loop
            for b in block.substack:
                s.target.blocks[b].blockRan = False
            nextBlock = s.target.blocks[inputs["SUBSTACK"][1]]
            nb = s.target.blocks[inputs["SUBSTACK"][1]]
            block.substack.add(nb.blockID)
            while nb.next and nb.next != block.blockID:
                nb.blockRan = False
                nb.waiting = False
                nb.timeDelay = 0
                nb.executionTime = 0
                nb = s.target.blocks[nb.next]
                block.substack.add(nb.blockID)
            nb.next = block.blockID
            return nextBlock

    elif opcode == "control_repeat":  # repeat (10) {...}
        if block.repeatCounter is None:
            block.repeatCounter = int(block.getInputValue("times", eventContainer=events))
        # Don't mark the loop as ran until done, and do a screen refresh
        if block.repeatCounter > 0:
            block.blockRan = False
        else:
            block.blockRan = True
            block.repeatCounter = None
            if block.next:
                return s.target.blocks[block.next]
            else:
                return
        block.screenRefresh = True

        if block.repeatCounter is not None:
            block.repeatCounter -= 1

        # If there are blocks, get them
        if inputs["SUBSTACK"][1]:
            # No blocks will be flagged as ran inside a forever loop
            for b in block.substack:
                s.target.blocks[b].blockRan = False
            nextBlock = s.target.blocks[inputs["SUBSTACK"][1]]
            nb = s.target.blocks[inputs["SUBSTACK"][1]]
            block.substack.add(nb.blockID)
            while nb.next and nb.next != block.blockID:
                nb.blockRan = False
                nb.waiting = False
                nb.timeDelay = 0
                nb.executionTime = 0
                nb = s.target.blocks[nb.next]
                block.substack.add(nb.blockID)
            nb.next = block.blockID
            return nextBlock

    elif opcode == "control_if":  # if <> then {...}
        if block.target.blocks[inputs["CONDITION"][1]].evaluateBlockValue(events):
            # If there are blocks, get them
            if inputs["SUBSTACK"][1]:
                # No blocks will be flagged as ran inside a forever loop
                for b in block.substack:
                    s.target.blocks[b].blockRan = False
                nextBlock = s.target.blocks[inputs["SUBSTACK"][1]]
                nb = s.target.blocks[inputs["SUBSTACK"][1]]
                block.substack.add(nb.blockID)
                while nb.next and nb.next not in block.substack:
                    nb.blockRan = False
                    nb.waiting = False
                    nb.timeDelay = 0
                    nb.executionTime = 0
                    nb = s.target.blocks[nb.next]
                    block.substack.add(nb.blockID)
                nb.next = block.next
                block.blockRan = True
                return nextBlock
            block.blockRan = True
        else:
            block.blockRan = True
            return s.target.blocks[block.next]

    elif opcode == "control_if_else":  # if <> then {...}
        if block.target.blocks[inputs["CONDITION"][1]].evaluateBlockValue(events):
            # If there are blocks, get them
            if inputs["SUBSTACK"][1]:
                # No blocks will be flagged as ran inside a forever loop
                for b in block.substack:
                    s.target.blocks[b].blockRan = False
                nextBlock = s.target.blocks[inputs["SUBSTACK"][1]]
                nb = s.target.blocks[inputs["SUBSTACK"][1]]
                block.substack.add(nb.blockID)
                while nb.next and nb.next not in block.substack:
                    nb.blockRan = False
                    nb.waiting = False
                    nb.timeDelay = 0
                    nb.executionTime = 0
                    nb = s.target.blocks[nb.next]
                    block.substack.add(nb.blockID)
                nb.next = block.next
                block.blockRan = True
                return nextBlock
            block.blockRan = True
        else:
            # If there are blocks, get them
            if inputs["SUBSTACK2"][1]:
                # No blocks will be flagged as ran inside a forever loop
                for b in block.substack2:
                    s.target.blocks[b].blockRan = False
                nextBlock = s.target.blocks[inputs["SUBSTACK2"][1]]
                nb = s.target.blocks[inputs["SUBSTACK2"][1]]
                block.substack2.add(nb.blockID)
                while nb.next and nb.next not in block.substack2:
                    nb.blockRan = False
                    nb.waiting = False
                    nb.timeDelay = 0
                    nb.executionTime = 0
                    nb = s.target.blocks[nb.next]
                    block.substack2.add(nb.blockID)
                nb.next = block.next
                block.blockRan = True
                return nextBlock
            block.blockRan = True

    elif opcode == "looks_switchcostumeto":  # switch costume to [... v]
        nextBlock = block.getBlockInputValue("costume")
        return s.target.blocks[nextBlock]

    elif opcode == "looks_nextcostume":  # next costume
        s.setCostume(s.target.currentCostume + 1)

    elif opcode == "looks_costume":
        if s.target.blocks[block.parent].opcode == "looks_switchcostumeto":
            costumeName = block.getFieldValue("costume")
            newCostume = 0
            for c in s.target.costumes:
                if c.name == costumeName:
                    break
                newCostume += 1
            s.setCostume(newCostume)
        if s.target.blocks[block.parent].next:
            return s.target.blocks[s.target.blocks[block.parent].next]
        return

    elif opcode == "looks_switchbackdropto":  # switch backdrop to [... v]
        nextBlock = block.getBlockInputValue("backdrop")
        return s.target.blocks[nextBlock]

    elif opcode == "looks_nextbackdrop":  # next backdrop
        getStage().setCostume(getStage().target.currentCostume + 1)

    elif opcode == "looks_backdrops":
        if s.target.blocks[block.parent].opcode == "looks_switchbackdropto":
            backdropName = block.getFieldValue("backdrop")
            newBackdrop = 0
            for c in getStage().target.costumes:
                if c.name == backdropName:
                    break
                newBackdrop += 1
            getStage().setCostume(newBackdrop)
        if s.target.blocks[block.parent].next:
            return s.target.blocks[s.target.blocks[block.parent].next]
        return

    elif opcode == "sound_play":  # start sound [... v]
        nextBlock = block.getBlockInputValue("sound_menu")
        return s.target.blocks[nextBlock]

    elif opcode == "sound_sounds_menu":
        if s.target.blocks[block.parent].opcode == "sound_play":
            soundName = block.getFieldValue("sound_menu")
            newSound = None
            for so in s.target.sounds:
                if so.name == soundName:
                    newSound = so
                    break
            newSound.play()
        if s.target.blocks[block.parent].next:
            return s.target.blocks[s.target.blocks[block.parent].next]
        return

    elif opcode == "procedures_call":
        if config.showSALogs:
            # These are Scratch Addons debugger blocks.
            if block.proccode == "​​log​​ %s":  # Scratch Addons log ()
                print("[", datetime.now().strftime("%H:%M:%S:%f"), "]", _("project-log"),  block.getCustomInputValue(0), file=sys.stderr)
            elif block.proccode == "​​warn​​ %s":  # Scratch Addons warn ()
                print("[", datetime.now().strftime("%H:%M:%S:%f"), "]", _("project-warn"), block.getCustomInputValue(0), file=sys.stderr)
            elif block.proccode == "​​error​​ %s":  # Scratch Addons error ()
                print("[", datetime.now().strftime("%H:%M:%S:%f"), "]", _("project-error"), block.getCustomInputValue(0), file=sys.stderr)

    else:
        print(_("unknown-opcode"), opcode)

    # If there is a block below, return it
    if block.next:
        nextBlock = s.target.blocks[block.next]
    block.blockRan = True

    return nextBlock
