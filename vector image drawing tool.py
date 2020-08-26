import pygame
from pygame import *
import math
from pygame import gfxdraw
import random
import os.path
import pickle

xSize=1920
ySize=1080
def removeDuplicated(x):
    p = []
    for i in x:
        if i not in p:
            
            p.append([i[0]-(xSize/2), i[1]-(ySize/2)])
            pass
    return(p)

fileName = "Vectors.pckl"
#Pygame stuff
pygame.init()

win = pygame.display.set_mode((xSize, ySize), pygame.FULLSCREEN)
pygame.display.set_caption("Vector Drawing Tool")

def middlePoint(p1, p2):#returns what point is in the middle
    return([(p1[0]+p2[0])/2, (p1[1]+p2[1])/2])

run = True
mouseDown = False
keepers = []
firstTime = True
win.fill((255,255,255)) #resets window
while run:

    mouseP = pygame.mouse.get_pos()



    for event in pygame.event.get():  # This will loop through a list of any keyboard or mouse events.
        #if mouseDown:
        #    mouseDown = False
        if (event.type == MOUSEBUTTONDOWN):
            mouseDown = not mouseDown
        if (mouseDown):
            

            if firstTime:
                lastP = mouseP
                firstTime = False
            else:
                
                x1 = lastP[0]
                x2 = mouseP[0]
                y1 = lastP[1]
                y2 = mouseP[1]
                #keepers.append([list(lastP), list(mouseP)])
                
                
                keepers.append([list(lastP), middlePoint(lastP, mouseP)])


                keepers.append([middlePoint(lastP, mouseP), list(mouseP)])

                
                    
                lastP = mouseP
        if event.type == pygame.QUIT: # Checks if the red button in the corner of the window is clicked
            run = False  # Ends the game loop
    keys = pygame.key.get_pressed()
    if (keys[K_SPACE] == 1):
        run = False


    
    for i in range(len(keepers)):
        pygame.draw.line(win, (0, 0, 0), keepers[i][0], keepers[i][1], 5)


    pygame.display.update()
pygame.quit()

for i in keepers:

    i[0][0] -= xSize/2
    i[0][1] -= ySize/2
    i[1][0] -= xSize/2
    i[1][1] -= ySize/2
    i[0][0] /= 80
    i[0][1] /= 80
    i[1][0] /= 80
    i[1][1] /= 80



"""
for i in range(len(keepers)):
    x1 = keepers[i][0][0]
    x2 = keepers[i][1][0]
    y1 = keepers[i][0][1]
    y2 = keepers[i][1][1]
    slope = (y1-y2)/(x1-x2)
    yintercept = (x1*y2 - x2*y1)/(x1-x2)
    keepers.insert(i, )
"""
f = open(fileName, 'wb')
pickle.dump(keepers, f)
f.close()

print("saved it as: " + fileName+'. the length is ' + str(len(keepers)))

"""reading from it
f = open('test1.pckl', 'rb')
obj = pickle.load(f)
f.close()
print(obj)
"""
