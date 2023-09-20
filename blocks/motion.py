from blockDef import *


class GoToXY(BlockDef):
    friendlyName = "go to x {input:x} y {input:y}"

    def runSelf(self):
        self.sprite.setXy(self.getInputValue("x"), self.getInputValue("y"))


opcodes = {
    "motion_gotoxy": GoToXY,
}
