import copy


def parseValue(value, type_):
    def getBase(value):
        if "0x" in value or "0X" in value:
            return 16
        if "0o" in value or "0o" in value:
            return 8
        if "0b" in value or "0b" in value:
            return 2
        return 10

    if type_ in {6, 7}:
        try:
            return int(round(value, getBase(value)))
        except ValueError:
            if value == "Infinity":
                return float("inf")
            if value == "-Infinity":
                return float("-inf")
            if value == "NaN":
                return float("nan")
            if "e" in str(value) or "E" in str(value):
                return int(round(float(value)))
            if str(value) == "true":
                return 1
            return 0

    if type_ in {4, 5}:
        try:
            return float(value)
        except ValueError:
            if value == "Infinity":
                return float("inf")
            if value == "-Infinity":
                return float("-inf")
            if "e" in str(value) or "E" in str(value):
                return int(float(value))
            if str(value) == "true":
                return 1
            return 0

    if type_ == 10:
        return str(value)

    if type_ == 8:
        if value == "true":
            return True
        if value == 0:
            return False
        try:
            return bool(float(value))
        except ValueError:
            return False

    if type_ == 9:
        return "#" + hex(int(round(value))).strip("0x")


def _getInputValue(inputObject):
    # input[0]: 1 = unobscured shadow, 2 = no shadow, 3 = obscured shadow
    # input[1][0]:
    # * float: 4
    # * positive float: 5
    # * positive int: 6
    # * int: 7
    # * boolean: 8
    # * color: 9
    # * text: 10
    # * broadcast: 11
    # * variable: 12
    # * list: 13
    # input[1][1]: the value
    # input[1][2]: default value

    if inputObject[0] == 1:
        # menu
        pass
    elif inputObject[0] == 3:
        # obscured menu
        pass
    else:
        # no menu
        if not isinstance(inputObject[1][1], list):
            return inputObject[1][1]
        return _getInputValue(inputObject[1][1])


class BlockDef:
    friendlyName = ""

    def __init__(self, blockId, sprite, substack, shadow, inputs, fields):
        self.blockId = blockId
        self.sprite = sprite
        self.substack = substack
        self.shadow = shadow
        self.inputs = copy.deepcopy(inputs)
        self.fields = copy.deepcopy(fields)

    def runSelf(self):
        raise RuntimeError("Please run a specific block type, not the block template class!")

    def getInputValue(self, inputId):
        blockInput = self.inputs[inputId.upper()]
        return _getInputValue(blockInput)
