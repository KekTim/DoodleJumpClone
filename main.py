import pygame
import os
from random import randint
from time import sleep

screenWidth = 400
screenHeight = 700

fallingSpeed = 3

playerMaxJumpHight = screenHeight / 2
player = {
    "x": screenWidth/2,
    "y": screenHeight/2,
    "width": 50,
    "height": 50
}

platforms = []
platformCount = 10
platformWidth = 50
platformHeight = 10

for platform in range(platformCount):
    platforms.append({"x": randint(0, screenWidth-platformWidth), "y": randint(0, screenHeight-platformHeight)})

jumpHeight = 30
jumpSpeed = 5 #immer gleich außer wenn es eine feder oder so hittet
remainingJumpingHeight = 0

while True:


    if remainingJumpingHeight == 0:
        
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


    print(player)
    for platform in platforms:
        print(platform)
    sleep(5)




# pygame setup
# pygame.init()
# screen = pygame.display.set_mode((400, 700))
# clock = pygame.time.Clock()
# running = True
# deltaTime = 0

# backgroundImage = pygame.image.load(os.path.join("Python\DoodleJump", "background.jpg"))
# backgroundImage = pygame.transform.scale(backgroundImage, (400, 700))

# screen.blit(backgroundImage, (0, 0))
# pygame.display.update()



# while running:
#     # poll for events
#     # pygame.QUIT event means the user clicked X to close your window
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False




    
#     # limits FPS to 60
#     # delta time in seconds since last frame, used for framerate-
#     # independent physics.
#     deltaTime = clock.tick(60) / 1000
    

# pygame.quit()