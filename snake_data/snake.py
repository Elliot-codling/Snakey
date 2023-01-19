#snakey
from engine import game_engine_130123 as engine
import pygame, os, random
file_dir = os.getcwd()

#create window
w, h = 300, 300
window = engine.window.define("Snekey", w, h, pygame.SCALED, 1)

#variables
run = True
clock = pygame.time.Clock()
direction = "right"         #direction the player is moving in
#rotation = 90           #current rotation in degrees
score = 0

#lists
display = []            #display
for x in range(20):             #creates the squares
    for y in range(20):
        square = engine.properties_object("square", f"{file_dir}/textures/background_square.png", x * 15, y * 15, 15, 15, False)
        display += [square]

#display_sprite
display_sprite = []
player = engine.properties_object("player", f"{file_dir}/textures/snake_head.png", 0, 0, 15, 15, False, 90)
display_sprite += [player]

#foreground
foreground = []
#text_foreground
text_foreground = []

#sub code
def moveHead():               #moves the player in the direction requested
    wallCheck = False
    if direction == "up":
        wallCheck = engine.player.up(player, 15, 0)
    elif direction == "down":
        wallCheck = engine.player.down(player, 15, h - 15)
    elif direction == "left":
        wallCheck = engine.player.left(player, 15, 0)
    elif direction == "right":
        wallCheck = engine.player.right(player, 15, w - 15)

    #check if the player hit the wall at any point, end the game
    if wallCheck:
        game_over()        

def moveBody():             #move the body by deleting the first body and adding to the list
    global foreground
    del foreground[0]
    addBody()
    
def addBody():              #add a body to the snake
    global foreground
    snake_body = engine.properties_object("snake_body", f"{file_dir}/textures/snake_body.png", player.x + 1, player.y + 1, 13, 13, False)
    foreground += [snake_body]

def create_apple():                 #create the apple in a random location
    global display_sprite
    x = random.randint(0, 19)
    y = random.randint(0, 19)
    apple = engine.properties_object("apple", f"{file_dir}/textures/apple.png", x * 15 + 1, y * 15 + 1, 13, 13, False)          #apple is slgihtly smaller than the squares
    display_sprite += [apple]

def game_over():                #ends the game
    global text_foreground
    gameOver_text = engine.properties_text("lost_text", "Game Over!", "YELLOW", w, h, 30, True)
    score_text = engine.properties_text("score", f"Score: {score}", "YELLOW", w, h + 50, 30, True)
    text_foreground += [gameOver_text, score_text]
    #update the display to all the user to read their score
    update(display, display_sprite, foreground, text_foreground)
    pygame.time.delay(1500)                     #wait for 1000ms
    reset_game()            #reset everything to defaults

def reset_game():                 #resets the whole game
    global foreground, text_foreground
    global direction, score
    player.x = 0                #reset the player position and angle
    player.y = 0
    engine.player.setAngle(player, 90)
    foreground = []
    text_foreground = []
    direction, score = "right", 0

def update(display, display_sprite, foreground, text_foreground):               #update the screen
    engine.window.update(window, display, display_sprite, foreground, text_foreground)

#main code
def main():
    global foreground
    global score, direction
    #set player direction - cannot move from up to down or similar directions as that will go through yourself
    if (keys[pygame.K_w] or keys[pygame.K_UP]) and direction != "down":
        direction = "up"
        engine.player.setAngle(player, 0)
    elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and direction != "up":
        direction = "down"
        engine.player.setAngle(player, 180)
    elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and direction != "right":
        direction = "left"
        engine.player.setAngle(player, 270)
    elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and direction != "left":
        direction = "right"
        engine.player.setAngle(player, 90)
    
    for index in range(len(display_sprite)):                    #check if collided with apple, if so add to the score
        if engine.player.collisions(player, display_sprite, index) == "apple":
            score += 1
            del display_sprite[index]               #delets the apple
            create_apple()                  #creates a new apple
            addBody()                       #adds to the whole snakebody
            break

    if engine.frames % 2 == 0:
        if len(foreground) != 0:
            moveBody()      #move the snakes body if the foreground isnt empty
        moveHead()         #move the snake head

        #collision check
        for index in range(len(foreground)):            #check if the player has collided with the snakes body
            if engine.player.collisions(player, foreground, index) == "snake_body":
                game_over()
                break           #break from the loop

create_apple()              #creates an apple at the start
while run:
    #keyboard and exit button, main code -----------------------------
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False

    main()          #runs the main game
    update(display, display_sprite, foreground, text_foreground)
    engine.counter.update()
    clock.tick(12)
pygame.quit()