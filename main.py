import pygame, sys, random
from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.display.set_caption("Rain rain rain")
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGD_COLOUR = (230, 255, 250)
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))


enemy_image = pygame.image.load("Assets/enemy.png").convert_alpha()
cloud_image_tr = pygame.transform.scale(enemy_image, (50,25))

bullet_sound = pygame.mixer.Sound("Assets/shoot.wav")

stars_image = pygame.image.load ("Assets/stars.jpg").convert()
stars_image_tr = pygame.transform.scale(stars_image, (SCREEN_WIDTH,SCREEN_HEIGHT))


player_image = pygame.image.load("Assets/avatar.png").convert()

# image should not have been converted with convert_alpha(0 but with convert()
player_image.set_colorkey((255,255,255))
clock = pygame.time.Clock()

Ui_font = pygame.font.SysFont("arial", 25)

# class Stars:
# 	def __init__(self, x ,y):
# 		self.x = x
# 		self.y = y
# 		self.velo1 = random.randint(1,10)
# 		self.accel1 = random.randint(1, 10)
#
# 	def move(self):
# 		self.y += self.accel1
#
# 	def draw(self):
# 		pygame.draw.circle(screen, (150,150,150), (self.x, self.y), 2)

class Laser:
	def __init__(self, x ,y):
		self.x = x
		self.y = y
		self.velo = random.randint(1,10)
		self.accel = random.randint(1, 10)

	def move(self):
		self.y += self.accel

	def draw(self):
		pygame.draw.circle(screen, (150,150,150), (self.x, self.y), 2)


class Cloud:
	def __init__(self, x, y, spd):
		self.x = x
		self.y = y
		self.movespeed = spd

	def move(self):

		self.x += self.movespeed

		if self.x >= SCREEN_WIDTH -50 or self.x <= 50:

			self.movespeed *= -1
			self.y = self.y + 130

	def draw(self):
		screen.blit(cloud_image_tr, (self.x, self.y))

	def createrain(self):
		raindrops.append(Laser(random.randint(self.x, self.x+100), self.y+50))

	def collide (self , bullet):
		return pygame.Rect (self.x,self.y, 50 ,50).collidepoint((bullet.x, bullet.y))



class Player:
	def __init__(self):
		self.x = 0
		self.y = SCREEN_HEIGHT - 50
		self.health = 3

	def move(self):
		if pressed_keys[K_RIGHT] and self.x <SCREEN_WIDTH - 60:
			self.x += 0.175

		if pressed_keys[K_LEFT] and self.x > 0:
			self.x -= 0.175

		# if pressed_keys[K_SPACE]:
		#
		# 	pygame.draw.circle(screen, (150, 150, 150), (self.x + 30, self.y), 5)

	def draw(self):
		screen.blit(player_image, (self.x,self.y))

		pygame.draw.rect(screen, (200, 0, 50), (10, 10, 20,self.health *100))

	def createbullet(self):
		bullets.append(Bullet(self.x + 30, self.y))





class Bullet:

	def __init__(self, x ,y):
		self.x = x
		self.y = y


	def move(self):
		self.y -= 0.25

	def draw(self):
		pygame.draw.line(screen, (0,255,0), (self.x , self.y) ,(self.x , self.y - 10), 4)

	def collide (self , cloud):
		return pygame.Rect (self.x,self.y, 50 ,50).collidepoint((cloud.x, cloud.y))




raindrops = []
bullets = []
cloudsss = []
for i in range(1,10):
	cloudsss.append(Cloud(10 + (i*75),0, 0.1))
	cloudsss.append(Cloud(10 + (i*75),65, 0.1))

player = Player()


while 1:
	#pygame registers all events from the users into an event queue
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			player.createbullet()
			bullet_sound.play()
		# if event.type == pygame.KEYDOWN and event.key == pygame.K_0:
		# # 	y += 2

	pressed_keys = pygame.key.get_pressed()
	screen.fill(BACKGD_COLOUR)
	screen.blit(stars_image_tr, (0, 0))


	# Creating the rain one raindrop at a time
	# cloud.createrain()


	player.draw()
	player.move()

	#for raindrop in raindrops:
	#	raindrop.move()
	#	raindrop.draw()
	for bullet in bullets:
		bullet.move()
		bullet.draw()
		for cloud in cloudsss:
			if cloud.collide(bullet):
				bullets.remove(bullet)
				cloudsss.remove(cloud)

	for cloud in cloudsss:
		cloud.draw()
		cloud.move()









	pygame.display.flip()
