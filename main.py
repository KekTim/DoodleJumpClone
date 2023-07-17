import pygame
import os
from random import randint, random
from time import sleep

screenWidth = 400
screenHeight = 700

# pygame setup
pygame.init()
pygame.display.set_caption("TopJump")
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
running = True

backgroundImage = pygame.image.load(os.path.join("images", "mikal.png"))
backgroundImage = pygame.transform.scale(backgroundImage, (screenWidth, screenHeight))

playerMaxJumpHight = screenHeight / 2
player = {
    "x": screenWidth/2,
    "y": screenHeight/2,
    "width": screenWidth,
    "height": 50
}
playerMaxSpeed = 6
playerSpeed = 0
playerMovementSpeed = 4
playerSprite = pygame.image.load(os.path.join("images", "player.png"))
playerSprite = pygame.transform.scale(playerSprite, (player["width"], player["height"]))

platforms = []
platformCount = 20
platformSpeed = 2
platformWidth = 50
platformHeight = 10
platformSprite = pygame.image.load(os.path.join("images", "platform.png"))
platformSprite = pygame.transform.scale(platformSprite, (platformWidth, platformHeight))
movingPlatformSprite = pygame.image.load(os.path.join("images", "platformBlau.png"))
movingPlatformSprite = pygame.transform.scale(movingPlatformSprite, (platformWidth, platformHeight))
breakingPlatformSprite = pygame.image.load(os.path.join("images", "platformBraun.png"))
breakingPlatformSprite = pygame.transform.scale(breakingPlatformSprite, (platformWidth, platformHeight))

jumpHeight = 250
remainingJumpingHeight = 0

def newPlatform(startSpawn=False ,platformProtectionHeight = 10):
    x = randint(0, screenWidth-platformWidth)
    y = 0
    
    if startSpawn:
        y = randint(0, screenHeight)
    else:
        y = randint(-100, 0)

    for platform in platforms:
        if y+platformHeight >= platform["y"]-platformProtectionHeight and y <= platform["y"]+platformHeight+platformProtectionHeight:
            x, y = newPlatform(startSpawn)
            break

    return x, y

for platform in range(platformCount):
    x, y = newPlatform(True)
    platforms.append({"x": x, "y": y, "type": 0}) #0 ist normal

score = 0
font = pygame.font.Font("freesansbold.ttf", 22)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player["x"] -= playerMovementSpeed
    if keys[pygame.K_RIGHT]:
        player["x"] += playerMovementSpeed

    if player["x"] < -player["width"] * 0.6: #60% = 0.6
        player["x"] = screenWidth-(player["width"]/2)
    if player["x"]+player["width"] > screenWidth + (player["width"] * 0.6): #60% = 0.6
        player["x"] = -player["width"]/2

    #move blue platforms
    for platform in platforms:
        if platform["type"] == 1:
            if platform["direction"] == "left":
                platform["x"] -= platformSpeed

                if platform["x"] <= 0:
                    platform["x"] = 0
                    platform["direction"] = "right"
            else:
                platform["x"] += platformSpeed

                if platform["x"]+platformWidth >= screenWidth:
                    platform["x"] = screenWidth-platformWidth
                    platform["direction"] = "left"

    #update sprites
    screen.blit(backgroundImage, (0, 0))
    screen.blit(font.render("Score: "+str(score), True, (0, 0, 0)), (20, 20))
    for platform in platforms:
        if platform["type"] == 0:
            screen.blit(platformSprite, (platform["x"], platform["y"]))

        elif platform["type"] == 1: 
            screen.blit(movingPlatformSprite, (platform["x"], platform["y"]))

        elif platform["type"] == 2:
            screen.blit(breakingPlatformSprite, (platform["x"], platform["y"]))

    screen.blit(playerSprite, (player["x"], player["y"]))
    pygame.display.update()

    #wenn er fällt
    if remainingJumpingHeight <= 0:

        if playerSpeed < playerMaxSpeed:
            playerSpeed += playerMaxSpeed * 0.05 #wieder beschleunigung

        if player["y"]+player["height"] > screenHeight:
            print("dead")
            break

        nextIsJump = False
        #ob er hittet
        for platform in platforms:
            if player["x"]+player["width"] >= platform["x"] and player["x"] <= platform["x"]+platformWidth:
                #wenn er beim nächsten hittet
                if player["y"]+player["height"] == platform["y"]:

                    if platform["type"] == 2: #bricht die platform
                        platform["type"] = 0
                        platform["x"], platform["y"] = newPlatform()
                    else:
                        remainingJumpingHeight = jumpHeight
                        playerSpeed = playerMaxSpeed
                        nextIsJump = True

                elif player["y"]+player["height"]+playerSpeed > platform["y"] and player["y"]+player["height"] < platform["y"]:
                    player["y"] = platform["y"]-player["height"]
                    nextIsJump = True
                
        if not nextIsJump:
            player["y"] += playerSpeed
    else:
        
        #works for now but there is better way
        #make him slow down smoothly
        if remainingJumpingHeight <= 10:
            playerSpeed = playerMaxSpeed * 0.2
        elif remainingJumpingHeight <= 30:
            playerSpeed = playerMaxSpeed * 0.4
        elif remainingJumpingHeight <= 60:
            playerSpeed = playerMaxSpeed * 0.6
        elif remainingJumpingHeight <= 80:
            playerSpeed = playerMaxSpeed * 0.8

        #doodle an die max jump höhe machen,
        if player["y"] > playerMaxJumpHight:
            player["y"] -= playerSpeed
            remainingJumpingHeight -= playerSpeed

        #welt hinter doodle verschieben
        else:
            for platform in platforms:
                platform["y"] += playerSpeed
                if platform["y"] > screenHeight:

                    abc = random()

                    if abc < 0.05:
                        platform["type"] = 1
                        platform["direction"] = "left"
                    elif abc < 0.1:
                        platform["type"] = 2

                    platform["x"], platform["y"] = newPlatform()

            remainingJumpingHeight -= playerSpeed
            score += int(playerSpeed)

    clock.tick(60) / 1000

pygame.quit()


