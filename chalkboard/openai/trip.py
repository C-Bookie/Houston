import pygame
import math
import random

pygame.init()

width = 800
height = 600
screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()

running = True

# Define variables for trippy effect
freq_x = 0.01
freq_y = 0.01
amplitude = 100
noise_scale = 0.1

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill((0, 0, 0))

    # Loop through each pixel on the screen
    for x in range(width):
        for y in range(height):
            # Calculate color based on position, time, and noise
            color_r = (math.sin(x * freq_x) + math.sin(y * freq_y)) * amplitude
            color_g = (math.sin(x * freq_x + math.pi / 2) + math.sin(y * freq_y + math.pi / 2)) * amplitude
            color_b = (math.sin(x * freq_x + math.pi) + math.sin(y * freq_y + math.pi)) * amplitude

            # Add some random noise to the color values
            color_r += random.uniform(-noise_scale, noise_scale) * amplitude
            color_g += random.uniform(-noise_scale, noise_scale) * amplitude
            color_b += random.uniform(-noise_scale, noise_scale) * amplitude

            # Add some variation to the color values based on their position
            color_r *= math.sin(x / width * math.pi)
            color_g *= math.sin(y / height * math.pi)
            color_b *= math.sin((x + y) / (width + height) * math.pi)

            # Clamp the color values between 0 and 255
            color_r = max(0, min(255, int(color_r)))
            color_g = max(0, min(255, int(color_g)))
            color_b = max(0, min(255, int(color_b)))

            color = (color_r, color_g, color_b)

            # Set pixel color
            screen.set_at((x, y), color)

    # Update display
    pygame.display.flip()

    # Limit framerate
    clock.tick(60)

pygame.quit()
