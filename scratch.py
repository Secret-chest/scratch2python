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
    # Get block properties
    opcode = block.opcode
    id = block.blockID
    blockRan = block.blockRan
    inputs = block.inputs
    fields = block.fields
    nextBlock = None
    if opcode == "motion_gotoxy":
        s.setXy(int(inputs["X"][1][1]), int(inputs["Y"][1][1]))
    if opcode == "motion_setx":
        s.setXy(int(inputs["X"][1][1]), s.y)
    if opcode == "motion_changexby":
        s.setXy(s.x + int(inputs["DX"][1][1]), s.y)
    if opcode == "motion_sety":
        s.setXy(s.x, int(inputs["Y"][1][1]))
    if opcode == "motion_changeyby":
        s.setXy(s.x, s.y + int(inputs["DY"][1][1]))
    if opcode == "control_wait":
        if not block.waiting:
            block.timeDelay = int(round(float(inputs["DURATION"][1][1]) * 1000))
            block.waiting = True
            block.executionTime = 0
            print("DEBUG: Waiting for", block.timeDelay, "ms")
        return block
    if opcode == "event_whenflagclicked":
        pass
    if opcode == "control_forever":
        block.blockRan = False
        if inputs["SUBSTACK"][1]:
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
    if block.next:
        print("DEBUG: Next ID", block.next)
        nextBlock = s.target.blocks[block.next]
        print("DEBUG: Next opcode", nextBlock.opcode)
    else:
        print("DEBUG: Script finished")
    block.blockRan = True
    return nextBlock
