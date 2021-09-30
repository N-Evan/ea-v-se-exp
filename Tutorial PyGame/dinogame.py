#first game with python pygame library.
#tutorial from realpython.com/pygame-a-primer/
#@author Md. Nurusshafi Evan

#we start by importing pygame library
import pygame
import random
from pygame.constants import K_ESCAPE

#We will import pygame.locals to make key coordinate access easier.

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

#Now to initialize the game
pygame.init()

#We define player objects to define player and incoming objects using Sprite library
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        #loads sprite image defined in path
        self.surf = pygame.image.load("Tutorial PyGame\img\playerIdle.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # self.surf = pygame.Surface((75,25))
        # self.surf.fill((0, 150, 40))
        self.rect = self.surf.get_rect()
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -15)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 15)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-15, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(15, 0)

        #Conditions / logics to stop from going off screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.top <= 0:
            self.rect.top = 0

#now we create enemies using sprite library
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("Tutorial PyGame\img\enemy.png").convert()
        self.surf.set_colorkey((255, 255, 255))
        # self.surf = pygame.Surface((20, 10))
        # self.surf.fill((120, 60, 35))
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5, 20)

    #Moves based on random speed received from line 63
    #kill sprite upon reaching left edge
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

#creating cloud class to render onto background
class Cloud(pygame.sprite.Sprite):
    def __init__(self): 
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("Tutorial PyGame\img\cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), random.randint(0, SCREEN_HEIGHT)
            )
        )

        #constant speed for cloud woosh
    def update(self):
        self.rect.move_ip(-15, 0)
        if self.rect.right < 0:
            self.kill()

#lets define screen area, constants
SCREEN_WIDTH = 1660
SCREEN_HEIGHT = 900

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#creating custom event to spawn enemies at set interval
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY,250)

#creating custom event for cloud spawn and setting interval
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

#initializing a player object from the player class we created before - line 25
player = Player()

#creating sprite group to hold all sprites
# - enemies used for collision detect and pos updates
# - all_sprites used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player) #adds player to sprite group

#now setup game loop. 
# 1. Will process user input
# 2. update state of all objs
# 3. Updates display and audio
# 4. Maintains speed.

#creating clock to control speed of the game. 
clock = pygame.time.Clock()

running = True #boolean var to keep game loop running

#main loop translate into while(running == True): do following
while running: 
    #if there's an event in pygame. event refers to keypress
    for event in pygame.event.get():
        if event.type == KEYDOWN: #only execute for a keypress event
            if event.key == K_ESCAPE:
                running = False #set game loop to false if esc pressed.
        elif event.type == QUIT:
            running = False #QUIT type event referes to pressing close button
    
        #adding enemies
        elif event.type == ADDENEMY:
            #creates enemies and adds to sprite group defined previously
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    #receive a dictionary of presed keys
    pressed_keys = pygame.key.get_pressed()

    #player sprite executes update function (here to move)
    player.update(pressed_keys)
    #updates enemy positions
    enemies.update()
    clouds.update()


    #filling the screen with black. Again.
    screen.fill((147, 202, 237)) 
    #creates a surface of 50,50 length-width
    surf = pygame.Surface((50, 50)) 
    #coloring the surface with 233,233,233 color
    surf.fill((233, 233, 233))
    rect = surf.get_rect() #storing as rect for later use.

    #fucntion to find surf center
    surf_center = ((SCREEN_WIDTH-surf.get_width())/2, (SCREEN_HEIGHT-surf.get_height())/2)

    # #Surfaces by themselves aren't visible.
    # #So we use blit (block transfer) to copy contents of one surface to another.
    # screen.blit(player.surf, player.rect) #copy surface to given coords
    # #player.rect currently holds coordinates of top left corner
    # #we use this later to move the player

    #drawing all sprites instead of using single blits
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    #sprite.collideany checks for sprite overlaps aka collisions
    #checks if player collided with any object from enemies
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    pygame.display.flip()

    #ticks to ensure program maintains 30fps
    clock.tick(30)

    #however blit thinks top left corner as anchor so not exactly centered unless we use maths.
    #line 56 to find surface center.




