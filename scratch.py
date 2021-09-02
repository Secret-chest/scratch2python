# Scratch project functions


# Green flag event
def startProject():
    print("DEBUG: Project start event")


# Run the given block object
def execute(block):
    opcode = block.opcode
    id = block.blockID
    blockRan = block.blockRan
    inputs = block.inputs
    fields = block.fields
