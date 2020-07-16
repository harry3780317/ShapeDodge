from turtle import *
from freegames import line
import pygame
import random
import math

gravity = 0.4
width = 1200
height = 250
FPS = 60

class ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("Aqua-Ball-icon.png")
        self.image = pygame.transform.scale(image, (30,30))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (width/5, height)
        self.vy = 0
    def update(self):
        keys = pygame.key.get_pressed() #get the key pressed
        if self.rect.bottomleft == (width/5, height):
            if keys[pygame.K_UP]:       #y speed set to 15
                self.vy = 15
                self.rect.y -= self.vy  #start to move the position of the ball

        if self.rect.bottomleft != (width/5,height):
            self.vy -= 1        #add in gravity effects i.e. speed reduction per frame at 60 fps
            self.rect.y -= self.vy #actually moving the ball object

        if self.rect.bottomleft >= (width/5, height): #detect if ball moves below bottom screen
            self.rect.bottomleft = (width/5, height) #set it back to zero until next up-key press

class obstacles(pygame.sprite.Sprite): #inherit the sprite class

    def __init__(self,ball):
        pygame.sprite.Sprite.__init__(self) #initialize all the necessary values of sprite class
        self.image = pygame.Surface((30,30))    #add in square obstacles
        self.image.fill((100,100,0)) #fill it with yellow color
        self.rect = self.image.get_rect()   #get the boundaries of the obstacles. use later for collision detection
        self.rect.bottomleft = (random.randint(width,width*1.5), height) #spawning randomly off the screen and scroll towards ball
        self.vx = -math.ceil((ball.rect.width + self.rect.width)/15)    #set the speed for the obstacle


    def update(self):
        self.rect.x += self.vx



#initialized pygame
class ball_game:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font(None, 30)
        self.screen = pygame.display.set_mode([width, height])
        pygame.display.set_caption("ball game")
        self.clock = pygame.time.Clock()
        self.running = True

    def new(self):
        self.main_sprite = pygame.sprite.Group()
        self.mob_sprites = pygame.sprite.Group()
        self.ball = ball()
        self.main_sprite.add(self.ball)
        self.new_obstacle = obstacles(self.ball)
        self.mob_sprites.add(self.new_obstacle)


        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.font
            self.fps = self.font.render(str(int(self.clock.get_fps())), True, pygame.Color('white'))

            self.events()
            self.update()
            self.draw()

    def draw(self):
        self.screen.fill((0,0,0))
        self.main_sprite.draw(self.screen)
        self.mob_sprites.draw(self.screen)
        self.screen.blit(self.fps, (0, 0))
        pygame.display.flip()

    def update(self):
        self.main_sprite.update()
        for sprite in self.mob_sprites.sprites():
            if sprite.rect.bottomright < (0, height):
                self.mob_sprites.remove(sprite)
                del sprite #if a sprite moves off screen then the idea is to delete it and spawn new ones
                #print(sprite.vx) #use for debugging - should generate error here
                break

        if self.new_obstacle.rect.bottomright < (width- self.ball.rect.width , height):
            self.new_obstacle = obstacles(self.ball)
            self.mob_sprites.add(self.new_obstacle)
        self.mob_sprites.update()

        collision = pygame.sprite.spritecollide(self.ball, self.mob_sprites, False)
        if collision:
            self.playing = False
            self.running = False

    def events(self):
        for keypress in pygame.event.get():
            if keypress.type == pygame.QUIT:
                self.playing = False
            self.running = False

    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass

game  = ball_game()
while game.running:
    game.new()

print('you lost for good!')
pygame.quit()
