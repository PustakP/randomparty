import pygame, os

pygame.init()
width = 900
height = 800
toggleControl = 1 # 0 means toggle and 1 means hold
screen = pygame.Surface((width,height)) # screen in which everything will be drawn
window = pygame.display.set_mode((width, height)) # pygame window, screen will be drawn on this
pygame.display.set_caption('EXACTLY')
clock = pygame.time.Clock()
FPS = 60

# define game variables
GRAVITY = 0.75

# define player action variables
moving_left = False
moving_right = False
invert_colors = False
k_key_held = False

# define colors
BG = (255, 255, 255)
RED = (255, 0, 0)

# Create a group to hold all sprites
all_sprites = pygame.sprite.Group()

# Set initial position of the red rectangle
red_rect_position = pygame.mouse.get_pos()

# Create a red rectangle sprite
red_rect = pygame.Rect(red_rect_position[0],red_rect_position[1],50,50)


class Platformer(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # load all images for the players
        animation_types = ['idle', 'run', 'jump']
        for animation in animation_types:
            # reset temp list of images
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir(f'img/player/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/player/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        # reset movement variables
        dx = 0
        dy = 0
        # assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = -1

        # jump
        if self.jump and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # check collision with floor
        if self.rect.bottom + dy > 600:
            dy = 600 - self.rect.bottom
            self.in_air = False


        # update rectangle postition
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out of frames, then reset back to start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

player = Platformer(200, 200, 1.9, 7) # x postion, y postition, scale, speed

run = True
while run:
    clock.tick(FPS)
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 600), (width, 600)) # draws a line for floor (temparary)
    player.update_animation()
    player.draw() # draws the platformer on screen

    # update player actions
    if player.alive:
        if player.in_air:
            player.update_action(2)  # 2: jumping
        elif moving_left or moving_right:
            player.update_action(1) # 1 means run
        else:
            player.update_action(0) # 0 means idle
        player.move(moving_left, moving_right)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_k and toggleControl:  # if "K"is pressed and togglecontrol is True
                invert_colors = True  # Enable color inversion
                k_key_held = True
            elif event.key == pygame.K_k and not toggleControl: # if "K"is pressed and togglecontrol is NOT True
                invert_colors = not invert_colors  # Toggle color inversion flag
        
        # key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
        if event.type == pygame.KEYUP and toggleControl:
            if event.key == pygame.K_k:
                invert_colors = False  # Disable color inversion
                k_key_held = False

    # Invert colors if the flag is True and "K" key is held
    if invert_colors and k_key_held:
        screen = pygame.transform.invert(screen)
        red_rect_position = pygame.mouse.get_pos()  # Update the position of the red rectangle
    else:
        red_rect_position = [red_rect.x,red_rect.y]  # Store the current position of the red rectangle

    # Draw all sprites onto the inverted surface
    pygame.draw.rect(screen,(255,0,0),red_rect)

    # Draw the inverted surface onto the window
    window.blit(screen, (0, 0))

    # Update the position of the red rectangle
    red_rect.x = red_rect_position[0]
    red_rect.y = red_rect_position[1]

    # Update the display
    pygame.display.update()

pygame.quit()