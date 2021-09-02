# Scratch project functions


def startProject():
    print("DEBUG: Project start event")


def execute(block):
    opcode = block.opcode
    id = block.blockID
    blockRan = block.blockRan
    inputs = block.inputs
    fields = block.fields
