import pygame
from pygame import mixer
import os
import time

pygame.init()

SCREENX = 1000
SCREENY = 750

SHEEP_IMGS = [pygame.image.load(os.path.join('Sprites', 'SheepRight.png')), pygame.image.load(os.path.join('Sprites', 'SheepUp.png')), pygame.image.load(os.path.join('Sprites', 'SheepLeft.png')), pygame.image.load(os.path.join('Sprites', 'SheepDown.png'))]
STILL_SHEEP = [pygame.image.load(os.path.join('Sprites', 'Sheep.png')), pygame.image.load(os.path.join('Sprites', 'Sheeplookingleft.png')), pygame.image.load(os.path.join('Sprites', 'Sheeplookingright.png'))]
SHEEP_BAA = mixer.Sound(os.path.join('Sounds', 'SheepBaa.ogg'))
DYNAMITE_IMG = pygame.image.load(os.path.join('Sprites', 'Not_exploded_dynamite.png'))
EXPLODED_DYNAMITE = pygame.image.load(os.path.join('Sprites', 'Explosion.png'))
DYNAMITE_SOUND = mixer.Sound(os.path.join('Sounds', 'Dynamite_Explostion.ogg'))
BLOCK = pygame.image.load(os.path.join('Sprites', 'Block.png'))

class Sheep:         #Name is Larry

    VELOSITY = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False
        self.Moving_IMGS = SHEEP_IMGS
        self.Still_IMGS = STILL_SHEEP
        self.curIMG = SHEEP_IMGS[0]
        self.Animation_time = 50
        self.frame_count = 0
        self.last_direction = (None, None)

    def move(self, leftKey, rightKey, upKey, downKey):

        #Last direction stuff
        #True = Positive X or Y
        #False = Negative X or Y
        #None = No movement
        #E.g. (True, None) means positve x (Right) movement, no y movement
        #Or (False, True) means negative x (Left), positive y (Down)
        
        if leftKey and upKey:
            self.curIMG = pygame.transform.rotate(self.Moving_IMGS[1], 45)
            self.x -= self.VELOSITY
            self.y -= self.VELOSITY
            self.frame_count = 0                                                    #I don't like how this is structed atm. I would like to change it
            self.last_direction = (False, False)                                    #First, remove self.x -= etc, and make 
        elif leftKey and downKey:
            self.curIMG = pygame.transform.rotate(self.Moving_IMGS[3], -45)
            self.x -= self.VELOSITY
            self.y += self.VELOSITY
            self.frame_count = 0
            self.last_direction = (False, True)
        elif rightKey and upKey:
            self.curIMG = pygame.transform.rotate(self.Moving_IMGS[1], -45)
            self.x += self.VELOSITY
            self.y -= self.VELOSITY
            self.frame_count = 0
            self.last_direction = (True, False)
        elif rightKey and downKey:
            self.curIMG = pygame.transform.rotate(self.Moving_IMGS[3], 45)
            self.x += self.VELOSITY
            self.y += self.VELOSITY
            self.frame_count = 0
            self.last_direction = (True, True)
        elif leftKey:
            self.curIMG = self.Moving_IMGS[2]
            self.x -= self.VELOSITY
            self.frame_count = 0
            self.last_direction = (False, None)
        elif rightKey:
            self.curIMG = self.Moving_IMGS[0]
            self.x += self.VELOSITY
            self.frame_count = 0
            self.last_direction = (True, None)
        elif upKey:
            self.curIMG = self.Moving_IMGS[1]
            self.y -= self.VELOSITY
            self.frame_count = 0
            self.last_direction = (None, False)
        elif downKey:
            self.curIMG = self.Moving_IMGS[3]
            self.y += self.VELOSITY
            self.frame_count = 0
            self.last_direction = (None, True)
        else:
            self.rotated = False
            self.frame_count += 1
            if self.frame_count < self.Animation_time:
                self.curIMG = self.Still_IMGS[0]
            elif self.frame_count < self.Animation_time*2:
                self.curIMG = self.Still_IMGS[1]
            elif self.frame_count < self.Animation_time*3:
                self.curIMG = self.Still_IMGS[0]
            elif self.frame_count < self.Animation_time*4:
                self.curIMG = self.Still_IMGS[2]
            elif self.frame_count < self.Animation_time*5:
                self.curIMG = self.Still_IMGS[0]
                SHEEP_BAA.play()
            elif self.frame_count == self.Animation_time*5 + 1:
                self.curIMG = self.Still_IMGS[0]
                self.frame_count = 0
        
        if self.x <= 0:
            self.x = 0
        if self.x >= SCREENX - 20:
            self.x = SCREENX - 20
        if self.y <= 0:
            self.y = 0
        if self.y >= SCREENY - 20:
            self.y = SCREENY- 20

    def draw(self, screen):
        screen.blit(self.curIMG, (self.x, self.y))

class Dynamite:

    VELOSITY = 15

    def __init__(self, x, y, last_direction):
        self.x = x
        self.y = y
        self.curIMG = DYNAMITE_IMG
        self.last_direction = last_direction
        self.image_count = 0
        self.exploding = False
        self.exploded = False

    def update(self):
        self.move()

    def move(self):
        if self.exploding:
            self.explode()
        else:
            if self.last_direction[0] == True and not self.exploding:
                self.x += self.VELOSITY
            if self.last_direction[0] == False and not self.exploding:
                self.x -= self.VELOSITY
            if self.last_direction[1] == True and not self.exploding:
                self.y += self.VELOSITY
            if self.last_direction[1] == False and not self.exploding:
                self.y -= self.VELOSITY
            if self.last_direction[0] == None and self.last_direction[1] == None and not self.exploding:
                self.x -= self.VELOSITY
            #if dynamite.x < 10 or dynamite.x > SCREENX - 20 or dynamite.y < 10 or dynamite.y > SCREENY - 20:
                #self.explode()
            if self.x < 1:
                self.x = 0
                self.explode()
            elif self.x > SCREENX - 21:
                self.x = SCREENX -20
                self.explode()
            elif self.y < 1:
                self.y = 0
                self.explode()
            elif self.y > SCREENY - 21:
                self.y = SCREENY - 20
                self.explode()

    def explode(self):
        self.exploding = True
        DYNAMITE_SOUND.play()
        self.curIMG = EXPLODED_DYNAMITE
        self.image_count += 1
        if self.image_count == 100:
            self.exploded = True
        

    def draw(self, screen):
        screen.blit(self.curIMG, (self.x, self.y))

class Enemy:

    VELOSITY = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.curIMG = BLOCK    #For now
        self.isShooting = False
        self.projectiles = []

    def update(self):
        self.shoot()

    def shoot(self):
        if not self.isShooting:
            self.projectiles.append(Dynamite(self.x, self.y, (None, False)))
            self.projectiles.append(Dynamite(self.x, self.y, (True, None)))
            self.projectiles.append(Dynamite(self.x, self.y, (None, True)))
            self.projectiles.append(Dynamite(self.x, self.y, (False, None)))
            self.isShooting = True

        if self.isShooting:
            for p in self.projectiles:
                if p.exploded:
                    self.projectiles.remove(p)
                
        if len(self.projectiles) == 0:
            self.isShooting = False

    def draw(self, screen):
        screen.blit(self.curIMG, (self.x, self.y))
        if self.isShooting:
            for p in self.projectiles:
                p.update()
                p.draw(screen)

def main():        
    sheep = Sheep(500, 500)
    screen = pygame.display.set_mode((SCREENX, SCREENY))
    pygame.display.update()

    objects = []
    #toRemove = []

    leftKey = False
    rightKey = False
    upKey = False
    downKey = False

    global dynamite
    unlocked_dynamite = True    #Change when progress
    dynamite_on_screen = False

    clock = pygame.time.Clock()
    running = True

    while running:

        clock.tick(60)
        screen.fill((255,255,255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    leftKey = True
                if event.key == pygame.K_RIGHT:
                    rightKey = True
                if event.key == pygame.K_UP:
                    upKey = True
                if event.key == pygame.K_DOWN:
                    downKey = True
                
                if event.key == pygame.K_SPACE and unlocked_dynamite and not dynamite_on_screen:
                    dynamite = Dynamite(sheep.x, sheep.y, sheep.last_direction)
                    objects.append(dynamite)
                    dynamite_on_screen = True

                if event.key == pygame.K_n:
                    enemy = Enemy(500, 500)
                    objects.append(enemy)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    leftKey = False
                if event.key == pygame.K_RIGHT:
                    rightKey = False
                if event.key == pygame.K_UP:
                    upKey = False
                if event.key == pygame.K_DOWN:
                    downKey = False
        
        if dynamite_on_screen:
            print(dynamite.x, dynamite.y)
            if dynamite.exploded:
                objects.remove(dynamite)
                dynamite_on_screen = False
        

        # for r in toRemove:
        #     objects.remove(r)
        #     toRemove.remove(r)

        sheep.move(leftKey, rightKey, upKey, downKey)
        sheep.draw(screen)

        for obj in objects:
            obj.update()
            obj.draw(screen)

        pygame.display.update()
        #print(sheep.frame_count)
        #print(sheep.x, sheep.y)
 

main()