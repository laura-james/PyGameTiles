import pygame
import config
import colors
import random

pygame.mixer.init()
sound = pygame.mixer.Sound("bell.wav")


class Enemy:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def draw(self):
		rect = [self.x * config.tilesizeX, self.y * config.tilesizeY, config.tilesizeX, config.tilesizeY]
		# pygame.draw.rect(screen, colors.WHITE, rect)
		screen.blit(ghostImg, (self.x * config.tilesizeX + 6, self.y * config.tilesizeY + 6))

	def moverandom(self):
		# random move
		# detect the 4 cells around it
		neighbours = []
		if self.x > 0:
			# IF I'M NOT AT THE LEFT EDGE I KNOW i CAN ADD THE TILE TO LEFT
			neighbours.append(tiles[self.y][self.x - 1])
		if self.x < config.tilediv - 2:  # minus 2 as tilediv is 11 and last index is 10
			# IF I'M NOT AT THE RIGHT EDGE I KNOW i CAN ADD THE TILE TO RIGHT
			neighbours.append(tiles[self.y][self.x + 1])
		if self.y > 0:
			# IF I'M NOT AT THE TOP EDGE I KNOW i CAN ADD THE TILE ABOVE
			neighbours.append(tiles[self.y - 1][self.x])
		if self.y < config.tilediv - 2:  # minus 2 as tilediv is 11 and last index is 10
			# IF I'M NOT AT THE BOTTOM EDGE I KNOW i CAN ADD THE TILE BELOW
			neighbours.append(tiles[self.y + 1][self.x])
		# this method for removing the stone cels from the list only works for the first item
		# for n in neighbours:
		# if n.type == "stone":
		# neighbours.remove(n)
		# this list comprehension works to remove all items that are stone
		neighbours = [n for n in neighbours if n.type != "stone"]
		newtile = random.choice(neighbours)
		self.x = newtile.x
		self.y = newtile.y

	def move(self):
		# detect the 4 cells around ghost and add to an array
		neighbours = []
		if self.x > 0:
			# IF I'M NOT AT THE LEFT EDGE I KNOW i CAN ADD THE TILE TO LEFT
			neighbours.append(tiles[self.y][self.x - 1])
		if self.x < config.tilediv - 2:  # minus 2 as tiliediv is 11 and last index is 10
			# IF I'M NOT AT THE RIGHT EDGE I KNOW i CAN ADD THE TILE TO RIGHT
			neighbours.append(tiles[self.y][self.x + 1])
		if self.y > 0:
			# IF I'M NOT AT THE TOP EDGE I KNOW i CAN ADD THE TILE ABOVE
			neighbours.append(tiles[self.y - 1][self.x])
		if self.y < config.tilediv - 2:  # minus 2 as tiliediv is 11 and last index is 10
			# IF I'M NOT AT THE BOTTOM EDGE I KNOW i CAN ADD THE TILE BELOW
			neighbours.append(tiles[self.y + 1][self.x])
		# if the cell is stone - then can't go there
		for n in neighbours:
			if n.type == "stone":
				neighbours.remove(n)
		# add the cell the enemy is on to the neighbours array as there's no point moving if i'm already at the closest place
		neighbours.append(tiles[self.y][self.x])
		shortestdist = 99  # ARBITRARY BIG DISTANCE
		# NOW LOOP THROUGH ALL NBOURS CALCULATING DIST BETWEEN ENEMY AND PLAYER
		for n in neighbours:
			# work out the distance between itself and the player
			dist = abs(playerX - n.x) + abs(playerY - n.y)
			# print(dist)
			if dist < shortestdist:
				shortestdist = dist
				nearestn = n
			# whichever is the shortest distance the enemy moves to
		self.x = nearestn.x
		self.y = nearestn.y


class Tile:

	def __init__(self, type, x, y):
		self.type = "blank"
		self.x = x
		self.y = y

	def draw(self, x, y):
		rect = [x * config.tilesizeX, y * config.tilesizeY, config.tilesizeX, config.tilesizeY]
		if self.type == "blank":
			pygame.draw.rect(screen, colors.LGREEN, rect)
		elif self.type == "stone":
			pygame.draw.rect(screen, colors.ORANGE, rect)
		elif self.type == "test":
			pygame.draw.rect(screen, colors.RED, rect)  # added to help debug the neighbours for the ghost move
		elif self.type == "exit":
			pygame.draw.rect(screen, colors.RED, rect)
		elif self.type == "coin":
			pygame.draw.circle(screen, colors.YELLOW,
												 [(x * config.tilesizeX) + config.tilesizeX // 2, y * config.tilesizeY + config.tilesizeX // 2],
												 config.tilesizeX // 2)
		else:
			pygame.draw.rect(screen, colors.BLUE, rect)

		# used to label the square
		# pick a font you have and set its size
		myfont = pygame.font.SysFont("Arial", 13)
		# apply it to text on a label
		label = myfont.render(str(x) + "," + str(y), 1, colors.BLACK)
		# put the label object on the screen at point x=100, y=100
		screen.blit(label, (x * config.tilesizeX, y * config.tilesizeY))

	def getRect(self):
		rect = [self.x * config.tilesizeX, self.y * config.tilesizeY, config.tilesizeX, config.tilesizeY]
		return rect

	def changeType(self):
		# cycle through the types of tile - used on mouse click as a cheat
		if self.type == "blank":
			self.type = "stone"
		elif self.type == "stone":
			self.type = "coin"
		elif self.type == "coin":
			self.type = "blank"
		# self.draw(self.x, self.y)
		print(self.x, self.y)


def writetext(text, x, y):
	# not used?
	# pick a font you have and set its size
	myfont = pygame.font.SysFont("Arial", 13)
	# apply it to text on a label
	label = myfont.render(text, 1, colors.BLACK)
	# put the label object on the screen at point x=100, y=100
	screen.blit(label, (x, y))


def printmessages():
	y = 510
	for msg in messages:
		writetext(msg, 10, y)
		y = y + 10


def drawrandomblocks():
	# added new thing to read from a text File NO LONGER RANDOM
	f = open("map.txt")
	mapgrid = f.readlines()
	f.close()
	# print(len(mapgrid))
	for i in range(len(mapgrid)):
		# print(mapgrid[i].strip())
		splitstuff = mapgrid[i].strip().split(",")
		# print(splitstuff)
		for j in range(len(splitstuff)):
			# print(splitstuff[j])
			if splitstuff[j] == "b":
				tiles[i][j].type = "stone"
			if splitstuff[j] == "c":
				tiles[i][j].type = "coin"


def drawrandomcoins():
	# NO LONGER USED AS DRAWN FROM MAP.TXT
	for i in range(10):
		rnumX = random.randint(0, config.tilediv - 1)
		rnumY = random.randint(0, config.tilediv - 1)
		# TODO to stop the random blocks appearing at the center
		tiles[rnumX][rnumY].type = "coin"


def drawallblanktiles():
	# SETS UP THE BLANK TILE ARRAY
	# NOTE IT IS REFERENCED Y COORDINATE FIRST!!!!
	global tiles
	tiles = [[Tile("blank", i, j) for i in range(config.tilediv)] for j in range(config.tilediv)]


def drawexitsquare():
	# add exit point
	# now that i have added outer walls exit sq can't be 0 or tilediv-1
	rnumX = random.randint(1, config.tilediv - 2)
	tiles[config.tilediv - 1][rnumX].type = "exit"


pygame.init()

screen = pygame.display.set_mode(config.size)
pygame.display.set_caption(config.wtitle)
clock = pygame.time.Clock()

# init position of player IN CENTRE OF 11 BY 11 GRID
playerX = 5
playerY = 5
twidth = config.tilesizeX
theight = config.tilesizeY
ghostImg = pygame.image.load("ghost.png")
ghostdelay = 0
GHOSTFRICTION = 1  # higher number slows ghosts down

tiles = []
drawallblanktiles()
messages = []
collectedcoins = 0
drawrandomblocks()  # these are now drawn in the map.txt - ie not random!
# drawrandomcoins() # these are now drawn in the map.txt
drawexitsquare()
# spawn ENEMIES
ghost = Enemy(1, 1)
ghost2 = Enemy(9, 9)

moveLeft = False
moveRight = False
moveUp = False
moveDown = False

done = False
while not done:
	oldplayerX = playerX
	oldplayerY = playerY
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		elif event.type == pygame.KEYDOWN:
			if event.key in (pygame.K_UP, pygame.K_w):
				moveDown = False
				moveUp = True
			elif event.key in (pygame.K_DOWN, pygame.K_s):
				moveDown = True
				moveUp = False
			elif event.key in (pygame.K_LEFT, pygame.K_a):
				moveRight = False
				moveLeft = True
			elif event.key in (pygame.K_RIGHT, pygame.K_d):
				moveRight = True
				moveLeft = False
		elif event.type == pygame.KEYUP:
			if event.key in (pygame.K_LEFT, pygame.K_a):
				moveLeft = False
			elif event.key in (pygame.K_RIGHT, pygame.K_d):
				moveRight = False
			elif event.key in (pygame.K_UP, pygame.K_w):
				moveUp = False
			elif event.key in (pygame.K_DOWN, pygame.K_s):
				moveDown = False

		if event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			clickX = int(pos[0] // (config.screenwidth / config.tilediv))
			clickY = int(pos[1] // (config.screenheight / config.tilediv))
			tiles[clickY][clickX].changeType()  # change type of tile when clicked on

		if moveDown:
			playerY = playerY + 1

		if moveUp:
			playerY = playerY - 1

		if moveLeft:
			playerX = playerX - 1

		if moveRight:
			playerX = playerX + 1

	screen.fill(colors.RED)

	# game logic
	for i in range(config.tilediv):
		for j in range(config.tilediv):
			# print(tiles[i][j].type)
			# check if the player goes off edge of map
			if (playerX == -1 or playerX == config.tilediv) or (playerY == -1 or playerY == config.tilediv):
				playerX = oldplayerX
				playerY = oldplayerY
			# have they hit a stone wall?
			if playerX == i and playerY == j and tiles[j][i].type == "stone":
				playerX = oldplayerX
				playerY = oldplayerY
			# have they reached the exit?
			if playerX == i and playerY == j and tiles[j][i].type == "exit":
				# TODO put this in a separate function
				print("hurray you reached the exit")
				messages.append("hurray you reached the exit")
				# reset the game
				# todo - load a different map?
				drawallblanktiles()
				drawrandomblocks()
				# drawrandomcoins()
				drawexitsquare()
				playerX = 5
				playerY = 5
				ghost.x, ghost.y = 1, 1
				ghost2.x, ghost2.y = 9, 9
				messages.clear()
			# collect coins
			if playerX == i and playerY == j and tiles[j][i].type == "coin":
				collectedcoins = collectedcoins + 1
				tiles[j][i].type = "blank"
				print("coin collected")
				sound.play()
				messages.append("coin collected " + str(collectedcoins))
				pygame.display.set_caption("coin collected " + str(collectedcoins))

	# draw tile map
	for i in range(config.tilediv):
		for j in range(config.tilediv):
			newX = i - playerX + config.tilediv
			newY = j - playerY + config.tilediv
			tiles[i][j].draw(j, i)

	# draw grid lines
	for i in range(config.tilediv):
		pygame.draw.line(screen, colors.BLACK, [i * twidth, 0], [i * twidth, config.screenheight])
		for j in range(config.tilediv):
			pygame.draw.line(screen, colors.BLACK, [0, j * theight], [config.screenwidth, j * theight])
	# draw player
	# TODO make this a Player class as a the moment its just a blue square
	pygame.draw.rect(screen, colors.BLUE, [playerX * twidth, playerY * theight, twidth, theight])
	# pygame.draw.rect(screen, colors.BLUE, [config.tilediv//2 * twidth, config.tilediv//2 * theight, twidth, theight])
	printmessages()

	ghostdelay += 1
	if ghostdelay > GHOSTFRICTION:
		ghost.move()
		ghost2.moverandom()
		ghostdelay = 0

	ghost.draw()
	ghost2.draw()
	# print(pygame.time.get_ticks())

	pygame.display.flip()
	clock.tick(20)
pygame.quit()
