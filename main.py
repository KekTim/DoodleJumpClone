from random import randint, random
from time import sleep
import pygame
import os

screenWidth = 400
screenHeight = 700

player = {
    "x": screenWidth/2,
    "y": 100,
    "width": 45,
    "height": 45
}
playerMaxSpeed = 15
playerMovementSpeed = 5
playerMaxJumpHight = screenHeight / 2
jumpHeight = 250

platformCount = 100
platformSpeed = 5
platformWidth = 60
platformHeight = 20
platformProtectionHeight = 20

score = 0

playerSpeed = 0 #verändern bringt nix man muss playerMaxSpeed verändern
remainingJumpingHeight = 0 #verändern bringt nix man muss jumpHeight verändern
platforms = [{"x": player["x"], "y": screenHeight-100, "type": 0}] 


#bilder laden und scalieren
backgroundImage = pygame.image.load(os.path.join("images", "background.jpg"))
backgroundImage = pygame.transform.scale(backgroundImage, (screenWidth, screenHeight))
playerSprite = pygame.image.load(os.path.join("images", "player.png"))
playerSprite = pygame.transform.scale(playerSprite, (player["width"], player["height"]))
platformSprite = pygame.image.load(os.path.join("images", "platform.png"))
platformSprite = pygame.transform.scale(platformSprite, (platformWidth, platformHeight))
movingPlatformSprite = pygame.image.load(os.path.join("images", "platformBlau.png"))
movingPlatformSprite = pygame.transform.scale(movingPlatformSprite, (platformWidth, platformHeight))
breakingPlatformSprite = pygame.image.load(os.path.join("images", "platformGelb.png"))
breakingPlatformSprite = pygame.transform.scale(breakingPlatformSprite, (platformWidth, platformHeight))

def newPlatform(startSpawn=False):

    
    x = 0
    if platformWidth < screenWidth:
        x = randint(0, screenWidth-platformWidth)
        
    y = 0

    if startSpawn:
        y = randint(0, screenHeight)
    else:
        y = randint(-100-platformHeight, 0)
    for platform in platforms:
        if y+platformHeight >= platform["y"]-platformProtectionHeight and y <= platform["y"]+platformHeight+platformProtectionHeight:
            return
        
    randomNum = random()
    if randomNum < 0.05:
        platforms.append({"x": x, "y": y, "type": 1, "direction": "left"})
    elif randomNum < 0.1:
        platforms.append({"x": x, "y": y, "type": 2})
    else:
        platforms.append({"x": x, "y": y, "type": 0})

#spawn the first platforms
for _ in range(platformCount):
    newPlatform(True)

# pygame setup
pygame.init()
pygame.display.set_caption("TopJump")
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
font = pygame.font.Font("freesansbold.ttf", 22)
running = True
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
    for platform in platforms:
        if platform["type"] == 0:
            screen.blit(platformSprite, (platform["x"], platform["y"]))

        elif platform["type"] == 1: 
            screen.blit(movingPlatformSprite, (platform["x"], platform["y"]))

        elif platform["type"] == 2:
            screen.blit(breakingPlatformSprite, (platform["x"], platform["y"]))

    screen.blit(playerSprite, (player["x"], player["y"]))
    screen.blit(font.render("Score: "+str(score), True, (0, 0, 0)), (20, 20))
    pygame.display.update()

    #wenn er fällt
    if remainingJumpingHeight <= 0:

        if playerSpeed < playerMaxSpeed:
            playerSpeed += playerMaxSpeed * 0.05 #wieder beschleunigung

        if player["y"]+player["height"] > screenHeight:
            
            textWidth, textHeight = font.size("Verloren!")
            screen.blit(font.render("Verloren!", True, (0, 0, 0)), (screenWidth/2-textWidth/2, screenHeight/2-textHeight/2))
            pygame.display.update()

            sleep(1)
            break

        nextIsJump = False
        for platform in platforms:
            if player["x"]+player["width"] >= platform["x"] and player["x"] <= platform["x"]+platformWidth:
                #wenn er hittet
                if player["y"]+player["height"] == platform["y"]:

                    if platform["type"] == 2: #bricht die platform
                        platforms.remove(platform)
                    else:
                        remainingJumpingHeight = jumpHeight
                        playerSpeed = playerMaxSpeed
                        nextIsJump = True

                #wenn er beim nächsten hittet
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
                    platforms.remove(platform)

            remainingJumpingHeight -= playerSpeed
            score += int(playerSpeed)

    #spawn new platforms
    if len(platforms) < platformCount:
        newPlatform()

    clock.tick(60) / 1000

pygame.quit()
