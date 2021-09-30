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
    # set direction
    sprite = pygame.transform.rotate(sprite, 90 - direction)
    # convert Scratch coordinates into Pygame coordinates
    finalX = x + WIDTH // 2 - sprite.get_width() // 2
    finalY = HEIGHT // 2 - y - sprite.get_height() // 2
    display.blit(sprite, (finalX, finalY))


# Set the stage background
def setBackground(bg, display):
    render(bg, 0, 0, 90, display)


def startProject():
    print("DEBUG: Project start event")


# Run the given block object
def execute(block, s):
    opcode = block.opcode
    id = block.blockID
    blockRan = block.blockRan
    inputs = block.inputs
    fields = block.fields
    nextBlock = None
    if opcode == "motion_gotoxy":
        s.setXy(int(inputs["X"][1][1]), int(inputs["Y"][1][1]))
    if opcode == "control_wait":
        if not block.waiting:
            block.timeDelay = int(round(float(inputs["DURATION"][1][1]) * 1000))
            block.waiting = True
            block.executionTime = 0
            print("DEBUG: Waiting for", block.timeDelay, "ms")
        return block
    if opcode == "event_whenflagclicked":
        pass
    if block.next:
        print("DEBUG: Next ID", block.next)
        nextBlock = s.target.blocks[block.next]
        print("DEBUG: Next opcode", nextBlock.opcode)
    else:
        print("DEBUG: Script finished")
    block.blockRan = True
    return nextBlock
