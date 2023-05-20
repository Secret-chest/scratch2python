import pygame

pygame.init()

# Set up the window
screen = pygame.display.set_mode((640, 480))

# Load the sprite image
sprite_image = pygame.image.load("sprite.png")

# Define the rotation center offset relative to the sprite's origin
rotation_center_offset = (20, 10)

# Define the initial angle of the sprite
angle = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Calculate the rotation center position relative to the sprite's origin
    rotation_center = (
        rotation_center_offset[0],
        rotation_center_offset[1]
    )

    # Rotate the sprite image around the rotation center
    rotated_image = pygame.transform.rotate(sprite_image, angle)

    # Get the rect of the rotated image
    rect = rotated_image.get_rect()

    # Calculate the position of the sprite based on the rotation center and rect dimensions
    position = (
        rotation_center[0] - rect.width / 2,
        rotation_center[1] - rect.height / 2
    )

    # Draw the rotated image to the screen at the calculated position
    screen.blit(rotated_image, position)

    # Increment the angle
    angle += 0.125

    # Update the screen
    pygame.display.update()
