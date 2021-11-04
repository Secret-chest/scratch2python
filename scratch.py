"""
This file runs Scratch blocks, and stuff like that. Basically
it simulates Scratch using the Scratch2Python file, hence tha name.
"""
# Scratch project functions
# Green flag event
import pygame.time
import cairosvg
import io
HEIGHT = 360
WIDTH = 480


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
def execute(block, s):
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
        print(block.getFieldValue("to"))
        if block.getFieldValue("to") == "_mouse_":  # go to [mouse pointer v]
            newX, newY = pygame.mouse.get_pos()
            newX = newX - WIDTH // 2
            newY = HEIGHT // 2 - newY
            s.setXy(newX, newY)
            return s.target.blocks[s.target.blocks[block.parent].next]

    if opcode == "motion_setx":  # set x to ()
        s.setXy(int(block.getInputValue("x")), s.y)

    if opcode == "motion_changexby":  # change x by ()
        s.setXy(s.x + int(block.getInputValue("x")), s.y)

    if opcode == "motion_sety":  # set y to ()
        s.setXy(s.x, int(block.getInputValue("y")))

    if opcode == "motion_changeyby":  # change y by ()
        s.setXy(s.x, s.y + int(block.getInputValue("y")))

    if opcode == "control_wait":  # wait () seconds
        # If not already waiting
        if not block.waiting:
            # Get time delay and convert it to milliseconds
            block.timeDelay = int(round(float(int(block.getInputValue("duration"))) * 1000))
            block.waiting = True
            block.executionTime = 0
            print("DEBUG: Waiting for", block.timeDelay, "ms")
        return block

    if opcode == "event_whenflagclicked":  # when green flag clicked
        pass

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

    # If there is a block below, print some debug messages and return it
    if block.next:
        print("DEBUG: Next ID", block.next)
        nextBlock = s.target.blocks[block.next]
        print("DEBUG: Next opcode", nextBlock.opcode)
    else:
        print("DEBUG: Script finished")
    block.blockRan = True
    return nextBlock
