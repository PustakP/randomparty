import pygame, sys
"""
main is the main game if you are testing "game" then put it here 
everything that would get inverted,to be drawn on screen
if something shouldn't be inverted then draw it directly on window
sys.exit() is neccessary shut the fuck up
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
backg = pygame.image.load("background.jpg")
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
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.animation_list = []
        self.left ,self.right,self.jump = False, False, False  #movement vars to be defined here from the class while all checks and change in pos will be done in "game"
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        for i in range(8):
            img = pygame.image.load(f'img/player/run/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
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

        # update rectangle postition
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100
        # update image depending on current frame
        self.image = self.animation_list[self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out of frames, then reset back to start
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class Game():
    def __init__(self):
        self.state = "menu"
        self.temp_iter_var = 0
        self.enter = [pygame.transform.rotate(pygame.transform.scale(pygame.image.load("img/enter.png"),(600,100)),x) for x in range(-20,22,2)]
        self.enter = self.enter + [pygame.transform.invert(x) for x in self.enter]

    def menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.state = 'main'
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
        global screen, invert_colors, k_key_held  # idk why but if not metion global it gives local var error
        screen.fill((255,255,255))
        player.update_animation()
        player.draw() # draws the platformer on screen
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
