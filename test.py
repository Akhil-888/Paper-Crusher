import pygame#INITIALIZE
pygame.init()
pygame.display.set_caption("Paper Crusher")#WINDOW NAME

import sys
import random

screen_width = 650 # GAME WINDOW
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))

score = 0
scissor_width = 150
scissor_height = 125
sframe = 0
hbox_width = 450
hbox_height = 100
vbox_width = 100
vbox_height = 530

left=False
right=False

###############
#Sprites    
bg = pygame.transform.scale(pygame.image.load("BACKGROUND.png.png"), (screen_width, screen_height))

red_hitbox1 = pygame.image.load("redhitbox1.png.png")
green_hitbox1 = pygame.image.load("greenhitbox1.png.png")
blue_hitbox1 = pygame.image.load("bluehitbox1.png.png")
yellow_hitbox1 = pygame.image.load("yellowhitbox1.png.png")

asd = pygame.image.load("asd.png.png")
wsx = pygame.image.load("wsx.png.png")


#################

#scissor class
class Scissor:
    def __init__(self, xcoord, ycoord, s_width, s_height, velocity):
        s = [pygame.transform.scale(pygame.image.load("s1.png.png"), (scissor_width, scissor_height)), 
            pygame.transform.scale(pygame.image.load("s2.png.png"), (scissor_width, scissor_height)), 
            pygame.transform.scale(pygame.image.load("s3.png.png"), (scissor_width, scissor_height))]
        self.send = s[0]
        self.speed = velocity
        self.xcoord = xcoord#
        self.ycoord = ycoord#
        self.frames = [pygame.Surface((scissor_width, scissor_height)) for _ in range(3)]  # Create frames
        self.frames[0].fill((0,0,0))
        self.frames[1].fill((200, 200, 200))
        self.frames[2].fill((150, 150, 150))

    def move(self):
        self.xcoord += self.speed

    def draw(self):
        screen.blit(self.send, (self.xcoord, self.ycoord))




'''
screen_width/2 - hbox_width/2 <= a <= screen_width/2 + hbox_width/2 and 0 <= b <= hbox_height
screen_width/2 - hbox_width/2 <= a <= screen_width/2 + hbox_width/2 and screen_height-97 <= b <= screen_height
'''
send_scissor_down = False
def key_hitbox(a, b):
    draw_window()
    if 100 <= a <= 550 and 0 <= b <= 100:#RED
        screen.blit(red_hitbox1, (screen_width/2 - hbox_width/2 , 0))
        screen.blit(asd, (250,0))
    elif 100 <= a <= 550 and 603 <= b <= 700: #YELLOW
        screen.blit(yellow_hitbox1, (screen_width/2 - hbox_width/2 , screen_height-97))
        screen.blit(asd, (250,screen_height-50))
    if 551<=a<=650 and 85<=b<=615: #GREEN
        screen.blit(green_hitbox1, (551,85))
        screen.blit(wsx, (600, 275))
    elif 0<=a<=99 and 85<=b<=615:#BLUE
        screen.blit(blue_hitbox1, (0,85))
        screen.blit(wsx, (0, 275))
    else:
        pass
scissor = Scissor(100,0,scissor_width,scissor_height,20)

def draw_window():
    screen.blit(bg, (0,0))
    

def main():
    run = True
    scissor_moving = False
    while run:# GAME LOOP
        for event in pygame.event.get(): # QUIT GAME
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a and not scissor_moving:  # Start moving object when a is pressed
                            scissor_moving = True
        
        if scissor_moving:
            scissor.move()
        
            if scissor.xcoord > screen_height-97:
                scissor_moving = False
        
        draw_window()  
        if scissor_moving:
            scissor.draw()
            pygame.display.update()

        
        a,b = pygame.mouse.get_pos()
        key_hitbox(a, b)
        
        '''keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            
        if keys[pygame.K_s]:
            ...
        '''
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()#QUIT

if __name__ == "__main__":#RUN PROGRAM
    main()