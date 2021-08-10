import pygame
import config, colors, random
pygame.mixer.init()
sound = pygame.mixer.Sound("bell.wav")


class Tile:

    def __init__(self, x, y, type):
        self.type = "blank"
        self.x = x
        self.y = y

    def draw(self, x, y):
        rect = [x * config.tilesizeX, y * config.tilesizeY, config.tilesizeX, config.tilesizeY]
        if self.type == "blank":
            pygame.draw.rect(screen, colors.LGREEN, rect)
        elif self.type == "stone":
            pygame.draw.rect(screen, colors.ORANGE, rect)
        elif self.type == "exit":
            pygame.draw.rect(screen, colors.RED, rect)
        elif self.type == "coin":
            pygame.draw.circle(screen, colors.YELLOW, [(x * config.tilesizeX)+config.tilesizeX//2, y * config.tilesizeY+config.tilesizeX//2],config.tilesizeX//2)
        else:
            pygame.draw.rect(screen, colors.BLUE, rect)
        # pick a font you have and set its size
        myfont = pygame.font.SysFont("Arial", 13)
        # apply it to text on a label
        label = myfont.render(str(x) + "," + str(y), 1, colors.BLACK)
        # put the label object on the screen at point x=100, y=100
        screen.blit(label, (x * config.tilesizeX, y * config.tilesizeY))

    def clicked(self):
        print("clicked")

    def getRect(self):
        rect = [self.x * config.tilesizeX, self.y * config.tilesizeY, config.tilesizeX, config.tilesizeY]
        return rect

    def changeType(self):
        if self.type == "blank":
            self.type = "stone"
        elif self.type == "stone":
            self.type = "coin"
        elif self.type == "coin":
            self.type = "blank"
        #self.draw(self.x, self.y)
        print(self.x, self.y)


def writetext(text, x, y):
    # pick a font you have and set its size
    myfont = pygame.font.SysFont("Arial", 13)
    # apply it to text on a label
    label = myfont.render(text, 1, colors.BLACK)
    # put the label object on the screen at point x=100, y=100
    screen.blit(label, (x, y))


def printmessages():
    y = 10
    for msg in messages:
        writetext(msg, 10, y)
        y = y + 10


def drawrandomblocks():
    for i in range(20):
        rnumX = random.randint(0, config.tilediv - 1)
        rnumY = random.randint(0, config.tilediv - 1)
        # TODO to stop the random blocks appearing at the center
        tiles[rnumX][rnumY].type = "stone"


def drawrandomcoins():
    for i in range(10):
        rnumX = random.randint(0, config.tilediv - 1)
        rnumY = random.randint(0, config.tilediv - 1)
        # TODO to stop the random blocks appearing at the center
        tiles[rnumX][rnumY].type = "coin"


def drawallblanktiles():
    global tiles
    tiles = [[Tile("blank",i,j) for i in range(config.tilediv)] for j in range(config.tilediv)]


def drawexitsquare():
    # add exit point
    rnumX = random.randint(0, config.tilediv - 1)
    tiles[config.tilediv - 1][rnumX].type = "exit"

pygame.init()

screen = pygame.display.set_mode(config.size)
pygame.display.set_caption(config.wtitle)
clock = pygame.time.Clock()

# init position of player
playerX = 5
playerY = 5
twidth = config.tilesizeX
theight = config.tilesizeY


tiles = []
drawallblanktiles()
messages = []
collectedcoins = 0
drawrandomblocks()
drawrandomcoins()
drawexitsquare()

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
        #if pygame.mouse.get_pressed()[0] and pygame.Rect(0, 0, 90, 90).collidepoint(pygame.mouse.get_pos()):
        #    print("you clicked the top corner")
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print(pos)
            print(pos[0] // (config.screenwidth / config.tilediv), pos[1] // (config.screenheight / config.tilediv))
            clickX = int(pos[0]//(config.screenwidth/config.tilediv))
            clickY = int(pos[1]//(config.screenheight/config.tilediv))
            print(tiles[clickY][clickX].type)
            tiles[clickY][clickX].changeType()
            print(tiles[clickY][clickX].type)

            # get a list of all sprites that are under the mouse cursor
            #clicked_tiles = [t for t in tiles if t.getRect().collidepoint(pos)]
            #clicked_tiles = [t for i in range(config.tilediv)] for j in range(config.tilediv)]
            # do something with the clicked sprites...
            #for i in range(config.tilediv):
                #for j in range(config.tilediv):
                #    print(tiles[j][i].type)
                #if t.getRect().collidepoint(pos):
                #    print("you clicked on "+t.type)
    #if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
    if moveDown:
        playerY = playerY + 1
    #if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
    if moveUp:
        playerY = playerY - 1
    #if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
    if moveLeft:
        playerX = playerX - 1
    #if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
    if moveRight:
        playerX = playerX + 1
    #print(playerX, playerY)
    # print(tiles[playerY][playerX].type)
    #print("moveup "+str(moveUp)+" movedown "+str(moveDown)+"moveleft"+str(moveLeft)+"moveright"+str(moveRight))
    screen.fill(colors.RED)

    # game logic
    for i in range(config.tilediv):
        for j in range(config.tilediv):
            # print(tiles[i][j].type)
            # check if the player goes outside the boundary
            if (playerX == -1 or playerX == config.tilediv) or (playerY == -1 or playerY == config.tilediv):
                print("out of bounds")
                playerX = oldplayerX
                playerY = oldplayerY
            # have they hit a stone wall?
            if playerX == i and playerY == j and tiles[j][i].type == "stone":
                print("collision")
                playerX = oldplayerX
                playerY = oldplayerY
            # have they reached the exit?
            if playerX == i and playerY == j and tiles[j][i].type == "exit":
                print("hurray you reached the exit")
                messages.append("hurray you reached the exit")
                drawallblanktiles()
                drawrandomblocks()
                drawrandomcoins()
                drawexitsquare()
                playerX = 5
                playerY = 5
                messages.clear()
            #collect coins
            if playerX == i and playerY == j and tiles[j][i].type == "coin":
                collectedcoins = collectedcoins + 1
                tiles[j][i].type = "blank"
                print("coin collected")
                sound.play()
                messages.append("coin collected " + str(collectedcoins))
                pygame.display.set_caption("coin collected " + str(collectedcoins))

        # when you touch exit point the map changes
        # add new type of block? coins? transport
        # click on items? messages eg help? reset/ show points

    # draw tile map
    for i in range(config.tilediv):
        for j in range(config.tilediv):
            newX = i - playerX + config.tilediv
            newY = j - playerY + config.tilediv
            tiles[i][j].draw(j, i)
            # try:
            #    tiles[newY][newX].draw(newX, newY)
            # except:
            #    print("out of range newX"+str(newX)+" newY"+str(newY))

    # draw grid
    for i in range(config.tilediv):
        pygame.draw.line(screen, colors.BLACK, [i * twidth, 0], [i * twidth, config.screenheight])
        for j in range(config.tilediv):
            pygame.draw.line(screen, colors.BLACK, [0, j * theight], [config.screenwidth, j * theight])
    # draw player
    pygame.draw.rect(screen, colors.BLUE, [playerX * twidth, playerY * theight, twidth, theight])
    # pygame.draw.rect(screen, colors.BLUE, [config.tilediv//2 * twidth, config.tilediv//2 * theight, twidth, theight])
    printmessages()

    pygame.display.flip()
    clock.tick(20)
pygame.quit()
