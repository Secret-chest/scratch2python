"""
targetSprite

Targets as pygame sprites
"""

import pygame
import cairosvg
import io
import scratch
import config
import sys
import i18n

i18n.set("locale", config.language)
i18n.set("filename_format", "{locale}.{format}")
i18n.load_path.append("lang/")
_ = i18n.t


class TargetSprite(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)
        self.padX = 0
        self.padY = 0
        self.target = target
        self.target.currentCostume = target.currentCostume
        # Load costume
        if target.costumes[self.target.currentCostume].dataFormat != "svg":
            sprite = pygame.image.load(io.BytesIO(target.costumes[target.currentCostume].file))
            initialWidth = sprite.get_width()
            initialHeight = sprite.get_height()
            sprite = pygame.transform.smoothscale(sprite, (sprite.get_width() // target.costumes[target.currentCostume].bitmapResolution, sprite.get_height() // target.costumes[target.currentCostume].bitmapResolution))
            self.padX = initialWidth - sprite.get_width()
            self.padY = initialHeight - sprite.get_height()
        else:
            sprite = scratch.loadSvg(target.costumes[target.currentCostume].file)
        sprite = pygame.transform.rotate(sprite, 90 - target.direction)
        self.x = target.x + self.padX // 2
        self.y = target.y - self.padY // 2
        self.size = target.size
        self.image = sprite
        self.rect = self.image.get_rect()
        self.isStage = target.isStage
        if self.target.name == "Stage":
            self.name = _("stage")
        else:
            self.name = self.target.name

        # Convert Scratch coordinates into Pygame coordinates
        self.rect.x = (self.x + scratch.WIDTH // 2 - self.target.costumes[self.target.currentCostume].rotationCenterX)
        self.rect.y = (scratch.HEIGHT // 2 - self.y - self.target.costumes[self.target.currentCostume].rotationCenterY)
        pygame.transform.scale(self.image, (int(round(self.rect.width * self.size / 100)), int(round(self.rect.height * self.size / 100))))

        print(_("costumes-count", sprite=self.name, costumes=len(self.target.costumes)))

    # Set self position
    def setXy(self, x, y):
        if not self.isStage:
            # Do sprite fencing
            if not config.allowOffScreenSprites:
                if self.rect.width > 32:
                    if x > scratch.WIDTH - scratch.WIDTH / 2 + (self.rect.width / 2 - 16):
                        x = scratch.WIDTH - scratch.WIDTH / 2 + (self.rect.width / 2 - 16)
                    if x < scratch.WIDTH / 2 - scratch.WIDTH - (self.rect.width / 2 + 16):
                        x = scratch.WIDTH / 2 - scratch.WIDTH - (self.rect.width / 2 + 16)
                else:
                    if x > scratch.WIDTH - scratch.WIDTH / 2:
                        x = scratch.WIDTH - scratch.WIDTH / 2
                    if x < scratch.WIDTH / 2 - scratch.WIDTH:
                        x = scratch.WIDTH / 2 - scratch.WIDTH
                if self.rect.height > 32:
                    if y > scratch.HEIGHT - scratch.HEIGHT / 2 + (self.rect.height / 2 - 16):
                        y = scratch.HEIGHT - scratch.HEIGHT / 2 + (self.rect.height / 2 - 16)
                    if y < scratch.HEIGHT / 2 - scratch.HEIGHT - (self.rect.height / 2 + 16):
                        y = scratch.HEIGHT / 2 - scratch.HEIGHT - (self.rect.height / 2 + 16)
                else:
                    if y > scratch.HEIGHT - scratch.HEIGHT / 2:
                        y = scratch.HEIGHT - scratch.HEIGHT / 2
                    if y < scratch.HEIGHT / 2 - scratch.HEIGHT:
                        y = scratch.HEIGHT / 2 - scratch.HEIGHT
            # Set X and Y
            self.x = x + self.padX // 2
            self.y = y - self.padY // 2
            print(_("debug-prefix"), _("new-sprite-position", x=x, y=y, name=self.name), file=sys.stderr)
            self.rect.x = self.x + scratch.WIDTH // 2 - self.target.costumes[self.target.currentCostume].rotationCenterX
            self.rect.y = scratch.HEIGHT // 2 - self.y - self.target.costumes[self.target.currentCostume].rotationCenterY

    # Move
    def setXyDelta(self, dx, dy):
        if not self.isStage:
            x = self.x + dx
            y = self.y + dy
            # Do sprite fencing
            if not config.allowOffScreenSprites:
                if self.rect.width > 32:
                    if x > scratch.WIDTH - scratch.WIDTH / 2 + (self.rect.width / 2 - 16):
                        x = scratch.WIDTH - scratch.WIDTH / 2 + (self.rect.width / 2 - 16)
                    if x < -scratch.WIDTH / 2 - (self.rect.width / 2 - 16):
                        x = -scratch.WIDTH / 2 - (self.rect.width / 2 - 16)
                else:
                    if x > scratch.WIDTH - scratch.WIDTH / 2:
                        x = scratch.WIDTH - scratch.WIDTH / 2
                    if x < scratch.WIDTH / 2 - scratch.WIDTH:
                        x = scratch.WIDTH / 2 - scratch.WIDTH
                if self.rect.height > 32:
                    if y > scratch.HEIGHT - scratch.HEIGHT / 2 + (self.rect.height / 2 - 16):
                        y = scratch.HEIGHT - scratch.HEIGHT / 2 + (self.rect.height / 2 - 16)
                    if y < -scratch.HEIGHT / 2 - (self.rect.height / 2 - 16):
                        y = -scratch.HEIGHT / 2 - (self.rect.height / 2 - 16)
                else:
                    if y > scratch.HEIGHT - scratch.HEIGHT / 2:
                        y = scratch.HEIGHT - scratch.HEIGHT / 2
                    if y < scratch.HEIGHT / 2 - scratch.HEIGHT:
                        y = scratch.HEIGHT / 2 - scratch.HEIGHT
            # Set X and Y
            self.x = x + self.padX // 2
            self.y = y - self.padY // 2
            print(_("debug-prefix"), _("new-sprite-position", x=x, y=y, name=self.name), file=sys.stderr)
            self.rect.x = self.x + scratch.WIDTH // 2 - self.target.costumes[self.target.currentCostume].rotationCenterX
            self.rect.y = scratch.HEIGHT // 2 - self.y - self.target.costumes[self.target.currentCostume].rotationCenterY

    # Change costume
    def setCostume(self, costumeId):
        self.target.currentCostume = costumeId % len(self.target.costumes)
        # Load costume
        if self.target.costumes[self.target.currentCostume].dataFormat != "svg":
            sprite = pygame.image.load(io.BytesIO(self.target.costumes[self.target.currentCostume].file))
            initialWidth = sprite.get_width()
            initialHeight = sprite.get_height()
            sprite = pygame.transform.smoothscale(sprite, (sprite.get_width() // self.target.costumes[self.target.currentCostume].bitmapResolution, sprite.get_height() // self.target.costumes[self.target.currentCostume].bitmapResolution))
            self.padX = initialWidth - sprite.get_width()
            self.padY = initialHeight - sprite.get_height()
        else:
            sprite = scratch.loadSvg(self.target.costumes[self.target.currentCostume].file)
        self.image = sprite
        self.rect = self.image.get_rect()
        self.setXy(self.x, self.y)
