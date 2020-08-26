import pygame
from pygame import *
import math
from pygame import gfxdraw
import random
import pickle
global keepers
from pygame.locals import *
keepers = []


importFileName = "Vectors.pckl"
fileName = "finished"#file name for where the finished vectors are stored
n = 10#number of sequences in the infinite sum/vectors calculated

timeScale = 15 #time(sec) for it to make one full cycle
sizeConst = 60
sketchMode = False#if enabled, it will only show the sketch and no circles
#downloadVectors = None #leave blank to generate
downloadVectors = None #if this is a string, it will search for that string and import preloaded vectors from it skipping the calculations
integralPrecision = 100

def fitToScreen(x = 0, y = 0):
	if (type(x)==complex):
		return(((int((x.real * sizeConst) +(xSize/2)), int((x.imag * sizeConst) +(ySize/2)))))
	return(((int((x * sizeConst) +(xSize/2)), int((y * sizeConst) +(ySize/2)))))



def comToTuple(com):
	return((int(com.real), int(com.imag)))


f = open(importFileName, 'rb')
obj = pickle.load(f)
f.close()



def f(x):#basic drawing before it goes through transformation
	#return(complex((x*6)-1, 0))
	totalDistance = 0
	for i in obj:
		lineLength = math.sqrt( (i[1][0]-i[0][0])**2 + (i[1][1] - i[0][1])**2 )
		totalDistance += lineLength
	linePercent = 0
	for i in range(len(obj)):
		lineLength = math.sqrt( (obj[i][1][0]-obj[i][0][0])**2 + (obj[i][1][1] - obj[i][0][1])**2 )
		linePercent += lineLength/totalDistance
		#print(i, linePercent)
		if (x<linePercent):


			return(complex(obj[i][0][0], obj[i][0][1]))
		else:
			pass


def integral(func, coef = 1):
	g=0
	for i in range(0, integralPrecision):
		g += func(i/integralPrecision)*math.e**((-1*coef)*2*math.pi*complex(0, 1)* i/integralPrecision)
	return((g/integralPrecision))




vectors = [] #list of vectors that make the system

def roundedComplex(c):
	return(round(c.real, 1), round(c.imag, 1))

#Pygame stuff
pygame.init()
xSize=1920
ySize=1080
win = pygame.display.set_mode((xSize, ySize), pygame.FULLSCREEN)
pygame.display.set_caption("Fourier Series (with no trigonomics)")
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 70)

#creates class that will later fill a list that has the infinite series
class vector():

	"""
	start = complex(0, 0)
	end = complex(0, 0)
	constCo = complex(1, 0)
	rotationalCo = 1
	"""

	def __init__(self, constCo = complex(1, 0), rotationalCo = 1, pencil = False):
		self.constCo = constCo
		self.rotationalCo = rotationalCo
		self.start = complex(0, 0)
		self.end = complex(0, 0)
		self.pencil = pencil #pencil mode draws a line where the endpoint is

	def drawMe(self, time, last = complex(0, 0)):
		
		self.end = self.constCo*math.e**(self.rotationalCo * 2 * math.pi * complex(0, 1) * time) + last
		self.start = last
		# the endpoint is getting what the endpoint would be if the start point is 0
		#condenses the future code A TON
		startpoint = fitToScreen(self.start)
		endpoint = fitToScreen(self.end)
		
		
		#draws the line, circle at the top, and the circle around it
		if (sketchMode == False):
			try:
				pygame.draw.circle(win, (136, 179, 247), startpoint, int(math.sqrt((self.constCo.real*sizeConst)**2 + (self.constCo.imag*sizeConst)**2)), 1)
			except:
				pass
			pygame.draw.line(win, (0,0,0),startpoint, endpoint, 2)
			
			pygame.draw.circle(win, (255, 0, 0), endpoint, 4)

			if (self.pencil == True):
				keepers.append(endpoint)#removes duplicated to help prevent lag

			
		

		
run = True


#insane math stuff going on here
if (type(downloadVectors) != str):
	for i in range(0, n):
		print(str(len(vectors)/2) + "/" + str(n))
		win.fill((255, 255, 255))

		textsurface = myfont.render(str(len(vectors)/2)[:-2] + "/" + str(n) + " vectors generated...", False, (0, 0, 0))
		win.blit(textsurface,(xSize/2-800,ySize/2))


		pygame.display.update()

		#print(i)
		vectors.append(vector(integral(f, i), i))
		vectors.append(vector(integral(f, i*-1), i*-1))
		
		#print((roundedComplex(integral(f, i)), i))
	f = open(fileName+".pckl", 'wb')
	pickle.dump(vectors, f)
	f.close()
else:
	f = open(downloadVectors, 'rb')
	vectors = pickle.load(f)
	f.close()

	

del vectors[0]
del vectors[0]


for i in range(len(vectors)):
	#print(((round(vectors[i].constCo.real),round(vectors[i].constCo.imag)), vectors[i].rotationalCo, i))
	pass
vectors[-1].pencil = True
while run:
	

	rawTime = pygame.time.get_ticks()-800#stores time and gives it a second to get going
	timeS = rawTime / (1000 * timeScale) #every 10 seconds





	
	win.fill((255,255,255)) #resets window



	if (sketchMode):
		if (timeS<=1):
			pygame.draw.circle(win, (255, 0, 0), ((fitToScreen(f(timeS).real, f(timeS).imag))), 6)
			keepers.append((fitToScreen(f(timeS).real, f(timeS).imag)))
		

	#its not adaptiong to the ones before it and keeping them at 0
	
	for i in range(len(vectors)):
		#print(i, (round(vectors[i].start.real*100), round(vectors[i].start.imag*100)), (round(vectors[i].end.real*100), round(vectors[i].end.imag*100)))
		if (i==0):
			vectors[i].drawMe(timeS)
			#print(i, vectors[i-1].end)
		else:
			vectors[i].drawMe(timeS,vectors[i-1].end)
	
	x=0
	y=0


	#pygame.draw.circle(win, (50, 0, 255), (int(x/len(keepers)), int(y/len(keepers))), 10, 1)#gonna delete this later i am just messing around

	#goes through all the "pencil points" and plots lines to make them more smooth

		

		



	

	

	#basic pygame stuff
	for event in pygame.event.get():  # This will loop through a list of any keyboard or mouse events.
		if event.type == pygame.QUIT: # Checks if the red button in the corner of the window is clicked
			run = False  # Ends the game loop
	keys = pygame.key.get_pressed()
	if (keys[K_SPACE] == 1):
		run = False
	for i in range(1, len(keepers)):
		pygame.draw.line(win, (212, 88, 0),keepers[i-1], keepers[i], 5)
	pygame.display.update()

