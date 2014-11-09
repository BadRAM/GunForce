import pygame, random

#button state variable, order: axes, A(z) B(x) START(enter) SELECT(shift)
#SELECT and START cannot be held
global buttons
buttons = [[0, 0], 0, 0, 0, 0]
pygame.init()
pygame.font.init()
text = pygame.font.Font('PressStart.ttf', 8)
clock = pygame.time.Clock()

global state
state = 1

global ents
ents = []

#read config file
config = open("config.ini")

cfg_resx = int(config.readline())
cfg_resy = int(config.readline())
cfg_res = [cfg_resx, cfg_resy]

cfg_fscreen = config.readline()

if cfg_fscreen == 1:
    cfg_fscreen = pygame.FULLSCREEN

cfg_debug = int(config.readline())
global screen
screen = pygame.display.set_mode(cfg_res)
config.close()

#sprite & sound imports + colorkeys
spr_menutext = [
text.render('TM 2014 Corrupt Memory studios', 0, [250, 250, 250]),
text.render('Start', 0, [250, 250, 250]),
text.render('Start', 0, [100, 100, 100]),
text.render('Highscores', 0, [250, 250, 250]),
text.render('Highscores', 0, [100, 100, 100]),
text.render('Quit', 0, [250, 250, 250]),
text.render('Quit', 0, [100, 100, 100])
]
spr_logo = pygame.image.load('titletext.bmp')
spr_logo.set_colorkey([0, 0, 0])
spr_player = pygame.image.load('player.bmp')
spr_player.set_colorkey([255, 255, 255])
spr_machinegun = pygame.image.load('machinegun.bmp')
spr_machinegun.set_colorkey([255, 255, 255])
spr_shotgun = pygame.image.load('shotgun.bmp')
spr_shotgun.set_colorkey([255, 255, 255])
spr_rocketlauncher = pygame.image.load('rocketlauncher.bmp')
spr_rocketlauncher.set_colorkey([255, 255, 255])
spr_lazergun = pygame.image.load('beamlazergun.bmp')
spr_lazergun.set_colorkey([255, 255, 255])
spr_specialgun = pygame.image.load('specialgun.bmp')
spr_specialgun.set_colorkey([255, 255, 255])
spr_bullet = pygame.image.load('bullet.bmp')
spr_bullet.set_colorkey([255, 255, 255])
spr_rocket = pygame.image.load('rocket.bmp')
spr_rocket.set_colorkey([255, 255, 255])
spr_beamlazer = pygame.image.load('beamlazer.bmp')
spr_beamlazer.set_colorkey([255, 255, 255])
spr_redupgrade = pygame.image.load('redupgrade.bmp')
spr_greenupgrade = pygame.image.load('greenupgrade.bmp')
spr_blueupgrade = pygame.image.load('blueupgrade.bmp')
spr_yellowupgrade = pygame.image.load('yellowupgrade.bmp')
spr_enemy = pygame.image.load('enemy.bmp')
spr_enemy.set_colorkey([255, 255, 255])
spr_slowenemy = pygame.image.load('slowenemy.bmp')
spr_slowenemy.set_colorkey([255, 255, 255])
spr_smallenemy = pygame.image.load('smallenemy.bmp')
spr_smallenemy.set_colorkey([255, 255, 255])
snd_menubeep = pygame.mixer.Sound('menubeep.wav')
snd_rocketfire = pygame.mixer.Sound('rocket1.wav')
snd_rockethit = pygame.mixer.Sound('rocket2.wav')
snd_bulletfire = pygame.mixer.Sound('machinegun.wav')
snd_shotgunfire = pygame.mixer.Sound('shotgun.wav')
snd_bullethit = pygame.mixer.Sound('bullethit.wav')
snd_beamlazer = pygame.mixer.Sound('beamlaser.wav')


global output
output = pygame.Surface([255, 240])


def update():
    pygame.transform.scale(output, cfg_res, screen)
    pygame.display.flip()
    screen.fill([0, 0, 0])
    output.fill([0, 0, 0])
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print "exit button was pressed"
            state = 0
            print state
            pygame.quit()
            #1 / 0 # DIVIDE BY ZERO TO CRASH APPLICATION
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                buttons[0][1] += 1
            elif event.key == pygame.K_DOWN:
                buttons[0][1] -= 1
            elif event.key == pygame.K_RIGHT:
                buttons[0][0] += 1
            elif event.key == pygame.K_LEFT:
                buttons[0][0] -= 1
            elif event.key == pygame.K_z:
                buttons[1] = 1
            elif event.key == pygame.K_x:
                buttons[2] = 1
            elif event.key == pygame.K_RETURN:
                buttons[3] = 1
            elif event.key == pygame.K_RSHIFT:
                buttons[4] = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                buttons[0][1] -= 1
            elif event.key == pygame.K_DOWN:
                buttons[0][1] += 1
            elif event.key == pygame.K_RIGHT:
                buttons[0][0] -= 1
            elif event.key == pygame.K_LEFT:
                buttons[0][0] += 1
            elif event.key == pygame.K_z:
                buttons[1] = 0
            elif event.key == pygame.K_x:
                buttons[2] = 0
    clock.tick(30)

class projectile:
    def update(self):
        
        #checks for collision with player enemy or projectile
        #and returns the id # of the entity collided with
        #for i in ents:
        
        pass
    
class bullet(projectile):
    
    dmg = 3
    
    def __init__(self, position, direction):
        self.pos = position
        self.dir = direction
    
    def update(self):
        self.pos[0] += self.dir[0]
        self.pos[1] += self.dir[1]
        collide = self.projectile.update()
        if collide[0] == 'enemy':
            enemies[collide[1]].health -= dmg
            
            
    
class enemy:
    def __init__(self, sprite, speed, health, weapontype):
        self.sprite = sprite
        self.speed = speed
        self.health = health
        self.weapon = weapontype

class player:
    def __init__(self, startpos, speed, starthealth, startlives):
        self.rect = [startpos[0], startpos[1], 16, 16]
        self.speed = speed
        self.health = starthealth
        self.lives = startlives
        self.bullets = []
    
    def update(self):
        self.rect[0] += buttons[0][0] * self.speed
        self.rect[1] -= buttons[0][1] * self.speed
        
        
        

    def draw(self):
        output.blit(spr_player, self.rect[:2])
        
        
class starfield:
    def __init__(self, num, speed):
        self.speed = speed
        self.stars = []
        for i in range(0, num):
            x = random.randint(0, 255)
            y = random.randint(0, 240)
            self.stars.append([x, y])
    
    def update(self):
        for i in range(0, len(self.stars)):
            if self.stars[i][1] > 241:
                self.stars[i][1] = -2
                self.stars[i][0] = random.randint(0, 255)
            else:
                self.stars[i][1] += self.speed
    
    def draw(self):
        for i in self.stars:
            output.set_at([int(i[0]), int(i[1])], [250, 250, 250]) 
            #could be more efficient


while state != 0:
    if state == 1:
        option = 2
    while state == 1: # --- main menu
        #display logo + legal text
        output.blit(spr_logo, [25, 20])
        output.blit(spr_menutext[0], [8, 210])
        
        #sprite test
        if cfg_debug == 1:
            output.blit(spr_smallenemy, [0, 70])
            output.blit(spr_slowenemy, [8, 70])
            output.blit(spr_enemy, [24, 70])
            
            output.blit(spr_bullet, [0, 180])
            output.blit(spr_bullet, [10, 180])
            output.blit(spr_rocket, [20, 180])
            output.blit(spr_beamlazer, [30, 180])
            
            output.blit(spr_machinegun, [0, 190])
            output.blit(spr_shotgun, [10, 190])
            output.blit(spr_rocketlauncher, [20, 190])
            output.blit(spr_lazergun, [30, 190])
            output.blit(spr_specialgun, [40, 190])
            
            output.blit(spr_yellowupgrade, [0, 200])
            output.blit(spr_redupgrade, [20, 200])
            output.blit(spr_blueupgrade, [30, 200])
            output.blit(spr_greenupgrade, [40, 400])
        
        # display menu text options in correct color
        if option == 2:
            output.blit(spr_menutext[1], [100, 100])
            output.blit(spr_player, [80, 95])
        else:
            output.blit(spr_menutext[2], [100, 100])
        if option == 3:
            output.blit(spr_menutext[3], [100, 115])
            output.blit(spr_player, [80, 110])
        else:
            output.blit(spr_menutext[4], [100, 115])
        if option == 4:
            output.blit(spr_menutext[5], [100, 130])
            output.blit(spr_player, [80, 125])
        else:
            output.blit(spr_menutext[6], [100, 130])
        
        if buttons[4] == 1:
            option += 1
            buttons[4] = 0
        
        if option >= 5:
            option = 2
        
        #change state when "start" is pressed
        if buttons[3] == 1:
            if option == 4:
                state = 0
            else:
                state = option
        
        update()
        
    if state == 2:# --- initialize game
        #player1 = player([127, 200], 3, 10, 3)
        ents.append(player([127, 200], 3, 10, 3))
        stars = starfield(50, 1)
        level = 1
        stage = 0 #stage key:   0 = game start
        timer = 0 #             1 = game running
        #                       2 = boss stage
        #                       3 = level clear
        
    while state == 2: # --- game
        # --- game code
        #player1.update()
        stars.update()
        print ents
        for i in range(0, len(ents)):
            ents[i].update()
        
        
        # --- draw code
        stars.draw()
        
        #player1.draw()
        for i in range(0, len(ents)):
            ents[i].draw()
        
        # --- update
        update()
        
pygame.quit()
    
