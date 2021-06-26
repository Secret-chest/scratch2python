class Monitor:
    def __init__(self):
        self.id = ""  # variable ID
        self.mode = "default"  # default, large or slide
        self.opcode = "data_variable"  # value type
        self.params = {}
        self.spriteName = None  # for local variables, shown as Sprite1: my variable
        self.value = 0
        self.x = 0
        self.y = 0
        self.visible = True
        self.sliderMin = 0
        self.sliderMax = 100
