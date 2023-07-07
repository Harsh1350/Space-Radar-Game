# This is a sample Python script.
import pygame
import random
import math
from pygame import mixer

pygame.init(),
screen = pygame.display.set_mode((800, 600))  # creating the screen
# background image
backgroundImg = pygame.image.load('spcae.png')
#background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("space Invador")
# adding player(spaceship)
playerImg = pygame.image.load('flying.png')
playerX = 370
playerY = 480
playerX_change = 0

# adding background enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemy = 6
for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# adding background bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"  # ready state mean u cant see the bullet on the screen
# fire state mean bulllet is currently moving

# score
score_value = 0
font = pygame.font.Font('Vintage Faith.ttf', 32)

textX = 10
textY = 10


#game over
over_font = pygame.font.Font('Vintage Faith.ttf', 64)



def show_score(x, y):
    score = font.render("score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_score = over_font.render("FINAL SCORE:" + str(score_value), True, (255, 255, 255))
    screen.blit(over_score, (200, 250))
def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y))


# function for collision
def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 15:
        return True
    else:
        return False


# game loop
running = True
while running:  # closing the screen at same time

    # RGB-red,green ,blue
    screen.fill((0, 0, 0))
    # background image
    screen.blit(backgroundImg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # movement of spaceship
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # checking for boundries of spaceship
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 764:
        playerX = 764
    # enemy movement
    for i in range(num_of_enemy):

        #game over
        if enemyY[i]>480:
            for j in range(num_of_enemy):
               enemyY[j]=2000

            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
 #       enemyY[i] += enemyY_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 764:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # code for collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if (bulletY <= 0):
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

