import pygame, time, random, os
from distutils.command.config import config
from distutils.dist import DistributionMetadata
from sys import displayhook
from tokenize import _all_string_prefixes
from assets.character import Person
from assets.levelList import Level
from assets.levelDictionary import currentMap
from assets.levelDictionary import levelWidth
from assets.levelDictionary import levelHeight
from assets.levelDictionary import validCoords
from assets.levelDictionary import startCoords
from assets.levelDictionary import levelBoundsFill
from assets.menus import PauseScreen
from assets.menus import MenuArrow

try:
    from saveData.fullscreenconfig import windowed_config
except ImportError:
    f = open("saveData/fullscreenconfig.py", "w")
    f.write("windowed_config = True")
    f.close()
    from saveData.fullscreenconfig import windowed_config


#engine initialize
pygame.init
pygame.font.init()

#declare colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (70, 70, 70)


windowed = windowed_config

#change the program icon
programIcon = pygame.image.load("assets/playerCharacter.png")

#Open game window and setup window stuff
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{100},{100}"
pygame.display.set_icon(programIcon)
pygame.display.set_caption("RPG Engine (indev)")
size = [640,480]
if windowed:
    selectedScreenSetup = pygame.display.set_mode(size, vsync=1)
else:
    selectedScreenSetup = pygame.display.set_mode(size, pygame.FULLSCREEN, vsync=1)
    
screen = selectedScreenSetup

#game variables
game_paused = False
in_pause_options = False

#define fonts
ubuntu_Eighteen = pygame.font.Font("assets/fonts/Ubuntu.ttf", 18)

#define function to draw text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#lists that contains all sprites
player_sprites = pygame.sprite.Group()
level_sprites = pygame.sprite.Group()
pauseMenu_sprites = pygame.sprite.Group()
menuArrow_sprites = pygame.sprite.Group()

#create player sprite
playerChar = Person(BLACK, 32, 32)
playerChar.rect.x = 320
playerChar.rect.y = 256

#create level sprite
levelArea = Level(BLACK, levelWidth, levelHeight)
levelArea.rect.x = 0
levelArea.rect.y = 0

pauseMenu = PauseScreen(BLACK, 640, 480)
pauseMenu.rect.x = 0
pauseMenu.rect.y = 0

menuArrow = MenuArrow(BLACK, 32, 32)
menuArrow.rect.x = 0
menuArrow.rect.y = 0

#add player character and levels to the list of objects
player_sprites.add(playerChar)
level_sprites.add(levelArea)
pauseMenu_sprites.add(pauseMenu)
menuArrow_sprites.add(menuArrow)

carryOn = True
clock = pygame.time.Clock()

#set everything all coordinates to 0, 0 before the game handles and makes changes to them
coordinates = [0, 0]
coordinateForcastUp = [0, 0]
coordinateForcastDown = [0, 0]
coordinateForcastLeft = [0, 0]
coordinateForcastRight = [0, 0]

#set the coordinates to the coordinates that you should start a level in
levelArea.rect.x = levelArea.rect.x - (startCoords[0] * 32)
levelArea.rect.y = levelArea.rect.y + (startCoords[1] * 32)
coordinates = startCoords

#set a flag that gets used later in code
breakFlag = False

while carryOn:
    

    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we can exit the while loop

    #options menu inside of pause menu
    if in_pause_options:
        #set the fps
        clock.tick(10)

        #key press does action
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RETURN]:
            #exit to pause menu
            if current_button == 1:
                menuArrow.rect.x = 200
                menuArrow.rect.y = 60
                in_pause_options = False
                time.sleep(200000/1000000.0)
            #switch between windowed and fullscreen
            elif current_button == 2:
                if windowed:
                    f = open("saveData/fullscreenconfig.py", "w")
                    f.write("windowed_config = False")
                    f.close()
                    windowed = False
                    pygame.display.set_mode(size, pygame.FULLSCREEN, vsync=1)
                    pygame.WINDOWTAKEFOCUS                    
                else:
                    f = open("saveData/fullscreenconfig.py", "w")
                    f.write("windowed_config = True")
                    f.close()
                    windowed = True
                    screen = pygame.display.set_mode(size, pygame.SCALED, vsync=1)
                time.sleep(200000/1000000.0)

        if keys[pygame.K_w]:
            if current_button == 2:
                current_button = current_button - 1
                menuArrow.arrowUp(160)
                time.sleep(200000/1000000.0)
        
        if keys[pygame.K_s]:
            if current_button == 1:
                current_button = current_button + 1
                menuArrow.arrowDown(160)
                time.sleep(200000/1000000.0)
                

        #update the menu arrow
        menuArrow_sprites.update()
        
        #fill the screen with gray
        screen.fill(GRAY)
        
        #draw arrow sprite to the screen
        menuArrow_sprites.draw(screen)

        draw_text("Back to Menu", ubuntu_Eighteen, WHITE, 260, 120)
        if windowed:
            draw_text("Currently Windowed", ubuntu_Eighteen, WHITE, 260, 280)
        else:
            draw_text("Currently Fullscreen", ubuntu_Eighteen, WHITE, 260, 280)

        #screen update
        pygame.display.flip()
    
    #main pause menu
    elif game_paused:
        #set the fps
        clock.tick(10)

        #pressing keys does actions now
        keys = pygame.key.get_pressed()
        
        #navigate the menu
        if keys[pygame.K_w]:
            if current_button == 2:
                current_button = current_button - 1
                menuArrow.arrowUp(160)
                time.sleep(200000/1000000.0)
            elif current_button == 3:
                current_button = current_button - 1
                menuArrow.arrowUp(160)
                time.sleep(200000/1000000.0)

        if keys[pygame.K_s]:
            if current_button == 1:
                current_button = current_button + 1
                menuArrow.arrowDown(160)
                time.sleep(200000/1000000.0)
            elif current_button == 2:
                current_button = current_button + 1
                menuArrow.arrowDown(160)
                time.sleep(200000/1000000.0)
        
        #menu selection logic
        if keys[pygame.K_RETURN]:
            #resume button
            if current_button == 1:
                game_paused = False
            #options button
            elif current_button == 2:
                current_button = 1
                screen.fill(GRAY)
                in_pause_options = True
                menuArrow.rect.x = 220
                menuArrow.rect.y = 114
                time.sleep(200000/1000000.0)
            #exit button
            elif current_button == 3:
                carryOn = False

        #updating the pause menu sprites
        pauseMenu_sprites.update()
        menuArrow_sprites.update()

        #paint the screen
        screen.fill(GRAY)

        #draw pause menu sprites
        pauseMenu_sprites.draw(screen)
        menuArrow_sprites.draw(screen)

        #screen update
        pygame.display.flip()
    
    else:
        #set the fps
        clock.tick(10)

        #coordinate forecast up
        coordinateForcastUp[0] = coordinates[0]
        coordinateForcastUp[1] = coordinates[1] + 1

        #coordinate forecast down
        coordinateForcastDown[0] = coordinates[0]
        coordinateForcastDown[1] = coordinates[1] - 1

        #coordinate forecast left
        coordinateForcastLeft[0] = coordinates[0] - 1
        coordinateForcastLeft[1] = coordinates[1]

        #coordinate forecast right
        coordinateForcastRight[0] = coordinates[0] + 1
        coordinateForcastRight[1] = coordinates[1]

        #pressing keys does actions now
        keys = pygame.key.get_pressed()
        #Logic for moving up
        if keys[pygame.K_w]:
            for i in range(len(validCoords)):
                if validCoords[i] == coordinateForcastUp:
                    levelArea.moveUp(32)
                    coordinates[1] = coordinates[1] + 1
                    breakFlag = True
                if breakFlag:
                    breakFlag = False
                    break       
        #Logic for moving Left
        elif keys[pygame.K_a]:
            for i in range(len(validCoords)):
                if validCoords[i] == coordinateForcastLeft:
                    levelArea.moveLeft(32)
                    coordinates[0] = coordinates[0] - 1
                    breakFlag = True
                if breakFlag:
                    breakFlag = False
                    break
        #Logic for moving Downward
        elif keys[pygame.K_s]:
            for i in range(len(validCoords)):
                if validCoords[i] == coordinateForcastDown:
                    levelArea.moveDown(32)
                    coordinates[1] = coordinates[1] - 1
                    breakFlag = True
                if breakFlag:
                    breakFlag = False
                    break
        #Logic for moving Right
        elif keys[pygame.K_d]:
            for i in range(len(validCoords)):
                if validCoords[i] == coordinateForcastRight:
                    levelArea.moveRight(32)
                    coordinates[0] = coordinates[0] + 1
                    breakFlag = True
                if breakFlag:
                    breakFlag = False
                    break
        
        #movement keys for when you need to make a list of valid coordinates on a new map
        if keys[pygame.K_UP]:
            levelArea.moveUp(32)
            coordinates[1] = coordinates[1] + 1
        elif keys[pygame.K_LEFT]:
            levelArea.moveLeft(32)
            coordinates[0] = coordinates[0] - 1
        elif keys[pygame.K_DOWN]:
            levelArea.moveDown(32)
            coordinates[1] = coordinates[1] - 1
        elif keys[pygame.K_RIGHT]:
            levelArea.moveRight(32)
            coordinates[0] = coordinates[0] + 1
        #key for opening up the pause menu
        elif keys[pygame.K_ESCAPE]:
            menuArrow.rect.x = 200
            menuArrow.rect.y = 60
            game_paused = True
            current_button = 1


        #debug key set to g you can completely delete this section for final release
        if keys[pygame.K_g]:
            print(" ")
            print("debug info:")
            print("Coordinates: " + str(coordinates))
            print("Coordinate Forecast up: " + str(coordinateForcastUp))
            print("Coordinate Forecast down: " + str(coordinateForcastDown))
            print("Coordinate Forecast left: " + str(coordinateForcastLeft))
            print("Coordinate Forecast right: " + str(coordinateForcastRight))
            print("current resolution: " + str(size))
            
        #Game Logic
        player_sprites.update()
        level_sprites.update()

        #paint the screen
        screen.fill(levelBoundsFill)

        #draw sprites to screen
        level_sprites.draw(screen)
        player_sprites.draw(screen)

        #screen update
        pygame.display.flip()

pygame.quit()