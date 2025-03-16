from typing import Any
import pygame
import random
from random import randint

WIDTH = 800
HEIGHT = 500
SIZE = (WIDTH, HEIGHT)
FPS = 60

win = pygame.display.set_mode((800,500))
clock = pygame.time.Clock()
background = pygame.transform.scale(
                pygame.image.load("galaxy.jpg"),
                SIZE
                )
pygame.display.set_caption("Шутер")
pygame.mixer.init()
pygame.mixer.music.load("space.ogg")
pygame.mixer.music.play()



class GameSprite(pygame.sprite.Sprite):
    def __init__(self, filename:str, size:tuple[int,int], coords: tuple[int,int], speed:int):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(filename), size)
        self.rect = self.image.get_rect(center=coords)
        self.speed = speed
    def reset(self, window:pygame.Surface):
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.y > 0:
            self.rect.y -= self.speed
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.y < HEIGHT-self.rect.height:
            self.rect.y += self.speed
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.x < WIDTH-self.rect.width:
            self.rect.x += self.speed
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        pass

class Enemy(GameSprite):
    def update(self):   
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(self.rect.width, WIDTH-self.rect.width)
        

player = Player("rocket.png", (50,70), (HEIGHT-75,WIDTH//2),10)
test_enemy = Enemy("ufo.png", (70,50), (random.randint(70,WIDTH-70), 0), 8)

game = True
finish = False
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    if not finish:
        win.blit(background, (0,0))
        player.reset(win)
        player.update()
        test_enemy.reset(win)
        test_enemy.update()



    pygame.display.update()
    clock.tick(60)