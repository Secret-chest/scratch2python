import pygame
import cairosvg
import io
import scratch


class TargetSprite(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)
        self.target = target
        # Load and upscale
        sprite = scratch.loadSvg(target.costumes[target.currentCostume].file)
        sprite = pygame.transform.rotate(sprite, 90 - target.direction)
        self.image = sprite
        self.rect = self.image.get_rect()
        # Convert Scratch coordinates into Pygame coordinates
        self.x = target.x
        self.y = target.y
        self.rect.x = target.x + scratch.WIDTH // 2 - self.target.costumes[self.target.currentCostume].rotationCenterX
        self.rect.y = scratch.HEIGHT // 2 - target.y - self.target.costumes[self.target.currentCostume].rotationCenterY

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
        self.x = x
        self.y = y
        self.rect.x = x + scratch.WIDTH // 2 - self.target.costumes[self.target.currentCostume].rotationCenterX
        self.rect.y = scratch.HEIGHT // 2 - y - self.target.costumes[self.target.currentCostume].rotationCenterY
