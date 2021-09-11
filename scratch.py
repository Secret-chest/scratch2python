# Scratch project functions


# Green flag event
import pygame.time


def startProject():
    print("DEBUG: Project start event")


# Run the given block object
def execute(block, target):
    opcode = block.opcode
    id = block.blockID
    blockRan = block.blockRan
    inputs = block.inputs
    fields = block.fields
    if opcode == "motion_gotoxy":
        target.x = int(inputs["X"][1][1])
        target.y = int(inputs["Y"][1][1])
