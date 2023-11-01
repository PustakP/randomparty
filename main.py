import pygame, sys, os
"""
main is the main game if you are testing "game" then put it here 
everything that would get inverted,to be drawn on screen
if something shouldn't be inverted then draw it directly on window
sys.exit() is neccessary shut the fuck up NO YOU DONTTTTT SHUT UP THE FUCK UPIDEUWIOEUOWEIFWE
put comments to explain function methods or stuff not variables, for variables just name it properly
"""
pygame.init()
width = 900
height = 800
toggleControl = 1 # 0 means toggle and 1 means hold
screen = pygame.Surface((width,height)) # screen in which everything will be drawn
window = pygame.display.set_mode((width, height)) # pygame window, screen will be drawn on this
pygame.display.set_caption('EXACTLY')
clock = pygame.time.Clock()
FPS = 60
backg = pygame.image.load("img/bg/background.jpg")

# define game variables
GRAVITY = 0.75

# define player action variables
invert_colors = False
k_key_held = False
time1 = 0 # global time var for keeping track of time

# Create a group to hold all sprites
all_sprites = pygame.sprite.Group()

# Set initial position of the red rectangle
red_rect_position = pygame.mouse.get_pos()

# Create a red rectangle sprite
red_rect = pygame.Rect(red_rect_position[0],red_rect_position[1],50,50)
temp_iter_var = 0
run = True

class Player(pygame.sprite.Sprite):    # why would you name the player class as platformer rohan
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.left ,self.right,self.jump = False, False, False  #movement vars to be defined here from the class while all checks and change in pos will be done in "game"
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

    def move(self):
        # reset movement variables
        dx = 0
        dy = 0
        # assign movement variables if moving left or right
        if self.left:
            dx = -self.speed   #omg rohan differentiation OwO
            self.flip = True
            self.direction = -1
        if self.right:
            dx = self.speed   #omg rohan differentiation phirse? OwO
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
        window.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)   # player will not get inverted if player should change window to screen here

class Game():
    def __init__(self):
        self.state = "menu"
        self.temp_iter_var = 0
        self.left ,self.right = False, False
        self.enter = [pygame.transform.rotate(pygame.transform.scale(pygame.image.load("img/enter.png"),(600,100)),x) for x in range(-20,22,2)]
        self.enter = self.enter + [pygame.transform.invert(x) for x in self.enter]

    def menu(self):
        global run
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.state = 'main'
                if event.key == pygame.K_ESCAPE:
                    run = False
        if int(self.temp_iter_var) >= 0 and int(self.temp_iter_var) < 20:
            self.temp_iter_var += 0.2
        elif self.temp_iter_var > 20 and self.temp_iter_var < 20.5:
            self.temp_iter_var = 41
        elif self.temp_iter_var <= 41 and int(self.temp_iter_var) > 21:
            self.temp_iter_var -= 0.2 
        elif self.temp_iter_var > 21.5 and self.temp_iter_var < 22:
            self.temp_iter_var = 0
        
        mask = pygame.mask.from_surface(self.enter[int(self.temp_iter_var)]) 
        mask.invert()
        mask = mask.to_surface() 
        mask.set_colorkey((255,255,255))
        posx = 450-self.enter[int(self.temp_iter_var)].get_width()//2
        posy = 400-self.enter[int(self.temp_iter_var)].get_height()//2
        screen.blit(mask,(posx+3,posy))
        screen.blit(mask,(posx,posy-3))
        screen.blit(mask,(posx-3,posy))
        screen.blit(mask,(posx,posy+3))
        screen.blit(self.enter[int(self.temp_iter_var)],(posx,posy))

    def main(self):  # put stuff here
        global screen, invert_colors, k_key_held, run  # idk why but if not metion global it gives local var error
        screen.blit(backg,(0,0)) # for now normal background ke saath play play and test test 
        player.update_animation()
        player.draw() # draws the platformer on screen
        pygame.draw.line(screen, (255, 0, 0), (0, 600), (width, 600)) # draws a line for floor (temparary)
        player.move()
    
        # update player actions
        if player.alive:
            if player.in_air:
                player.update_action(2)  # 2: jumping
            elif self.left or self.right:
                player.update_action(1) # 1 means run
            else:
                player.update_action(0) # 0 means idle
            player.move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.left = True
                if event.key == pygame.K_d:
                    player.right = True
                if event.key == pygame.K_SPACE and player.alive:
                    player.jump = True
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_k:  # if "K"is pressed and togglecontrol is True
                    invert_colors = True  # Enable color inversion
                    k_key_held = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.left = False
                if event.key == pygame.K_d:
                    player.right = False
                if event.key == pygame.K_k and toggleControl:
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
    
        # Update the position of the red rectangle
        red_rect.x = red_rect_position[0]
        red_rect.y = red_rect_position[1]

#    def gameov(self):

    def stateselector(self):
        if self.state == "menu":
            self.menu()
        if self.state == "gameover":
            self.gameov()
        if self.state == "main":
            self.main()
    
player = Player(200, 200, 2, 7) # x postion, y postition, scale, speed
game = Game()

while run:
    pygame.display.update()
    window.blit(screen,(0,0))
    time1  = pygame.time.get_ticks()
    game.stateselector()
    clock.tick(FPS)
    