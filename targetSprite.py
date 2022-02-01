"""
targetSprite

Targets as pygame sprites
"""

import pygame
import cairosvg
import io
import scratch


class TargetSprite(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)
        self.padX = 0
        self.padY = 0
        self.target = target
        # Load costume
        if target.costumes[target.currentCostume].dataFormat != "svg":
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
        self.image = sprite
        self.rect = self.image.get_rect()
        self.isStage = target.isStage

        # Convert Scratch coordinates into Pygame coordinates
        self.rect.x = (self.x + scratch.WIDTH // 2 - self.target.costumes[self.target.currentCostume].rotationCenterX)
        self.rect.y = (scratch.HEIGHT // 2 - self.y - self.target.costumes[self.target.currentCostume].rotationCenterY)

    # Set self position
    def setXy(self, x, y):
        # Do sprite fencing
        if x > 240:
            x = 240
        if x < -240:
            x = -240
        if y > 180:
            y = 180
        if x < -240:
            x = -240
        # Set X and Y
        self.x = x + self.padX // 2
        self.y = y - self.padY // 2
        self.rect.x = self.x + scratch.WIDTH // 2 - self.target.costumes[self.target.currentCostume].rotationCenterX
        self.rect.y = scratch.HEIGHT // 2 - self.y - self.target.costumes[self.target.currentCostume].rotationCenterY
