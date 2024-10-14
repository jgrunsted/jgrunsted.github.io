import numpy as np
import pygame
from pygame import gfxdraw
import scipy.constants as sp
import json

data = {}
CONFIG_FILE_NAME = "many_particles_1"

#CONSTANTS >> MESS WITH THESE AND THE PLANETS
TRAIL_LENGTH = 50
CONNECT_DENSITY = 10000
FPS_MAX = 100
bg_color = (255,255,250) 	#rgb
con_color = (255,255,250)	#rgb

data["main"] = []
data["main"].append({
	"trail_length": str(TRAIL_LENGTH),
	"connect_density": str(CONNECT_DENSITY),
	"fps_max": str(FPS_MAX),
	"bg_color": str(bg_color[0]) + "," + str(bg_color[1]) + "," + str(bg_color[2]),
	"con_color": str(con_color[0]) + "," + str(con_color[1]) + "," + str(con_color[2])
})

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


#MESS WITH THESE
star1 = Body(mass=1500000000000, radius=4, init_position=[500, 500], color=(10,10,10), init_velocity=[0, 130], init_acceleration=[0, 0], name="star1", connect=False, fixed_pos=True)
#star2 = Body(mass=2000000000000, radius=4, init_position=[700, 500], color=(250,250,250), init_velocity=[0, -130], init_acceleration=[0, 0], name="star2", connect=False)
p1 = Body(mass=1, radius=0, init_position=[20, 50], color=(10,10,10), init_velocity=[100, 0], init_acceleration=[0, 0], name="p1", connect=False)
p2 = Body(mass=1, radius=0, init_position=[20, 100], color=(10,10,10), init_velocity=[100, 0], init_acceleration=[0, 0], name="p2", connect=False)
p3 = Body(mass=1, radius=0, init_position=[20, 150], color=(10,10,10), init_velocity=[100, 0], init_acceleration=[0, 0], name="p3", connect=False)
p4 = Body(mass=1, radius=0, init_position=[20, 200], color=(10,10,10), init_velocity=[100, 0], init_acceleration=[0, 0], name="p4", connect=False)
p5 = Body(mass=1, radius=0, init_position=[20, 250], color=(10,10,10), init_velocity=[100, 0], init_acceleration=[0, 0], name="p5", connect=False)
p6 = Body(mass=1, radius=0, init_position=[20, 300], color=(10,10,10), init_velocity=[100, 0], init_acceleration=[0, 0], name="p6", connect=False)
p7 = Body(mass=1, radius=0, init_position=[20, 350], color=(10,10,10), init_velocity=[100, 0], init_acceleration=[0, 0], name="p7", connect=False)
p8 = Body(mass=1, radius=0, init_position=[20, 400], color=(10,10,10), init_velocity=[100, 0], init_acceleration=[0, 0], name="p8", connect=False)
p9 = Body(mass=1, radius=0, init_position=[20, 450], color=(10,10,10), init_velocity=[100, 0], init_acceleration=[0, 0], name="p9", connect=False)
p10 = Body(mass=1, radius=0, init_position=[20, 550], color=(10,10,10), init_velocity=[100, 0], init_acceleration=[0, 0], name="p10", connect=False)
p11 = Body(mass=1, radius=0, init_position=[20, 600], color=(10,10,10), init_velocity=[100, 0], init_acceleration=[0, 0], name="p11", connect=False)
p12 = Body(mass=1, radius=0, init_position=[20, 650], color=(10,10,10), init_velocity=[100, 0], init_acceleration=[0, 0], name="p12", connect=False)
p13 = Body(mass=1, radius=0, init_position=[20, 700], color=(10,10,10), init_velocity=[100, 0], init_acceleration=[0, 0], name="p13", connect=False)
p14 = Body(mass=1, radius=0, init_position=[20, 750], color=(10,10,10), init_velocity=[100, 0], init_acceleration=[0, 0], name="p14", connect=False)
p15 = Body(mass=1, radius=0, init_position=[20, 800], color=(10,10,10), init_velocity=[100, 0], init_acceleration=[0, 0], name="p15", connect=False)
p16 = Body(mass=1, radius=0, init_position=[20, 850], color=(10,10,10), init_velocity=[100, 0], init_acceleration=[0, 0], name="p16", connect=False)
p17 = Body(mass=1, radius=0, init_position=[20, 900], color=(10,10,10), init_velocity=[100, 0], init_acceleration=[0, 0], name="p17", connect=False)
p18 = Body(mass=1, radius=0, init_position=[20, 950], color=(10,10,10), init_velocity=[100, 0], init_acceleration=[0, 0], name="p18", connect=False)
d1 = Body(mass=1, radius=0, init_position=[980, 50], color=(10,10,10), init_velocity=[-100, 0], init_acceleration=[0, 0], name="d1", connect=False)
d2 = Body(mass=1, radius=0, init_position=[980, 100], color=(10,10,10), init_velocity=[-100, 0], init_acceleration=[0, 0], name="d2", connect=False)
d3 = Body(mass=1, radius=0, init_position=[980, 150], color=(10,10,10), init_velocity=[-100, 0], init_acceleration=[0, 0], name="d3", connect=False)
d4 = Body(mass=1, radius=0, init_position=[980, 200], color=(10,10,10), init_velocity=[-100, 0], init_acceleration=[0, 0], name="d4", connect=False)
d5 = Body(mass=1, radius=0, init_position=[980, 250], color=(10,10,10), init_velocity=[-100, 0], init_acceleration=[0, 0], name="d5", connect=False)
d6 = Body(mass=1, radius=0, init_position=[980, 300], color=(10,10,10), init_velocity=[-100, 0], init_acceleration=[0, 0], name="d6", connect=False)
d7 = Body(mass=1, radius=0, init_position=[980, 350], color=(10,10,10), init_velocity=[-100, 0], init_acceleration=[0, 0], name="d7", connect=False)
d8 = Body(mass=1, radius=0, init_position=[980, 400], color=(10,10,10), init_velocity=[-100, 0], init_acceleration=[0, 0], name="d8", connect=False)
d9 = Body(mass=1, radius=0, init_position=[980, 450], color=(10,10,10), init_velocity=[-100, 0], init_acceleration=[0, 0], name="d9", connect=False)
d10 = Body(mass=1, radius=0, init_position=[980, 550], color=(10,10,10), init_velocity=[-100, 0], init_acceleration=[0, 0], name="d10", connect=False)
d11 = Body(mass=1, radius=0, init_position=[980, 600], color=(10,10,10), init_velocity=[-100, 0], init_acceleration=[0, 0], name="d11", connect=False)
d12 = Body(mass=1, radius=0, init_position=[980, 650], color=(10,10,10), init_velocity=[-100, 0], init_acceleration=[0, 0], name="d12", connect=False)
d13 = Body(mass=1, radius=0, init_position=[980, 700], color=(10,10,10), init_velocity=[-100, 0], init_acceleration=[0, 0], name="d13", connect=False)
d14 = Body(mass=1, radius=0, init_position=[980, 750], color=(10,10,10), init_velocity=[-100, 0], init_acceleration=[0, 0], name="d14", connect=False)
d15 = Body(mass=1, radius=0, init_position=[980, 800], color=(10,10,10), init_velocity=[-100, 0], init_acceleration=[0, 0], name="d15", connect=False)
d16 = Body(mass=1, radius=0, init_position=[980, 850], color=(10,10,10), init_velocity=[-100, 0], init_acceleration=[0, 0], name="d16", connect=False)
d17 = Body(mass=1, radius=0, init_position=[980, 900], color=(10,10,10), init_velocity=[-100, 0], init_acceleration=[0, 0], name="d17", connect=False)
d18 = Body(mass=1, radius=0, init_position=[980, 950], color=(10,10,10), init_velocity=[-100, 0], init_acceleration=[0, 0], name="d18", connect=False)

#PUT ALL BODIES YOU WANT IN THE planets LIST
planets = [star1, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15, d16, d17, d18]

pos_logger = open(CONFIG_FILE_NAME + "_pos_log.txt", "w")

for p in planets:
	data[p.name] = []
	data[p.name].append({
		"mass": str(p.mass), 
		"radius": str(p.radius), 
		"color": str(p.color[0]) + "," + str(p.color[1]) + "," + str(p.color[2]), 
		"init_position": str(p.position[0]) + "," + str(p.position[1]), 
		"init_velocity": str(p.velocity[0]) + "," + str(p.velocity[1]), 
		"init_acceleration": str(p.acceleration[0]) + "," + str(p.acceleration[1]), 
		"connect": str(p.connect), 
		"fixed_pos": str(p.fixed_pos)
	})

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size=[1000, 1000])
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
		pos_logger.write(planet.name + "," + str(planet.position[0]) + "," + str(planet.position[1]) + "\n")

	#FPS counter in top right corner (for debug)
	#lb = myfont.render(str(clock.get_fps()), 1, (255, 255, 255))
	#screen.blit(lb, (900, 10))
	
	pygame.display.flip()

pygame.quit()

pos_logger.close()

with open("scripts/" + CONFIG_FILE_NAME + ".json", "w") as configfile:
	json.dump(data, configfile, indent=4)