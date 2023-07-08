import pygame

# Initialize Pygame
pygame.init()

# Define the dimensions of the window
width = 900
height = 800

# Create the Pygame window
window = pygame.display.set_mode((width, height))

# Initialize color inversion flag
invert_colors = False

# Create a group to hold all sprites
all_sprites = pygame.sprite.Group()

# Create your sprites and add them to the group
# Example:
# sprite = YourSpriteClass()
# all_sprites.add(sprite)

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:  # Check if "K" key is pressed
                invert_colors = not invert_colors  # Toggle color inversion flag

    # Update game logic

    # Clear the window
    window.fill((255, 255, 255))  # Fill with white color (RGB: 255, 255, 255)

    # Create a new surface for rendering
    inverted_surface = pygame.Surface((width, height))

    # Copy the original window surface onto the inverted surface
    inverted_surface.blit(window, (0, 0))

    # Invert colors if the flag is True
    if invert_colors:
        inverted_surface = pygame.transform.invert(inverted_surface)

    # Draw all sprites onto the inverted surface
    all_sprites.draw(inverted_surface)

    # Draw the inverted surface onto the window
    window.blit(inverted_surface, (0, 0))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
