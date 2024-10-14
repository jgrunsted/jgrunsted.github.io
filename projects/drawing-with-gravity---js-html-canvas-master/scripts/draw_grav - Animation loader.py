import numpy as np
import pygame
from pygame import gfxdraw
import json


#CHANGE THIS TO THE CONFIGURATION OF PLANETS YOU WANT
CONFIG_FILE_NAME = "binary_star_1"

f = open("scripts/" + CONFIG_FILE_NAME + ".json")
data = json.load(f)
pos_log = open("scripts/" + CONFIG_FILE_NAME + "_pos_log.txt")

TRAIL_LENGTH = 0
CONNECT_DENSITY = 0
FPS_MAX = 0

def draw_circle(surface, x, y, radius, color):		#Custom method for drawing circles w/ aa
    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)

class Obj:
	position = np.array([0.0, 0.0])

	def __init__(self, radius, init_position, color, name, connect=False):
		self.radius = radius			#Radius of the body
		self.position = init_position
		self.color = color 				#Color of the body
		self.name = name				#Name of the body given
		self.points = [(tuple(init_position))]	#All Drawn Points
		self.connect = connect 			#If the body will connect to all other bodies w/ this set to True


	def draw(self, sc):		#handles drawing all elements except connecting lines
		#Draws circles at front of lines
		draw_circle(surface=sc, color=self.color, x=int(self.position[0]), y=int(self.position[1]), radius=int(self.radius))

		#Draws Trails
		self.points.append(tuple(self.position))
		if len(self.points) == TRAIL_LENGTH:
			self.points.pop(0)
		#pygame.draw.aalines(surface=sc, color=self.color, closed=False, points=self.points)

		#Writes labels under the planets
		#label = myfont.render(self.name, 1, (255, 255, 255))
		#sc.blit(label, (self.position[0] - (len(self.name) * 4.3), self.position[1] + self.radius + 2))

		#Old Method of Drawing Circles
		#pygame.draw.circle(surface=sc, color=self.color, center=self.position, radius=self.radius)

	def connect_planets(self, sc, bodies):		#Handles connecting lines between connected bodies
		for body in bodies:
			#connect_points = np.array([[self.points[0], body.points[0]]])
			if body.connect and self.connect:
				connect_points = np.array([[self.points[0], body.points[0]]])
				for i in range(0, len(self.points) - 1, CONNECT_DENSITY):
					connect_points = np.vstack((connect_points, [[self.points[i], body.points[i]]]))					

		if self.connect:
			for pt in connect_points:
				pygame.draw.aaline(surface=sc, color=con_color, start_pos=pt[0], end_pos=pt[1])

planets = []
bg_color = (0, 0, 0)
con_color = (0, 0, 0)
for key, value in data.items():
	if key == "main":
		TRAIL_LENGTH = int(value[0]["trail_length"])
		CONNECT_DENSITY = int(value[0]["connect_density"])
		FPS_MAX = int(value[0]["fps_max"])
		raw_bg = value[0]["bg_color"]
		bg_color = (int(raw_bg.split(',')[0]), int(raw_bg.split(',')[1]), int(raw_bg.split(',')[2]))
		raw_con = value[0]["con_color"]
		con_color = (int(raw_con.split(',')[0]), int(raw_con.split(',')[1]), int(raw_con.split(',')[2]))
	else:
		raw_pos = value[0]["init_position"]
		ipos = [float(raw_pos.split(',')[0]), float(raw_pos.split(',')[1])]
		raw_col = value[0]["color"]
		col = (int(raw_col.split(',')[0]), int(raw_col.split(',')[1]), int(raw_col.split(',')[2]))
		planets.append(Obj(radius=float(value[0]["radius"]), init_position=ipos, color=col, name=key, connect=(value[0]["connect"] == "True")))

lines = pos_log.readlines()
pos = []
for i in range(len(lines)):
	line = lines[i].split(",")
	pos.append((line[0], float(line[1]), float(line[2])))

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size=[1000, 1000], flags=pygame.NOFRAME)
running = True
screen.fill(bg_color)

plan = [item for item in range(0, len(planets))]

c = 0

#Fills background with stars
#stars = []
#for i in range(100):
#	stars.append((np.random.randint(0, 999), np.random.randint(0, 999)))

#mouse_down = False #Tracks if mouse is down

myfont = pygame.font.SysFont("monospace", 15)	#Font used in labels

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		#if mouse_down != True:		#uncomment below for drag and drop
		#	mouse_down = (event.type == pygame.MOUSEBUTTONDOWN)
		#else:
		#	mouse_down = (event.type != pygame.MOUSEBUTTONUP)

	screen.fill(bg_color)

	#For putting stars in the background
	#for star in stars:
	#	screen.fill(color=(255, 255, 255), rect=(star, (1, 1)))

	clock.tick(FPS_MAX) #Time Passed since last main loop in ms

	four = []

	for j in plan:
		if c >= len(pos):
			planets[j].points = [tuple(np.array([pos[j][1], pos[j][2]]))]
		planets[j].position = np.array([pos[j][1], pos[j][2]])
		planets[j].draw(screen)
		planets[j].connect_planets(screen, planets)
		four.append(pos[j])
		c = c + 1

	if c > len(pos):
		c = 0

	pos = pos[len(planets): len(pos)]
	for f in four:
		pos.append(f)

	#FPS counter in top right corner (for debug)
	#lb = myfont.render(str(clock.get_fps()), 1, (255, 255, 255))
	#screen.blit(lb, (900, 10))

	pygame.display.flip()

pygame.quit()