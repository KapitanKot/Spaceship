import pygame, sys, random
from pygame import *
from random import *

class Airshow(object):
    '''Main'''
    
    def __init__(self, width = 600, height = 600):
        
        pygame.init()
        self.started = True
        self.board = Board(width, height)
        self.player = Player(width, height)
        self.enemy = Enemy(width, height)
        self.clock = pygame.time.Clock()

    def events(self):
        '''Event handler'''
        
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_RETURN:
                self.started = True

            if event.type == KEYDOWN:
                if event.key == K_UP:       self.player.move[0] = True
                if event.key == K_DOWN:     self.player.move[1] = True
                if event.key == K_RIGHT:    self.player.move[2] = True
                if event.key == K_LEFT:     self.player.move[3] = True

            if event.type == KEYUP:
                if event.key == K_UP:       self.player.move[0] = False
                if event.key == K_DOWN:     self.player.move[1] = False
                if event.key == K_RIGHT:    self.player.move[2] = False
                if event.key == K_LEFT:     self.player.move[3] = False

    def run(self):
        '''Main loop'''

        ticks = 30
        while not self.events():
            self.board.draw(self.player, self.enemy)
            self.player.movePlayer()
            self.enemy.moveEnemy()
            try:
                self.player.shooting.remove(self.enemy.lifeEnemy(self.player.shooting))
            except:
                pass
            self.player.shoot(ticks)
            if ticks == 30:
                ticks = 0
            ticks += 1
            self.clock.tick(60)
            
class Board(object):
    
    def __init__(self, width, height):
        '''Window'''
        self.window = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption('Airshow')

    def draw(self, *args):
        '''Draw elements'''
        background = (0, 0, 0)
        self.window.fill(background)
        args[0].drawPlayer(self.window)
        args[0].drawShoot(self.window)
        args[1].drawEnemy(self.window)
            
        pygame.display.update()

class Player(object):
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.startX = width/2
        self.startY = height * (4/5)
        self.playerX = self.startX
        self.playerY = self.startY
        self.move = [False, False, False, False]
        self.warplane = 'apEagle.png'
        self.bullet = 'shFire.png'
        self.shooting = []

    def drawPlayer(self, surface):
        '''Draw warplane'''
        
        plane = pygame.image.load(self.warplane)
        surface.blit(plane, (self.playerX-25, self.playerY))

    def movePlayer(self):
        '''Player move'''

        if self.move[0] and self.playerY > self.height*(1/7): self.playerY -= 5
        if self.move[1] and self.playerY < self.height-50: self.playerY += 5
        if self.move[2] and self.playerX < self.width-25: self.playerX += 5
        if self.move[3] and self.playerX > 25: self.playerX -= 5

    def drawShoot(self, surface):
        '''Single shoot'''
        
        shoot = pygame.image.load(self.bullet)
        for i in range(len(self.shooting)):
            surface.blit(shoot, (self.shooting[i][0], self.shooting[i][1]))
        
    def shoot(self, ticks):
        '''Shooting'''

        try:
            if ticks == 30:
                self.shooting.append([self.playerX-5, self.playerY-35])
            if self.shooting[0][1] < 0:
                del(self.shooting[0])
            for i in range(len(self.shooting)):
                self.shooting[i][1] = self.shooting[i][1] - 5        
        except:
            pass

class Enemy(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.startX = randrange(0+25, width-25)
        self.startY = -25
        self.enemyX = self.startX
        self.enemyY = self.startY
        self.enemyplane = 'apCepid.png'
        self.health = 3

    def drawEnemy(self, surface):
        '''Draw enemy spaceship'''

        enemy = pygame.image.load(self.enemyplane)
        surface.blit(enemy, (self.enemyX-25, self.enemyY))

    def moveEnemy(self):
        '''Move enemy spaceship'''
        
        self.enemyY += 3

    def lifeEnemy(self, *args):
        '''Destro spaceship'''

        if self.enemyY > self.height+10 or self.health == 0:
            self.enemyX = randrange(25, self.width-25)
            self.enemyY = self.startY
            self.health = 3
        
        for arg in args:
            for i in range(len(arg)):
                try:
                    if arg[i][0] > self.enemyX - 25 and arg[i][0] < self.enemyX + 25 and arg[i][1] > self.enemyY and arg[i][1] < self.enemyY+50:
                        self.health -= 1
                        return arg[i]
                except:
                    pass
        
if __name__ == "__main__":
    game = Airshow(600, 600)
    game.run()
