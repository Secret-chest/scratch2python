import copy

class BlockDef:
    def __init__(self, blockId, sprite, substack, shadow, inputs, fields):
        self.blockId = blockId
        self.sprite = sprite
        self.substack = substack
        self.shadow = shadow
        self.inputs = copy.deepcopy(inputs)
        self.fields = copy.deepcopy(fields)

    def getInputValue(self, inputId):
        # input[0]: 1 = unobscured shadow, 2 = no shadow, 3 = obscured shadow
        # input[1][0]:
        # * num: 4, 5, 6, 7, 8
        # * color: 9
        # * text: 10
        # * broadcast: 11
        # * variable: 12
        # * list: 13
        blockInput = self.inputs[inputId.upper()]
        if blockInput[0] == 1:
            # menu
            pass
        elif blockInput[0] == 3:
            # obsucred menu
            pass
        else:
            # normal input
            pass
