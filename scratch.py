"""
This file runs Scratch blocks, and stuff like that. Basically
it simulates Scratch using the Scratch2Python file, hence the name.
"""
# Scratch project functions
# Green flag event
import pygame.time
import cairosvg
import io
HEIGHT = 360
WIDTH = 480
KEY_MAPPING = {
    "up arrow": pygame.K_UP,
    "down arrow": pygame.K_DOWN,
    "left arrow": pygame.K_LEFT,
    "right arrow": pygame.K_RIGHT,
    "enter": pygame.K_RETURN,
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
def loadSvg(svg_bytes):
    newBites = cairosvg.svg2png(bytestring=svg_bytes)
    byteIo = io.BytesIO(newBites)
    return pygame.image.load(byteIo)


# Render a sprite at its coordinates
def render(sprite, x, y, direction, display):
    # Set direction
    sprite = pygame.transform.rotate(sprite, 90 - direction)
    # Convert Scratch coordinates into Pygame coordinates
    finalX = x + WIDTH // 2 - sprite.get_width() // 2
    finalY = HEIGHT // 2 - y - sprite.get_height() // 2
    display.blit(sprite, (finalX, finalY))


# Set the stage background
def setBackground(bg, display):
    render(bg, 0, 0, 90, display)


# Project start event
def startProject():
    print("DEBUG: Project start event")


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

    if opcode == "motion_goto":
        nextBlock = block.getBlockInputValue("to")
        return s.target.blocks[nextBlock]

    if opcode == "motion_goto_menu":
        if block.getFieldValue("to") == "_mouse_":  # go to [mouse pointer v]
            newX, newY = pygame.mouse.get_pos()
            newX = newX - WIDTH // 2
            newY = HEIGHT // 2 - newY
            s.setXy(newX, newY)
            return s.target.blocks[s.target.blocks[block.parent].next]

    if opcode == "motion_setx":  # set x to ()
        s.setXy(int(block.getInputValue("x")), s.y)

    if opcode == "motion_changexby":  # change x by ()
        s.setXy(s.x + int(block.getInputValue("dx")), s.y)

    if opcode == "motion_sety":  # set y to ()
        s.setXy(s.x, int(block.getInputValue("y")))

    if opcode == "motion_changeyby":  # change y by ()
        s.setXy(s.x, s.y + int(block.getInputValue("dy")))

    if opcode == "control_wait":  # wait () seconds
        if not block.waiting:
            # Get time delay and convert it to milliseconds
            block.timeDelay = int(round(float(int(block.getInputValue("duration"))) * 1000))
            block.waiting = True
            block.executionTime = 0
            print("DEBUG: Waiting for", block.timeDelay, "ms")
        return block

    if opcode == "event_whenflagclicked":  # when green flag clicked
        pass

    if opcode == "event_whenkeypressed":  # when key [... v] pressed
        # if not block.waiting:
        #     # Get time delay and convert it to milliseconds
        #     block.timeDelay = 500
        #     block.waiting = True
        #     block.executionTime = 0
        #     print("DEBUG: Waiting for", block.timeDelay, "ms")
        key = block.getFieldValue("key_option", lookIn=0)

        if key == "any":
            if keys:
                nb = block  # s.target.blocks[block.next]
                nb.blockRan = False
                while nb.next and nb.next != block.blockID:
                    nb.blockRan = False
                    nb.timeDelay = 0
                    nb.executionTime = 0
                    nb = s.target.blocks[nb.next]
                    block.script.add(nb.blockID)
                    if not nb.next:
                        nb.next = block.blockID
                    # TODO
                nb.blockRan = False
                nextBlock = s.target.blocks[block.next]
                block.blockRan = False
                return nextBlock
        elif KEY_MAPPING[key] in keys and block.next:
            print("DEBUG: Handling key", key)
            nb = block  # s.target.blocks[block.next]
            nb.blockRan = False
            while nb.next and nb.next != block.blockID:
                nb.blockRan = False
                nb.timeDelay = 0
                nb.executionTime = 0
                nb = s.target.blocks[nb.next]
                block.script.add(nb.blockID)
                if not nb.next:
                    nb.next = block.blockID
                # TODO: Check if inEventLoop is true and event is last in loop
            nb.blockRan = False
            nextBlock = s.target.blocks[block.next]
            return nextBlock

    if opcode == "control_forever":  # forever {..}
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
            while nb.next and nb.next != block.blockID:
                # TODO: Caution: Don't loop the program
                nb.blockRan = False
                nb.waiting = False
                nb.timeDelay = 0
                nb.executionTime = 0
                nb = s.target.blocks[nb.next]
                block.substack.add(nb.blockID)
            nb.next = block.blockID
            return nextBlock

    # If there is a block below, return it
    if block.next:
        nextBlock = s.target.blocks[block.next]
    # else:
    #     print("DEBUG: Script finished")
    block.blockRan = True
    return nextBlock
