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

i18n.set("locale", config.language)
i18n.set("filename_format", "{locale}.{format}")
i18n.load_path.append("lang/")
_ = i18n.t

sprites = set()


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
        self.imageSize = sprite.get_size()
        if self.target.name == "Stage":
            self.name = _("stage")
        else:
            self.name = self.target.name

        self.setXy(self.x, self.y)
        self.setRot(self.direction)

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
        # Set X and Y
        self.x = x
        self.y = y
        print("aici")
        # print(_("debug-prefix"), _("new-sprite-position", x=x, y=y, name=self.name), file=sys.stderr)
        #rect = self.sprite.get_rect(topleft=(self.x - self.target.costumes[self.target.currentCostume].rotationCenterX, self.y - self.target.costumes[self.target.currentCostume].rotationCenterY))
        offset = pygame.Vector2(self.target.costumes[self.target.currentCostume].rotationCenterX - self.sprite.get_rect().width / 2, self.target.costumes[self.target.currentCostume].rotationCenterY - self.sprite.get_rect().height / 2)
        offset.rotate_ip(90 + self.direction)
        self.image = pygame.transform.rotozoom(self.sprite, 90 - self.direction, 1)
        # offset = pygame.Vector2(0, 0)
        self.rect.centerx = scratch.WIDTH // 2 + self.x + offset.x
        self.rect.centery = scratch.HEIGHT // 2 - self.y + offset.y
        print(self.rect.x, self.rect.y, "/", self.x, self.y, "/", offset.x, offset.y)
        # TODO update current rotation centre to correct sprite position

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
