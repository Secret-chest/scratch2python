import pygame
import cairosvg
import io
import scratch


class TargetSprite(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)
        self.target = target
        # load and upscale
        sprite = scratch.loadSvg(target.costumes[target.currentCostume].file)
        sprite = pygame.transform.rotate(sprite, 90 - target.direction)
        self.image = sprite
        self.rect = self.image.get_rect()
        # convert Scratch coordinates into Pygame coordinates
        self.rect.x = target.x + scratch.WIDTH // 2 - self.rect.width // 2
        self.rect.y = scratch.HEIGHT // 2 - target.y - self.rect.height // 2

    def setXy(self, x, y):
        self.rect.x = x + scratch.WIDTH // 2 - self.rect.width // 2
        self.rect.y = scratch.HEIGHT // 2 - y - self.rect.height // 2
