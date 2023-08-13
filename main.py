
#first we  import pygame
#pygame is a 2d graphics library/module that lets you make little games.
#when working with pygame we create something called a surfice or window
# so everything we work with when using pygame is called a surfice.

import pygame
import os
#we import os because we need to use the images in the assets folder and to do that we need their directory
#sepificly for this line of code:
#YELLOW_SPACESHIP_IMAGE = pygame.image.load("")
#os means operating system and allows us to get the directory of the file
pygame.font.init() #to show some text or numbers in the window we need to  initialise the fonts for the text



WIDTH, HEIGHT = 900, 500  #it is good to name all constant variables in capital letters
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #opens a window but it closes immediately thats why we need a while loop
#to continue forever and keep the window forever untill we decide to close it.
pygame.display.set_caption("First game!")

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT) #this creates a rectangel witch is going to be the border.
#we want the border in the middle so """WIDTH//2"""but(all shapea in pygame start form the top left corner)very important
#just like the pygame window, so this would start in the middle and end a bit farther from the middle.
#so we need the shapes middel to be in the mddel of the window so we need to place it a bit before the middle.
#10 is the width of the recktangle    """Explonation 2"""

#// means that the answer is turned into a int even if it has decimal points meaning it is rounded

HEALTH_FONT = pygame.font.SysFont('Times New Roman', 40) #here we are defineing the font and size of the text
WINNER_FONT = pygame.font.SysFont('Times New Roman', 100)#here we declare another font

FPS = 60 #this means frames per second witch is the number of times the  event loop will run in a secod
# because the event loop is a infinite loop. For as long as the window is running the loop is running.

VELOCITY = 5 #how much a spaceship moves one we press one of the kyes

BULLET_VELOCITY = 7 #this shows how fast the bullet moves
MAX_BULLETS = 3 #max number of bullets


BULLET_HIT_YELLOW = pygame.USEREVENT +1 #this is how we create our own event just like the events we have used.
# the +1 is used to define one event from one another. so it is like saying EVENT 1. +2 EVENT 2.
BULLET_HIT_RED = pygame.USEREVENT +2 #This two events will be used in the main loop
# to check if something collided with the rectangle.

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 65, 50

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))#lodes immage from assets
YELLOW_SPACESHIP = pygame.transform.rotate (pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)#changes size of the image and rotates it 90degree

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))#lodes immage from assets
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, yellow_bullets,red_bullets, red_health, yellow_health): # here wi will ad stuf to the window
    WIN.blit(BACKGROUND_IMAGE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)#here we apply:font,size,text,color
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)#same for yellow
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 18))#we draw it in the window and position it.
    WIN.blit(yellow_health_text, (10, 18))#we draw it in the window and position it.


    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    """WIN.blit(YELLOW_SPACESHIP, (100, 200))"""#here we use cordinat system here we use cordinat system is used to put
    # the immages or text that we have loded on to the screenan important thing to know is the pygame cordinat system.
    # 0,0 starts at the top left when we increse x we go right and when we increse y we go down """Explonarion 1"""
    WIN.blit(RED_SPACESHIP, (red.x, red.y))




    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()  # we can draw a bunch of stuff in the screen but unless we update it
    # they will not be shown

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0:  # this if statement moves the spaceship left because we
        # are subtracting from x. the other one checks is the spaceship cordinates are out of the window
        yellow.x -= VELOCITY  # it is getting closer to 0,0 because of the pygame coordination system.
        # this means the spaceship will move 5 places on this direction: ←/left/back only if the a key is pressed.
    if keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width < BORDER.x:  # moves right
        yellow.x += VELOCITY      #we need this               ↑ because when we dont account the width we are saying
        # that the top left corner of spaceship must not br greater than the  top left of the border.but the width
        # would pass to the others side so we need to account the width as well.         """Exploration 3"""
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0:  # moves up
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT : # moves down
        yellow.y += VELOCITY

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width :  #moves left
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY + red.width < WIDTH:  # moves right
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0:  # moves up
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT:  # moves down
        red.y += VELOCITY




def handle_bullets(yellow_bullets,red_bullets, yellow, red):#in this function we will make the bullets move
# and check if any of them have collided with a spaceship
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY #moves the bullet to the right →
        if red.colliderect(bullet): #checks if the spaceship has collided with a bullet
            pygame.event.post(pygame.event.Event(BULLET_HIT_RED))# here we are posting an event witch allows us to use
# this event that we created
            yellow_bullets.remove(bullet) #removes the bullet if it has collided
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY #moves to the left ←
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BULLET_HIT_YELLOW))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text): #we are not doing it in the draw window is because we want to pause the game, text, than restart
    winner_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(winner_text, (WIDTH/2 - winner_text.get_width()/2, HEIGHT/2 - winner_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main(): # in this function we are going to write all the code for the game and the loop
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)#this creates a rectangle with a x and y position
    # as well as height and width. this will represent the spaceships positions. we use this to make it easier

    red_bullets = [] #this list stores the red players bullets
    yellow_bullets = [] #this list stores the yellow players bullets
    red_health = 10 #health of red spaceship
    yellow_health =10 #health of yellow spaceship

    clock = pygame.time.Clock() #this and the clock.tick help define the times the loop runs
    run = True #for as long as the variable run is true the loop will continue for ever.
    while run: # this is called the event loop
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN: #this allows us to continue the if statement only if the button is pressed
                                                #and not if it is held down
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS: #if the left CTRL key is pressed
                   bullet = pygame.Rect(yellow.x + yellow.width, yellow.y +yellow.height//2 - 2, 10, 5)#here we created
                #a rectangle that  has a (position x, position y, width, height) this places the bullet in front of
                #the spaceship
                   yellow_bullets.append(bullet)#this adds the rect bullet in the yellow_bullet list

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)



            if event.type == BULLET_HIT_RED: #if red is hit we subtract 1 from the health amount
                red_health -= 1
            if event.type == BULLET_HIT_YELLOW: #if yellow is hit we subtract 1 from the health amount
                yellow_health -=1

        winner_text = ""
        if red_health <= 0: #if health of red is lower or equal to 0 we want to get the text yello wins
            winner_text = "Yellow wins!"
        if yellow_health == 0: #if health of red is lower or equal to 0 we want to get the text yello wins
            winner_text = "Red wins!"

        if winner_text != "":
            draw_winner(winner_text)


        keys_pressed = pygame.key.get_pressed() #every single time the loop runs meaning 60 times a second,
#it will tell us what keys are being pressed so we can check what keys are being pressed
#and if the keys we want are being pressed we can respond.

        red_handle_movement(keys_pressed, red)
        yellow_handle_movement(keys_pressed, yellow)

        handle_bullets(yellow_bullets,red_bullets, yellow, red)

        draw_window(red, yellow, yellow_bullets, red_bullets, red_health, yellow_health)

    pygame.quit()
# here we check what event is accusing in pygame if the event being used is quit
#if it is we sto running the loop therefor closing the game.


if __name__ == "__main__":
    main()

#this makes sure that we run this main function only if it is ran in this python file directly.
# So if we run it from another file because we imported it as a module there it wold not run.
#So the game would run only from this file.



