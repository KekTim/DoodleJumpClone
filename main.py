import pygame
import os
from random import randint
from time import sleep

screenWidth = 400
screenHeight = 700

# pygame setup
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
running = True
deltaTime = 0

backgroundImage = pygame.image.load(os.path.join("images", "background.jpg"))
backgroundImage = pygame.transform.scale(backgroundImage, (screenWidth, screenHeight))


playerMaxJumpHight = screenHeight / 2
player = {
    "x": screenWidth/2,
    "y": screenHeight/2,
    "width": 50,
    "height": 50
}
playerSprite = pygame.image.load(os.path.join("images", "player.png"))
playerSprite = pygame.transform.scale(playerSprite, (player["width"], player["height"]))

platforms = [{"x": screenWidth/2, "y": screenHeight-100}, {"x": screenWidth/2, "y": screenHeight-600}]
platformCount = 10
platformWidth = 50
platformHeight = 10
platformSprite = pygame.image.load(os.path.join("images", "platform.png"))
platformSprite = pygame.transform.scale(platformSprite, (platformWidth, platformHeight))

for platform in range(platformCount):
    platforms.append({"x": randint(0, screenWidth-platformWidth), "y": randint(0, screenHeight-platformHeight)})

jumpHeight = 310
remainingJumpingHeight = 0
playerSpeed = 1

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #update sprites
    screen.blit(backgroundImage, (0, 0))
    screen.blit(playerSprite, (player["x"], player["y"]))
    for platform in platforms:
        screen.blit(platformSprite, (platform["x"], platform["y"]))
    pygame.display.update()


    #wenn er fällt
    if remainingJumpingHeight <= 0:

        if player["y"]+player["height"] > screenHeight:
            print("dead")
            break


        nextIsJump = False
        #ob er hittet
        for platform in platforms:
            if player["x"]+player["width"] >= platform["x"] and player["x"] <= platform["x"]+platformWidth:
                #wenn er beim nächsten hittet
                if player["y"]+player["height"] == platform["y"]:
                    print("jump")
                    remainingJumpingHeight = jumpHeight
                    nextIsJump = True
                
                elif player["y"]+player["height"]+playerSpeed > platform["y"] and player["y"]+player["height"] < platform["y"]:
                    print(player["y"]+player["height"]+playerSpeed)
                    print(platform["y"])
                    player["y"] = platform["y"]
                    nextIsJump = True
                    sleep(10)
                
        if not nextIsJump:
            player["y"] += playerSpeed
    else:
        
        #doodle an die max jump höhe machen,
        if player["y"] > playerMaxJumpHight:
            print("doodle höher")
            player["y"] -= playerSpeed #noch komplexer eig weil er sonst an verschiedenen stellen sein kann, noch checken ob - jumpSpeed 3 rest lässt oder so
            remainingJumpingHeight -= playerSpeed

        #welt hinter doodle verschieben
        else:
            print("welt nach unten")
            for platform in platforms:
                platform["y"] += playerSpeed
            print(remainingJumpingHeight)
            remainingJumpingHeight -= playerSpeed


    """
    if remainingJumpingHeight <= 0:
        
        #nach unten fallen lassen
        player["y"] += fallingSpeed #eig noch delta time

        #check if dead
        if (player["y"]+player["height"] > screenHeight):
            print("dead")
            break

        #ob er platform hittet
        for platform in platforms:
            #ob die rechte ecke vom spieler an die linke der platfrom geht, ob die linke vom spieler an die rechte von platfrom ist, ob die beine vom spieler die platfrom berührern
            if player["x"]+player["width"] >= platform["x"] and player["x"] <= platform["x"]+platformWidth and player["y"]+player["height"] == platform["y"]:
                print("jump")
                remainingJumpingHeight = jumpHeight
    else:
        
        #doodle an die max jump höhe machen,
        if player["y"] > playerMaxJumpHight:
            print("doodle höher")
            player["y"] -= jumpSpeed #noch komplexer eig weil er sonst an verschiedenen stellen sein kann, noch checken ob - jumpSpeed 3 rest lässt oder so
            remainingJumpingHeight -= jumpSpeed

        #welt hinter doodle verschieben
        else:
            print("welt nach unten")
            for platform in platforms:
                platform["y"] += jumpSpeed
                remainingJumpingHeight -= jumpSpeed
                print(remainingJumpingHeight)
    """


    


    # print(player)
    # for platform in platforms:
    #     print(platform)
    deltaTime = clock.tick(60) / 1000


pygame.quit()
    