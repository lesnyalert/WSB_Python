import pygame #to make a game
from pygame import mixer #to play music in game
import math #to make a collision
import random #to randomize aliens

#Initialize the pygame library

pygame.init()

#screen - resolution

screen = pygame.display.set_mode((800, 600))

#game background
background = pygame.image.load('space_background.png')

#game background sounds
mixer.music.load('background_music.mp3')
mixer.music.play(-1)

#Icon and Title
pygame.display.set_caption("Alien Shooter")
icon = pygame.image.load('game_icon.png')
pygame.display.set_icon(icon)

#Player spaceship
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change=0

#Alien spaceship
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
alien_num = 6

for i in range (alien_num):
    alienImg.append(pygame.image.load('alien.png'))
    alienX.append(random.randint(0, 735))
    alienY.append(random.randint(50, 150))
    alienX_change.append(0.3)
    alienY_change.append(40)

#Missile
missileImg = pygame.image.load('missile.png')
missileX = 0
missileY = 480
missileX_change= 0
missileY_change = 7
missile_state = "ready" #ready - you can't see the missile on the screen, fire - bullet is moving

#Score
score_value = 0
font = pygame.font.Font('tahoma.ttf', 34)
textX=10
textY=10

#Gameover text
gameover_font = pygame.font.Font('tahoma.ttf', 64)

def show_score (x,y):
    score = font.render("Score :" + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def gameover_text():
    gameover_text = gameover_font.render("GAME OVER", True, (255, 255, 0))
    screen.blit(gameover_text, (200, 250))

def player(x,y):
    screen.blit(playerImg, (x, y))

def alien(x,y, i):
    screen.blit(alienImg[i], (x, y))

def fire_missile(x,y):
    global missile_state
    missile_state = "fire"
    screen.blit(missileImg, (x + 16, y + 10))  #to shoot missile from the middle of spaceship

def isCollision(alienX, alienY, missileX, missileY):
    distance = math.sqrt((math.pow(alienX-missileX,2) + (math.pow(alienY-missileY,2))))
    if distance < 27:
        return True
    else:
        return False

#Game Loop
running = True
while running:

    screen.fill((200, 100, 100))
    #background image
    screen.blit(background,(0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

         # spaceship moving to left/right with key arrows
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                missile_sound = mixer.Sound('laser.wav')
                missile_sound.play()
                if missile_state == "ready":
                    missileX = playerX
                    fire_missile(missileX, missileY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # when spaceship reach borders of window - do not go over it
    playerX += playerX_change
    if playerX <=0:
        playerX=0
    elif playerX >=736:
        playerX= 736

    #aliens movement
    for i in range (alien_num):

        #Game Over
        if alienY[i] > 440:
            for j in range (alien_num):  #to move aliens off the screen
                alienY[j] = 2000
            gameover_text()
            break

        alienX[i] += alienX_change[i]
        if alienX[i] <= 0:
            alienX_change[i] = 0.3
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -0.3
            alienY[i] += alienY_change[i]

            # collision between alien and bullet
        collision = isCollision(alienX[i], alienY[i], missileX, missileY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            missileY = 480
            missile_state = "ready"
            score_value += 1
            alienX[i] = random.randint(0, 735)
            alienY[i] = random.randint(50, 150)

        alien(alienX[i], alienY[i], i)

    #missile movement
    if missileY <= 0:
        missileY = 480
        missile_state = "ready"
    if missile_state == "fire":
        fire_missile(missileX, missileY)
        missileY -= missileY_change


    player(playerX,playerY)
    show_score(textX, textY)
    pygame.display.update()