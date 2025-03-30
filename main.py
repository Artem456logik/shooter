from typing import Any
import pygame
import random
from random import randint

WIDTH = 800
HEIGHT = 500
SIZE = (WIDTH, HEIGHT)
FPS = 60
lost = 0 
score = 0
lives = 3
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

bullets = pygame.sprite.Group()
fire_sound = pygame.mixer.Sound("fire.ogg")


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
        new_bullet = Bullet("bullet.png", (15,20), (self.rect.centerx, self.rect.top), 11)
        bullets.add(new_bullet)
        fire_sound.play()

class Enemy(GameSprite):
    def update(self):   
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(self.rect.width, WIDTH-self.rect.width)
            global lost
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()
            
pygame.font.init()
medium_font = pygame.font.SysFont("Helvetica", 24)

lost_text = medium_font.render("Пропущено" + str(lost), True, (255,255,255))
score_text = medium_font.render("Збито" + str(score), True, (255,255,255))

player = Player("rocket.png", (50,70), (HEIGHT-75,WIDTH//2),10)

enemis = pygame.sprite.Group()
enemis_num = 3

for i in range(enemis_num):
    n = random.randint(1,100)
    if n > 50:
        new_enemy = Enemy("ufo.png", (70,50), (random.randint(50, WIDTH-50), 0), random.randint(1,3))
    else:
        new_enemy = Enemy("asteroid.png", (70,50), (random.randint(50, WIDTH-50), 0), random.randint(1,3))
    enemis.add(new_enemy)


game = True
finish = False
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fire()
    if not finish:
        win.blit(background, (0,0))
        player.reset(win)
        player.update()
        lost_text = medium_font.render("Пропущено" + str(lost), True, (255,255,255))
        win.blit(lost_text, (25,25))
        score_text = medium_font.render("Збито" + str(score), True, (255,255,255))
        win.blit(score_text, (25,50))
        bullets.draw(win)
        bullets.update()
        enemis.draw(win)
        enemis.update()
        lives_text = medium_font.render("Життя" + str(lives), True, (255,255,0))
        win.blit(lives_text, (WIDTH-100,0))

        collided = pygame.sprite.groupcollide(enemis, bullets, True, True)
        for dead_enemy in collided:
            score += 1
            n = random.randint(1,100)
            if n > 50:
                new_enemy = Enemy("ufo.png", (70,50), (random.randint(50, WIDTH-50), 0), random.randint(1,3))
            else:
                new_enemy = Enemy("asteroid.png", (70,50), (random.randint(50, WIDTH-50), 0), random.randint(1,3))
            enemis.add(new_enemy)
        if score >= 51:
            finish = True
            font1 = pygame.font.Font(None, 48)
            text = font1.render("YOU WON", True, (0,255,0))
            win.blit(text, (WIDTH//2 - 100,HEIGHT//2)) 
        if lost >= 11:
            finish = True
            font1 = pygame.font.Font(None, 48)
            text = font1.render("YOU LOSE", True, (255,0,0))
            win.blit(text, (WIDTH//2 - 100,HEIGHT//2)) 

        collided = pygame.sprite.spritecollide(player, enemis, True)
        for enemy in collided:
            lives -= 1 
            n = random.randint(1,100)
            if n > 50:
                new_enemy = Enemy("ufo.png", (70,50), (random.randint(50, WIDTH-50), 0), random.randint(1,3))
            else:
                new_enemy = Enemy("asteroid.png", (70,50), (random.randint(50, WIDTH-50), 0), random.randint(1,3))
            enemis.add(new_enemy)
        if lives == 0:
            finish = True
            font1 = pygame.font.Font(None, 48)
            text = font1.render("YOU LOSE", True, (255,0,0))
            win.blit(text, (WIDTH//2 - 100,HEIGHT//2))
    pygame.display.update()
    clock.tick(60)