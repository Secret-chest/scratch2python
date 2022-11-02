import time
import pygame

pygame.init()
pygame.key.set_repeat(2000, 1000 // 30)

pygame.display.set_mode((240, 180))

lastTime = time.time_ns()

if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                print(event.key, "+" + str((time.time_ns() - lastTime) // 1000000))
                lastTime = time.time_ns()
