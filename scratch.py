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

i18n.set("locale", config.language)
i18n.set("filename_format", "{locale}.{format}")
i18n.load_path.append("lang/")
_ = i18n.t


if not config.enableDebugMessages:
    sys.stderr = open(os.devnull, "w")
if not config.enableTerminalOutput:
    sys.stdout = open(os.devnull, "w")


HEIGHT = config.projectScreenHeight
WIDTH = config.projectScreenWidth

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
    "f12": pygame.K_F12
}


# Load SVG
def loadSvg(svgBytes):
    newBytes = cairosvg.svg2png(bytestring=svgBytes)
    byteIo = io.BytesIO(newBytes)
    return pygame.image.load(byteIo)


# Refresh screen resolution
def refreshScreenResolution():
    global HEIGHT
    global WIDTH
    HEIGHT = config.projectScreenHeight
    WIDTH = config.projectScreenWidth


# Run the given block object
def execute(block, s, keys=[]):
    # Get block values
    opcode = block.opcode
    id = block.blockID
    blockRan = block.blockRan
    inputs = block.inputs
    fields = block.fields
    shadow = block.shadow
    nextBlock = None

    if opcode == "motion_gotoxy":  # go to x: () y: ()
        s.setXy(int(block.getInputValue("x")), int(block.getInputValue("y")))

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
        s.setXy(int(block.getInputValue("x")), s.y)

    elif opcode == "motion_changexby":  # change x by ( )
        s.setXyDelta(int(block.getInputValue("dx")), 0)

    elif opcode == "motion_sety":  # set y to ()
        s.setXy(s.x, int(block.getInputValue("y")))

    elif opcode == "motion_changeyby":  # change y by ()
        s.setXyDelta(0, int(block.getInputValue("dy")))

    elif opcode == "control_wait":  # wait () seconds
        block.screenRefresh = True
        if not block.waiting:
            # Get time delay and convert it to milliseconds
            block.timeDelay = int(round(float(float(block.getInputValue("duration"))) * 1000))
            block.waiting = True
            block.executionTime = 0
            print(_("debug-prefix"), _("block-waiting", time=block.timeDelay), file=sys.stderr)
        return block

    elif opcode == "event_whenflagclicked":  # when green flag clicked
        pass

    elif opcode == "event_whenkeypressed":
        # if not block.waiting:
        #     # Get time delay and convert it to milliseconds
        #     block.timeDelay = 500
        #     block.waiting = True
        #     block.executionTime = 0
        #     print("DEBUG: Waiting for", block.timeDelay, "ms")
        key = block.getFieldValue("key_option", lookIn=0)

        if key == "any":  # when key [any v] pressed
            if keys:
                print(_("debug-prefix"), _("keypress-handling", keyName=_("key-any")), file=sys.stderr)
                for b in block.script:
                    s.target.blocks[b].blockRan = False
                nb = block  # s.target.blocks[block.next]
                nb.blockRan = False
                block.script.add(nb.blockID)
                while nb.next and nb.next != block.blockID:
                    nb.blockRan = False
                    nb.timeDelay = 0
                    nb.executionTime = 0
                    nb = s.target.blocks[nb.next]
                    block.script.add(nb.blockID)
                    if not nb.next:
                        nb.next = block.blockID
                nb.blockRan = False
                nextBlock = s.target.blocks[block.next]
                return nextBlock

        elif KEY_MAPPING[key] in keys and block.next:  # when key [. . . v] pressed
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
            for b in block.script:
                s.target.blocks[b].blockRan = False
            nb = block  # s.target.blocks[block.next]
            nb.blockRan = False
            block.script.add(nb.blockID)
            while nb.next and nb.next != block.blockID:
                nb.blockRan = False
                nb.timeDelay = 0
                nb.executionTime = 0
                nb = s.target.blocks[nb.next]
                block.script.add(nb.blockID)
                if not nb.next:
                    nb.next = block.blockID
            nb.blockRan = False
            nextBlock = s.target.blocks[block.next]
            return nextBlock

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

    elif opcode == "control_repeat":  # repeat (10) {..}
        if block.repeatCounter is None:
            block.repeatCounter = int(block.getInputValue("times"))
        # Don't mark the loop as ran until done, and do a screen refresh
        if block.repeatCounter > 1:
            block.blockRan = False
        else:
            block.blockRan = True
            block.repeatCounter = None
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

    elif opcode == "looks_switchcostumeto":  # switch costume to [ v]
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

    elif opcode == "sound_play":  # start sound [ v]
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
            if block.proccode == "​​log​​ %s":  # Scratch Addons log ()
                print(_("project-log"), block.getCustomInputValue(0), file=sys.stderr)
            elif block.proccode == "​​warn​​ %s":  # Scratch Addons warn ()
                print(_("project-warn"), block.getCustomInputValue(0), file=sys.stderr)
            elif block.proccode == "​​error​​ %s":  # Scratch Addons error ()
                print(_("project-error"), block.getCustomInputValue(0), file=sys.stderr)

    else:
        print(_("unknown-opcode"), opcode)

    # If there is a block below, return it
    if block.next:
        nextBlock = s.target.blocks[block.next]
    block.blockRan = True

    return nextBlock
