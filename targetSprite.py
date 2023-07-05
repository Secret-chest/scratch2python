"""
targetSprite

Targets as pygame sprites
"""
import time
import math
import pygame
import cairosvg
import io
import scratch
import config
import sys
import i18n
import copy
import random

i18n.set("locale", config.language)
i18n.set("filename_format", "{locale}.{format}")
i18n.load_path.append("lang/")
_ = i18n.t

sprites = set()

# Disable the print function
def decorator(func):
    def disabledPrint(*args, **kwargs):
        if not config.disablePrint:
            func(*args, **kwargs)
    return disabledPrint
print = decorator(print)

class TargetSprite(pygame.sprite.Sprite):
    def __init__(self, target):
        sprites.add(self)
        pygame.sprite.Sprite.__init__(self)
        self.target = target
        self.target.currentCostume = target.currentCostume
        # Load costume
        if target.costumes[self.target.currentCostume].dataFormat != "svg":
            self.isBitmap = True
            sprite = pygame.image.load(io.BytesIO(target.costumes[target.currentCostume].file))
            initialWidth = sprite.get_width()
            initialHeight = sprite.get_height()
            sprite = pygame.transform.smoothscale(sprite, (sprite.get_width() // target.costumes[target.currentCostume].bitmapResolution, sprite.get_height() // target.costumes[target.currentCostume].bitmapResolution))
        else:
            self.isBitmap = False
            sprite = scratch.loadSvg(target.costumes[target.currentCostume].file)
        self.x = target.x
        self.y = target.y
        self.direction = target.direction
        self.size = target.size
        self.sprite = sprite
        self.image = self.sprite.copy()
        self.rect = self.image.get_rect()
        self.spriteRect = self.sprite.get_rect()
        self.isStage = target.isStage
        self.rotationStyle = target.rotationStyle
        self.imageSize = sprite.get_size()
        self.flipped = False
        self.layerOrder = target.layerOrder
        if self.target.name == "Stage":
            self.name = _("stage")
        else:
            self.name = self.target.name

        self.setXy(self.x, self.y)
        self.setRot(self.direction)
        self.setSize(self.size)
        print(self.rect.size)

    # Set self position
    def setXy(self, x, y):
        # Do sprite fencing
        if not config.allowOffScreenSprites:
            if self.rect.width <= 32:
                if x > scratch.WIDTH / 2:
                    x = scratch.WIDTH / 2
                elif x < scratch.WIDTH / -2:
                    x = scratch.WIDTH / -2
            else:
                if x > scratch.WIDTH / 2 + self.rect.width / 2 - 16:
                    x = scratch.WIDTH / 2 + self.rect.width / 2 - 16
                elif x < scratch.WIDTH / -2 - self.rect.width / 2 + 16:
                    x = scratch.WIDTH / -2 - self.rect.width / 2 + 16

            if self.rect.height <= 32:
                if y > scratch.HEIGHT / 2:
                    y = scratch.HEIGHT / 2
                elif y < scratch.HEIGHT / -2:
                    y = scratch.HEIGHT / -2
            else:
                if y > scratch.HEIGHT / 2 + self.rect.height / 2 - 16:
                    y = scratch.HEIGHT / 2 + self.rect.height / 2 - 16
                elif y < scratch.HEIGHT / -2 - self.rect.height / 2 + 16:
                    y = scratch.HEIGHT / -2 - self.rect.height / 2 + 16

        self.x = x
        self.y = y
        # print(_("debug-prefix"), _("new-sprite-position", x=x, y=y, name=self.name), file=sys.stderr)
        #rect = self.sprite.get_rect(topleft=(self.x - self.target.costumes[self.target.currentCostume].rotationCenterX, self.y - self.target.costumes[self.target.currentCostume].rotationCenterY))
        if not self.isStage:
            self.image = pygame.transform.smoothscale(self.sprite, (self.size / 100 * self.imageSize[0], self.size / 100 * self.imageSize[1]))
        else:
            self.image = self.sprite
        offset = self.target.costumes[self.target.currentCostume].offset.elementwise() * self.size / 100 - pygame.math.Vector2(self.sprite.get_width() / 2, self.sprite.get_height() / 2).elementwise() * self.size / 100
        # TODO fix rotation centre precision
        if self.rotationStyle == "all around":
            self.image = pygame.transform.rotate(self.image, 90 - self.direction)
            offset.rotate_ip(90 + self.direction)
        elif self.rotationStyle == "left-right":
            angle = self.direction % 360
            print(angle, self.flipped)
            if angle > 180:
                self.flipped = True
            else:
                self.flipped = False
            if self.flipped:
                self.image = pygame.transform.flip(self.image, True, False)
                offset = self.target.costumes[self.target.currentCostume].offset.elementwise() * self.size / 100 - pygame.math.Vector2(self.sprite.get_width() / 2, self.sprite.get_height() / 2).elementwise() * self.size / 100
            else:
                offset = pygame.math.Vector2(-self.target.costumes[self.target.currentCostume].offset.x, self.target.costumes[self.target.currentCostume].offset.y).elementwise() * self.size / 100 - pygame.math.Vector2(-self.sprite.get_width() / 2, self.sprite.get_height() / 2).elementwise() * self.size / 100
        else:
            self.image = self.image

        relativePosition = pygame.math.Vector2(self.spriteRect.centerx, self.spriteRect.centery)
        position = pygame.math.Vector2(self.x - self.sprite.get_width() / 2 + scratch.WIDTH / 2, self.y - self.sprite.get_height() / 2 + scratch.HEIGHT / 2)

        self.rect = self.image.get_rect(center=position+relativePosition+offset)

    # Relatively set self position
    def setXyDelta(self, dx, dy):
        x = self.x + dx
        y = self.y + dy
        self.setXy(x, y)

    # Set self rotation
    def setRot(self, rot):
        self.direction = rot
        print(_("debug-prefix"), _("new-sprite-rotation", rot=rot, name=self.name), file=sys.stderr)

        self.setXy(self.x, self.y)

    # Relatively set self rotation (turn)
    def setRotDelta(self, drot):
        rot = self.direction + drot
        self.setRot(rot)

    # Set self rotation
    def setSize(self, size):
        self.size = size
        print(_("debug-prefix"), _("new-sprite-size", size=size, name=self.name), file=sys.stderr)

        self.setXy(self.x, self.y)

    # Relatively set self rotation (turn)
    def setSizeDelta(self, dsize):
        size = self.size + dsize
        self.setSize(size)

    # Change costume
    def setCostume(self, costumeId):
        self.target.currentCostume = costumeId % len(self.target.costumes)

        # Load costume
        if self.target.costumes[self.target.currentCostume].dataFormat != "svg":
            sprite = pygame.image.load(io.BytesIO(self.target.costumes[self.target.currentCostume].file))
            initialWidth = sprite.get_width()
            initialHeight = sprite.get_height()
            sprite = pygame.transform.smoothscale(sprite, (sprite.get_width() // self.target.costumes[self.target.currentCostume].bitmapResolution, sprite.get_height() // self.target.costumes[self.target.currentCostume].bitmapResolution))
        else:
            sprite = scratch.loadSvg(self.target.costumes[self.target.currentCostume].file)
        self.image = sprite
        self.imageSize = sprite.get_size()
        self.rect = self.image.get_rect()
        self.setXy(self.x, self.y)
