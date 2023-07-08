import pygame

toggleControl = 1 # 0 means toggle and 1 means hold

# Initialize Pygame
pygame.init()

# Define the dimensions of the window
width = 900
height = 800

# Create the Pygame window
window = pygame.display.set_mode((width, height))

# Initialize color inversion flags
invert_colors = False
k_key_held = False

# Create a group to hold all sprites
all_sprites = pygame.sprite.Group()

# Create a red rectangle sprite
red_rect = pygame.sprite.Sprite()
red_rect.image = pygame.Surface((50, 50))
red_rect.image.fill((255, 0, 0))  # Fill with red color (RGB: 255, 0, 0)
red_rect.rect = red_rect.image.get_rect()

# Set initial position of the red rectangle
red_rect_position = pygame.mouse.get_pos()
red_rect.rect.center = red_rect_position

# Add the red rectangle sprite to the group
all_sprites.add(red_rect)

# Main game loop
running = True
while running:
    if toggleControl == 0:
    # Handle events if toggle
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:  # Check if "K" key is pressed
                    invert_colors = not invert_colors  # Toggle color inversion flag
    elif toggleControl == 1:
        # Handle events if hold
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:  # Check if "K" key is pressed
                    invert_colors = True  # Enable color inversion
                    k_key_held = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_k:  # Check if "K" key is released
                    invert_colors = False  # Disable color inversion
                    k_key_held = False

    # Update game logic

    # Clear the window
    window.fill((255, 255, 255))  # Fill with white color (RGB: 255, 255, 255)

    # Create a new surface for rendering
    inverted_surface = pygame.Surface((width, height))

    # Copy the original window surface onto the inverted surface
    inverted_surface.blit(window, (0, 0))

    # Invert colors if the flag is True and "K" key is held
    if invert_colors and k_key_held:
        inverted_surface = pygame.transform.invert(inverted_surface)
        red_rect_position = pygame.mouse.get_pos()  # Update the position of the red rectangle
    else:
        red_rect_position = red_rect.rect.center  # Store the current position of the red rectangle

    # Draw all sprites onto the inverted surface
    all_sprites.draw(inverted_surface)

    # Draw the inverted surface onto the window
    window.blit(inverted_surface, (0, 0))

    # Update the position of the red rectangle
    red_rect.rect.center = red_rect_position

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
