import pygame
import math
import random

# initialising pygame
pygame.init()

# creating screen
width = 480
height = 480
win = pygame.display.set_mode((width, height))


# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)


def show_score(x, y):
    scoreshow = font.render("Score : " + str(score), True, (255, 255, 255))
    win.blit(scoreshow, (x, y))


WIDTH = 18
food = pygame.image.load('bait.png')

over_font = pygame.font.Font('freesansbold.ttf', 64)


class snake(object):
    def __init__(self, x, y, width, length=1, vel=20):
        self.vel = vel
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.eat = False
        self.xchange = 0
        self.ychange = 0
        self.posx = [(self.x // 20 * 20 + 1)]
        self.posy = [(self.y // 20 * 20 + 1)]
        self.movecount = 0

    def move(self, keys):
        if keys[pygame.K_UP]:
            self.ychange = -self.vel
            self.xchange = 0
        elif keys[pygame.K_DOWN]:
            self.ychange = self.vel
            self.xchange = 0
        elif keys[pygame.K_RIGHT]:
            self.xchange = self.vel
            self.ychange = 0
        elif keys[pygame.K_LEFT]:
            self.xchange = -self.vel
            self.ychange = 0

        if self.movecount >= 20:
            self.movecount += 1
        else:
            self.movecount = 0

        self.y += self.ychange
        self.x += self.xchange

        self.posx[0] = self.x // 20 * 20 + 1
        self.posy[0] = self.y // 20 * 20 + 1

        a1 = self.posx[0]
        b1 = self.posy[0]
        a2 = self.posx[0]
        b2 = self.posy[0]

        for i in range(1, self.length):
            a2 = self.posx[i]
            b2 = self.posy[i]
            self.posx[i] = a1
            self.posy[i] = b1
            a1 = a2
            b1 = b2

    def drawsnake(self):
        unit = pygame.image.load('units.png')

        for i in range(0, self.length):
            win.blit(unit, (self.posx[i], self.posy[i]))


baitx = (random.randint(0, (width//20 - 1))) * 20 + 1
baity = (random.randint(0, (width//20 - 1))) * 20 + 1


def drawbait():
    win.blit(food, (baitx, baity))


def drawgrid():
    w = 18
    m = 1
    for i in range(0, 800, 20):
        for j in range(0, 600, 20):
            pygame.draw.line(win, (255, 255, 255), (0, i-1), (width, i-1), 2)
            pygame.draw.line(win, (255, 255, 255), (i-1, 0), (i-1, height), 2)


def eat(player):
    global baity
    global baitx
    global score
    if player.posx[0] == baitx and player.posy[0] == baity:
        player.posx.append(player.posx[player.length - 2])
        player.posy.append(player.posy[player.length - 2])
        player.length += 1
        baitx = (random.randint(0, (width // 20 - 1))) * 20 + 1
        baity = (random.randint(0, (width // 20 - 1))) * 20 + 1
        score += 1


def gameover(player):
    flag = 0
    for i in range(4, player.length):
        if player.posx[0] == player.posx[i] and player.posy[0] == player.posx[i]:
            flag = 1
            break

    if flag == 1:
        return True
    else:
        return False

def game_over_text():
    win.fill((0, 0, 0))
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    win.blit(over_text, (50, 200))


# MAIN LOOP
player = snake(400, 300, WIDTH)
running = True
a = False
clock = pygame.time.Clock()
while running:

    pygame.time.delay(60)
    win.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.move(keys)

    if player.x >= width:
        player.x = 0
    elif player.x <= 0:
        player.x = width

    if player.y >= height:
        player.y = 0
    elif player.y <= 0:
        player.y = height

    eat(player)

    if gameover(player) or player.length == 0:
        game_over_text()
        player.length = 0

    drawbait()
    player.drawsnake()
    show_score(10, 10)

    pygame.display.update()
