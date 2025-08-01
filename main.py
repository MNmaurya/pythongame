import math
import random

import pygame
from pygame import mixer

# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('forest.png')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Fruit Cutter")
icon = pygame.image.load('apple.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('bow.png')
playerX = 370
playerY = 480
playerX_change = 0

# Apples (Enemies)
appleImg = []
appleX = []
appleY = []
appleX_change = []
appleY_change = []
num_of_apples = 6

for i in range(num_of_apples):
    appleImg.append(pygame.image.load('apple.png'))
    appleX.append(random.randint(0, 736))
    appleY.append(random.randint(50, 150))
    appleX_change.append(4)
    appleY_change.append(40)

# Arrow (Bullet)
# Ready - You can't see the arrow on the screen
# Fire - The arrow is currently moving

arrowImg = pygame.image.load('arrow.png')
arrowX = 0
arrowY = 480
arrowX_change = 0
arrowY_change = 10
arrow_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def apple(x, y, i):
    screen.blit(appleImg[i], (x, y))


def fire_arrow(x, y):
    global arrow_state
    arrow_state = "fire"
    screen.blit(arrowImg, (x + 16, y + 10))


def isCollision(appleX, appleY, arrowX, arrowY):
    distance = math.sqrt(math.pow(appleX - arrowX, 2) + (math.pow(appleY - arrowY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    screen.fill((115, 215, 255))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if arrow_state == "ready":
                    arrowSound = mixer.Sound("laser.wav")
                    arrowSound.play()
                    arrowX = playerX
                    fire_arrow(arrowX, arrowY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Apple Movement
    for i in range(num_of_apples):

        # Game Over
        if appleY[i] > 440:
            for j in range(num_of_apples):
                appleY[j] = 2000
            game_over_text()
            break

        appleX[i] += appleX_change[i]
        if appleX[i] <= 0:
            appleX_change[i] = 4
            appleY[i] += appleY_change[i]
        elif appleX[i] >= 736:
            appleX_change[i] = -4
            appleY[i] += appleY_change[i]

        # Collision
        collision = isCollision(appleX[i], appleY[i], arrowX, arrowY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            arrowY = 480
            arrow_state = "ready"
            score_value += 1
            appleX[i] = random.randint(0, 736)
            appleY[i] = random.randint(50, 150)

        apple(appleX[i], appleY[i], i)

    # Arrow Movement
    if arrowY <= 0:
        arrowY = 480
        arrow_state = "ready"

    if arrow_state == "fire":
        fire_arrow(arrowX, arrowY)
        arrowY -= arrowY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
