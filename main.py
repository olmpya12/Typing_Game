from typing import Counter, Text
import pygame
from pygame.locals import *
import sys
import random
import requests
import os

pygame.init()
FramePerSec = pygame.time.Clock()
vec = pygame.math.Vector2

HEIGHT = 450
WIDTH = 700
ACC = 0.5
FRIC = -0.12
FPS = 60
LEVEL = 2  # ne kadar duşuk o kadar zor
WORD_LEVEL = 1


max_score = 0


displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("typing game")
font = pygame.font.SysFont('Verdana', 50)


words_level_1 = []
words_level_2 = words_level_1.copy()
words_level_3 = words_level_2.copy()





class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("DINO.png")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = pygame.Rect(80, 360, 150, 60)

        self.pos = vec((80, 360))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def move(self):
        self.acc = vec(0, 0.5)

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def jump(self):
        self.vel.y = -10

    def update(self, hits):

        self.vel.y = 0
        self.pos.y = hits[0].rect.top + 1


class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(center=(WIDTH/2, HEIGHT - 10))

    def move(self):
        pass


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()

        self.image = pygame.image.load("KAKTUS.png")
        self.image = pygame.transform.scale(self.image, (40, 40))

        self.rect = self.image.get_rect(x=x, y=400)

        self.pos = vec(self.rect.x, self.rect.y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def move(self):

        self.acc = vec(-0.8, 0)

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc

        self.rect.x += self.vel.x + 0.5 * self.acc.x
        self.rect.y += self.vel.y + 0.5 * self.acc.y


def get_word():
    if os.path.isfile("./words.txt"):
        with open('words.txt', 'r') as f:
            target_list = words_level_1
            i = f.readline()
            while i:
                i = f.readline()

                if i == "--\n":
                    target_list = words_level_2
                    continue
                if i == "---\n":
                    target_list = words_level_3
                    continue
                if i == -1:
                    break
                target_list.append(i[:-1])

    else:
        #internetten kelime indirme
        ''' word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

        response = requests.get(word_site)
        WORDS = response.content.splitlines()

        for i in WORDS:
            a = i.decode("utf-8")
            if len(a) < 4 and len(a) >= 3:
                words_level_1.append(a)
            elif len(a) < 5 and len(a) >= 4:
                words_level_2.append(a)
            elif len(a) < 7 and len(a) > 5:
                words_level_3.append(a)

        with open('words.txt', 'x') as f:
            for i in words_level_1:
                f.write(i)
                f.write("\n")
            f.write("--\n")
            for i in words_level_2:
                f.write(i)
                f.write("\n")
            f.write("---\n")
            for i in words_level_3:
                f.write(i)
                f.write("\n") '''
        print("Kelime Dosyası bulunamadı...")
        pygame.quit()
        sys.exit()
        


def main_loop():
    LIFE = 4

    PT1 = platform()
    P1 = Player()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(PT1)
    all_sprites.add(P1)

    enemy_sprites = pygame.sprite.Group()

    platforms = pygame.sprite.Group()
    platforms.add(PT1)

    counter = 0
    hit_key = 32

    entery = ""
    entery_name = ""

    score = 0

    while 1:
        displaysurface.fill((255, 255, 255))
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if not event.key == 8:
                    last_key = str(event.key)
                    entery += last_key
                    entery_name += chr(event.key)
                else:
                    if not entery == "":
                        try:
                            last_key = entery_name[len(entery_name)-1:]

                            if last_key == "a" or last_key == "b" or last_key == "c":
                                entery = entery[:-2]
                            else:
                                entery = entery[:-3]
                            entery_name = entery_name[:-1]
                        except:
                            pass

        

        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if P1.vel.y > 0:
            if hits:
                P1.update(hits)
        
        if counter % (LEVEL*60) == 0:
            entery = ""

            if score < 10:
                random_key = random.choice(words_level_1)
            elif score < 20:
                random_key = random.choice(words_level_2)
            else:
                random_key = random.choice(words_level_3)

            enemy_sprites.add(Obstacle(700))
            hit_key = ""
            entery = ""
            entery_name = ""
            
            
            for a in random_key:
                i = ord(a)
                hit_key += str(i)



        for entity in all_sprites:
            try:
                displaysurface.blit(entity.image, entity.rect)
            except:
                displaysurface.blit(entity.surf, entity.rect)
            entity.move()
        for enemy in enemy_sprites:
            if enemy.rect.x <= 0:
                enemy.kill()
                entery_name = ""
                continue
            displaysurface.blit(enemy.image, enemy.rect)
            enemy.move()

        key_display = font.render(random_key, False, (0, 0, 0))
        if random_key == entery_name:
            key_display_2 = font.render(entery_name, False, (0, 255, 0))
        else:
            key_display_2 = font.render(entery_name, False, (255, 0, 0))

        score_text = font.render(f"Score: {score}", False, (0, 0, 0))
        life_counter_text = font.render(f"Life: {LIFE}", False, (0, 0, 0))

        displaysurface.blit(key_display, (WIDTH/2, 40))
        displaysurface.blit(key_display_2, (WIDTH/2, 80))
        displaysurface.blit(score_text, (30, 10))
        displaysurface.blit(life_counter_text, (30, 50))

        hits = pygame.sprite.spritecollide(P1, enemy_sprites, False)
        if hits:
            if LIFE <= 0:

                return score
            elif hits and counter % 20 == 0:
                if entery == hit_key:
                    hits = pygame.sprite.spritecollide(P1, platforms, False)
                    if hits:
                        P1.jump()
                        score += 1
                else:
                    LIFE -= 1
        counter += 1
        pygame.display.update()
        FramePerSec.tick(FPS)


def Gui():
    image_dino = pygame.image.load("DINO.png")
    image_dino = pygame.transform.scale(image_dino, (200, 200))
    small_font = pygame.font.SysFont('Corbel', 35)
    
    play_text = small_font.render('PLAY', True, (255, 255, 255))
    max_score_text = small_font.render(f'Max_score: {max_score}', True, (0, 0, 0))
    
    while 1:
        displaysurface.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:

                if WIDTH/2-70 <= mouse[0] <= WIDTH/2+70 and HEIGHT/2+100 <= mouse[1] <= HEIGHT/2+140:
                    return

        mouse = pygame.mouse.get_pos()

        

        if WIDTH/2-70 <= mouse[0] <= WIDTH/2+70 and HEIGHT/2+100 <= mouse[1] <= HEIGHT/2+140:
            pygame.draw.rect(displaysurface, (170, 170, 170), [
                             WIDTH/2-70, HEIGHT/2+100, 140, 40])

        else:
            pygame.draw.rect(displaysurface, (100, 100, 100), [
                             WIDTH/2-70, HEIGHT/2+100, 140, 40])

        displaysurface.blit(image_dino, (WIDTH/2-100, 100))
        displaysurface.blit(play_text, (WIDTH/2-26, HEIGHT/2+110))
        displaysurface.blit(max_score_text, (30, 10))

        pygame.display.update()
        FramePerSec.tick(FPS)


if __name__ == "__main__":

    get_word()
    if os.path.isfile("./save.txt"):
        with open("save.txt", "r") as f:
            try:
                max_score = int(f.readline())
            except:
                pass

    while True:
        Gui()
        last_score = main_loop()
        if last_score > max_score:
            max_score = last_score
        with open("save.txt", "w") as f:
            f.write(str(max_score))
