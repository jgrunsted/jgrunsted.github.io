import numpy as np
import pygame
from pygame import gfxdraw
import scipy.constants as sp
import json


#CHANGE THIS TO THE CONFIGURATION OF PLANETS YOU WANT
CONFIG_FILE_NAME = "binary_star_1"


f = open("scripts/" + CONFIG_FILE_NAME + ".json")
data = json.load(f)

TRAIL_LENGTH = 0
CONNECT_DENSITY = 0
FPS_MAX = 0

#ENABLING CERTAIN FUNCTIONS WILL REDUCE PERFORMANCE

def draw_circle(surface, x, y, radius, color):		#Custom method for drawing circles w/ aa
    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)

class Body:
	position = np.array([0.0, 0.0])		#Position Vector of the body
	velocity = np.array([0.0, 0.0])		#Velocity Vector of the body
	acceleration = np.array([0.0, 0.0])	#Acceleration Vector of the body
	nf = np.array([0.0, 0.0])			#Net Force Vector of the body
	mouse = False						#If the mouse is on the body
	
	collided = False					#Internal Tracking

	def __init__(self, mass, radius, init_position, color, init_velocity, init_acceleration, name, connect=False, fixed_pos=False):
		self.mass = mass				#Mass of the body
		self.radius = radius			#Radius of the body
		self.position = init_position	
		self.color = color 				#Color of the body
		self.velocity = init_velocity
		self.acceleration = init_acceleration
		self.name = name				#Name of the body given
		self.points = [tuple(init_position)]	#All Drawn Points
		self.connect = connect 			#If the body will connect to all other bodies w/ this set to True
		self.fixed_pos = fixed_pos		#If this will have a fixed position

	def set_pos(self, passed_time):
		if self.fixed_pos != True:
			self.position = self.position + (self.velocity * (passed_time / 1000))
		if self.position[0] <= -30000 or self.position[0] >= 30000:
			self.position[0] = 30000
		if self.position[1] <= -30000 or self.position[1] >= 30000:
			self.position[1] = 30000


	def set_vel(self, passed_time):
		self.velocity = self.velocity + (self.acceleration * (passed_time / 1000))

	def set_acc(self, bodies):
		#self.acceleration = np.array([0.0, 0.0])
		self.nf = np.array([0.0, 0.0])
		for body in bodies:
			dist = np.sqrt((self.position[0] - body.position[0])**2 + (self.position[1] - body.position[1])**2)
			u = [body.position[0] - self.position[0], body.position[1] - self.position[1]] / dist
			if body.position[0] == self.position[0] and body.position[1] == self.position[1]:
				continue
			#Collision (Don't reccomend, is very janky)
			#elif ((self.position[0] - body.position[0])**2 + (self.position[1] - body.position[1])**2) <= (self.radius + body.radius)**2:
			#	self.velocity = self.velocity - (2*body.mass / (self.mass + body.mass)) * ((np.dot(self.velocity - body.velocity, self.position - body.position)) / ((self.position - body.position)**2)) * (self.position - body.position)
			#	body.velocity = body.velocity - (2*self.mass / (self.mass + body.mass)) * ((np.dot(body.velocity - self.velocity, body.position - self.position)) / ((self.position - body.position)**2)) * (body.position - self.position)
			#	body.collided = True
			#	break
			self.nf = self.nf + (((sp.G * 100000000000) * self.mass * body.mass)/((dist*1000)**2)) * u
		self.collided = False
		self.acceleration = self.nf / self.mass

	def draw(self, sc):		#handles drawing all elements except connecting lines
		#Draws circles at front of lines
		draw_circle(surface=sc, color=self.color, x=int(self.position[0]), y=int(self.position[1]), radius=int(self.radius))

		#Draws Trails
		self.points.append(tuple(self.position))
		if len(self.points) == TRAIL_LENGTH:
			self.points.pop(0)
		pygame.draw.aalines(surface=sc, color=self.color, closed=False, points=self.points)

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
		raw_vel = value[0]["init_velocity"]
		ivel = [float(raw_vel.split(',')[0]), float(raw_vel.split(',')[1])]
		raw_acc = value[0]["init_acceleration"]
		iacc = [float(raw_acc.split(',')[0]), float(raw_acc.split(',')[1])]
		raw_col = value[0]["color"]
		col = (int(raw_col.split(',')[0]), int(raw_col.split(',')[1]), int(raw_col.split(',')[2]))
		planets.append(Body(mass=float(value[0]["mass"]), radius=float(value[0]["radius"]), init_position=ipos, color=col, init_velocity=ivel, init_acceleration=iacc, name=key, connect=(value[0]["connect"] == "True"), fixed_pos=(value[0]["fixed_pos"] == "True")))

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size=[1000, 1000], flags=pygame.NOFRAME)
running = True
screen.fill(bg_color)

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

	tp = clock.tick(FPS_MAX) #Time Passed since last main loop in ms

	for planet in planets:
		#Tracks if mouse is over a planet:
		#planet.mouse = (((pygame.mouse.get_pos()[0] - planet.position[0])**2 + (pygame.mouse.get_pos()[1] - planet.position[1])**2) <= planet.radius**2 + 100)

		#Drag and Drop functionality with planets (uncomment and comment the three set functions below it)
		#if planet.mouse and mouse_down:
		#	planet.position = np.array([pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]])
		#	planet.velocity = np.array(pygame.mouse.get_rel())*35
		#else:
		#	planet.set_acc(planets)
		#	planet.set_vel(tp)
		#	planet.set_pos(tp)

		planet.set_acc(planets)
		planet.set_vel(tp)
		planet.set_pos(tp)

		planet.draw(screen)
		planet.connect_planets(screen, planets)

	#FPS counter in top right corner (for debug)
	#lb = myfont.render(str(clock.get_fps()), 1, (0, 0, 0))
	#screen.blit(lb, (900, 10))
	
	pygame.display.flip()

pygame.quit()