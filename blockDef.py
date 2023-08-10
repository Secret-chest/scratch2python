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
        # * float: 4
        # * positive float: 5
        # * positive int: 6
        # * int: 7
        # * boolean: 8 (unconfirmed)
        # * color: 9
        # * text: 10
        # * broadcast: 11
        # * variable: 12
        # * list: 13
        # input[1][1]: the value
        # input[1][2]: default value
        blockInput = self.inputs[inputId.upper()]
        if blockInput[0] == 1:
            # menu
            pass
        elif blockInput[0] == 3:
            # obscured menu
            pass
        else:
            # normal input

            pass
