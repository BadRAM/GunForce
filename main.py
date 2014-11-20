import pygame, random

#button state variable, order: axes, A(z) B(x) START(enter) SELECT(shift)
#SELECT and START cannot be held
global buttons
buttons = [[0, 0], 0, 0, 0, 0]
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mixer.init(44100, -16, 1, 512)
pygame.font.init()
text = pygame.font.Font('PressStart.ttf', 8)
clock = pygame.time.Clock()

global state
state = 1

global score
score = 0

global ents
ents = []

global dest
dest = []

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
spr_text = [
text.render('TM 2014 Corrupt Memory studios', 0, [250, 250, 250]),
text.render('Start', 0, [250, 250, 250]),
text.render('Start', 0, [100, 100, 100]),
text.render('Highscores', 0, [250, 250, 250]),
text.render('Highscores', 0, [100, 100, 100]),
text.render('Quit', 0, [250, 250, 250]),
text.render('Quit', 0, [100, 100, 100]),
text.render('Score:', 0, [250, 250, 250]),
text.render('Lives:', 0, [250, 250, 250]),
text.render('Hull:', 0, [250, 250, 250]),
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
spr_specialbullet = pygame.image.load('wavepulse.bmp')
spr_specialbullet.set_colorkey([255, 255, 255])
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
#snd_playerhit = pygame.mixer.Sound('playerhit.wav') <-- make playerhit.wav


global output
output = pygame.Surface([255, 240])

def offset(number, pos):
    #takes the indice number of a player weapon and generates offset,
    #then applies offset to pos
    finaloffset = [0, 8]
    if number / 2 == number / 2.0:
        finaloffset[0] = number * -3
    else:
        finaloffset[0] = 15 + (number * 3)
    pos[0] += finaloffset[0]
    pos[1] += finaloffset[1]
    return pos
    
    
def padnumber(number, length):
    #pads a number with zeroes. 
    #usage: padnumber(1234, 8) ---> "00001234"
    number = str(number)
    while len(number) < length:
        number = '0' + number
    if len(number) == length:
        return number
    else:
        print 'padding failed'


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
    clock.tick(60)


class projectile:
    def update(self, entnum, rect):
        output = []
        for i in ents:
            if i != ents[entnum]:
                if i.rect[0] + i.rect[2] > rect[0]:
                    if i.rect[0] < rect[0] + rect[2]:
                        if i.rect[1] + i.rect[3] > rect[1]:
                            if i.rect[1] < rect[1] + rect[3]:
                                try:
                                    output.append([i.ent_type, i.entnum])
                                except:
                                    print "failed to get id from collision"
        return output
        #checks for collision with player enemy or projectile
        #and returns the id # of the entity collided with
        #for i in ents:


class shotgun:
    
    heat = 0
    cooldown = 60
    
    def fire(self, pos):
        if self.heat <= 0:
            snd_shotgunfire.play()
            ents.append(bullet(pos, [-0.5, -1.2], 1))
            ents.append(bullet(pos, [0, -1.3], 1))
            ents.append(bullet(pos, [0.5, -1.2], 1))
            self.heat = self.cooldown
            
    def draw(self, pos):
        output.blit(spr_shotgun, pos)


class machinegun:
    
    heat = 0
    cooldown = 10
    
    def fire(self, pos):
        if self.heat <= 0:
            ents.append(bullet(pos, [0, -2], 1))
            self.heat = self.cooldown
            
    def draw(self, pos):
        output.blit(spr_machinegun, pos)
        
        
class rocketlauncher:
    
    heat = 0
    cooldown = 60
    
    def fire(self, pos):
        if self.heat <= 0:
            snd_rocketfire.play()
            ents.append(rocket(pos))
            self.heat = self.cooldown
            
    def draw(self, pos):
        output.blit(spr_rocketlauncher, pos)
        
        
class specialgun:
    
    heat = 0
    cooldown = 30
    
    def fire(self, pos):
        if self.heat <= 0:
            outpos = [pos[0] - 2, pos[1]]
            ents.append(specialbullet(outpos))
            self.heat = self.cooldown
            
    def draw(self, pos):
        output.blit(spr_specialgun, pos)
        
        
class valvegun:
    
    heat = 0
    cooldown = 0
    
    def fire(self, pos):
        if self.heat <= 0:
            direction = [random.randint(-3, 3), random.randint(-3, -1)]
            ents.append(bullet(pos, direction, 1))
            self.heat = self.cooldown
            
    def draw(self, pos):
        output.blit(spr_shotgun, pos)


class bullet(projectile):
    
    ent_type = "bullet"
    dmg = 3
    
    def __init__(self, pos, direction, friendly):
        self.rect = [pos[0], pos[1], 4, 4]
        self.dir = direction
        self.friendly = friendly
    
    def pre_update(self, entnum):
        self.entnum = entnum
        
    def update(self):
        self.rect[0] += self.dir[0]
        self.rect[1] += self.dir[1]
        
        collide = projectile.update(self, self.entnum, self.rect)
        if self.friendly:
            for i in collide:
                if i[0] == "enemy":
                    ents[i[1]].health -= self.dmg
                    snd_bullethit.play()
                    dest.append(self.entnum)
        elif not self.friendly:
            for i in collide:
                if i[0] == "player":
                    ents[i[1]].health -= self.dmg
                    dest.append(self.entnum)
        
        if self.rect[1] < -10:
            dest.append(self.entnum)
        elif self.rect[1] > 260:
            dest.append(self.entnum)
        elif self.rect[0] < -10:
            dest.append(self.entnum)
        elif self.rect[0] > 190:
            dest.append(self.entnum)
            
    def draw(self):
        output.blit(spr_bullet, self.rect[:2])
            
           
class rocket(projectile):
     
    ent_type = "rocket"
    dmg = 10
    speed = 0
    
    def __init__(self, pos):
        self.rect = [pos[0], pos[1], 4, 8]
    
    def pre_update(self, entnum):
        self.entnum = entnum
        
    def update(self):
        self.rect[1] -= self.speed
        self.speed += 0.1
        if self.speed > 3:
            self.speed = 3
        
        collide = projectile.update(self, self.entnum, self.rect)
        for i in collide:
            if i[0] == "enemy":
                ents[i[1]].health -= self.dmg
                snd_rockethit.play()
                dest.append(self.entnum)
    
        if self.rect[1] < -10:
            dest.append(self.entnum)
            
    def draw(self):
        output.blit(spr_rocket, self.rect[:2])
        
        
class specialbullet(projectile):
     
    ent_type = "specialbullet"
    dmg = 0
    
    def __init__(self, pos):
        self.rect = [pos[0], pos[1], 8, 4]
    
    def pre_update(self, entnum):
        self.entnum = entnum
        
    def update(self):
        self.rect[1] -= 2
        
        collide = projectile.update(self, self.entnum, self.rect)
        for i in collide:
            if i[0] == "bullet":
                if ents[i[1]].friendly == 0:
                    dest.append(i[1])
                    dest.append(self.entnum)
    
        if self.rect[1] < -10:
            dest.append(self.entnum)
            
    def draw(self):
        output.blit(spr_specialbullet, self.rect[:2])
    
    
class enemy:
    
    ent_type = "enemy"
    
    def __init__(self, rect, sprite, speed, health, weapontype, scorebonus):
        self.rect = rect
        self.sprite = sprite
        self.speed = speed
        self.health = health
        self.weapon = weapontype
        self.score = scorebonus
        self.heat = 60
        
    def fire(self):
        if self.heat == 0:
            if self.weapon == "gun":
                rect = self.rect
                pos = [rect[0] + (rect[2] / 2 - 2), rect[1] + rect[3]]
                ents.append(bullet(pos, [0, 2], 0))
                self.heat = 120
        else:
            self.heat -= 1
        
    def pre_update(self, entnum):
        self.entnum = entnum
        
    def update(self):
        self.rect[1] += self.speed
        self.fire()
        if self.health <= 0:
            #score += self.score
            dest.append(self.entnum)
        elif self.rect[1] > 260:
            dest.append(self.entnum)
            
    def draw(self):
        output.blit(self.sprite, self.rect[:2])


class player:
    
    ent_type = "player"
    heat = 0
    weapons = [
    specialgun(), specialgun(),
    rocketlauncher(), rocketlauncher(),
    shotgun(), shotgun(),
    machinegun(), machinegun()]
    
    def __init__(self, startpos, speed, starthealth, startlives):
        self.rect = [startpos[0], startpos[1], 16, 16]
        self.speed = speed
        self.health = starthealth
        self.lives = startlives
        self.bullets = []
        
    def pre_update(self, entnum):
        self.entnum = entnum
        
    def update(self):
        self.rect[0] += buttons[0][0] * self.speed
        self.rect[1] -= buttons[0][1] * self.speed
        if self.rect[0] < 0:
            self.rect[0] = 0
        if self.rect[0] > 172:
            self.rect[0] = 172
        if self.rect[1] < 0:
            self.rect[1] = 0
        if self.rect[1] > 224:
            self.rect[1] = 224
        
        if buttons[1] == 1:
            for i in range(0, len(self.weapons)):
                self.weapons[i].fire(offset(i + 1, self.rect[:2]))
            if self.heat == 0:
                snd_bulletfire.play()
                ents.append(bullet([self.rect[0]+6, self.rect[1]], [0,-2], 1))
                self.heat = 10
        
        for i in range(0, len(self.weapons)):
            self.weapons[i].heat -= 1
            
        if self.heat > 0:
            self.heat -= 1
        
    def draw(self):
        output.blit(spr_player, self.rect[:2])
        for i in range(0, len(self.weapons)):
            self.weapons[i].draw(offset(i + 1, self.rect[:2]))

        
        
        
class starfield:
    def __init__(self, num, speed):
        self.speed = speed
        self.stars = []
        for i in range(0, num):
            x = random.randint(0, 188)
            y = random.randint(0, 240)
            self.stars.append([x, y])
    
    def update(self):
        for i in range(0, len(self.stars)):
            if self.stars[i][1] > 241:
                self.stars[i][1] = -2
                self.stars[i][0] = random.randint(0, 188)
            else:
                self.stars[i][1] += self.speed
    
    def draw(self):
        for i in self.stars:
            output.set_at([int(i[0]), int(i[1])], [250, 250, 250])
            #could be more efficient, may cause slowdowns

def smallenemy(pos):
    return enemy([pos[0],pos[1],8,8], spr_smallenemy, 1, 5, "gun", 100)

while state != 0:
    if state == 1:
        option = 2
    while state == 1: # --- main menu
        #display logo + false legal text
        output.blit(spr_logo, [25, 20])
        output.blit(spr_text[0], [8, 210])
        
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
            output.blit(spr_text[1], [100, 100])
            output.blit(spr_player, [80, 95])
        else:
            output.blit(spr_text[2], [100, 100])
        if option == 3:
            output.blit(spr_text[3], [100, 115])
            output.blit(spr_player, [80, 110])
        else:
            output.blit(spr_text[4], [100, 115])
        if option == 4:
            output.blit(spr_text[5], [100, 130])
            output.blit(spr_player, [80, 125])
        else:
            output.blit(spr_text[6], [100, 130])
        
        if buttons[4] == 1:
            option += 1
            buttons[4] = 0
            snd_menubeep.play()
        
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
        ents = [player([100, 200], 1, 20, 3)]
        stars = starfield(50, 1)
        level = 1
        stage = 0 #stage key:   0 = game start
        timer = 0 #             1 = game running
        #                       2 = boss stage
        #                       3 = level clear
        
        #if cfg_debug == 1:
        #    ents.append(smallenemy([100, 0]))
        
    while state == 2: # --- game
        # --- game code
        
        if random.randint(1, 100) == 50:
            ents.append(smallenemy([random.randint(2, 176), -10]))
            
        for i in range(0, len(ents)):
            ents[i].pre_update(i)
        
        stars.update()
        print len(ents)
        for i in range(0, len(ents)):
            ents[i].update()
            
        dest = list(set(dest)) #remove dupes
        dest.sort(reverse = True)
        for i in range(0, len(dest)):
            if ents[dest[0]].ent_type == "enemy":
                score += ents[dest[0]].score
            ents.pop(dest[0])
            dest.pop(0)
        
        # --- draw code
        stars.draw()
        
        for i in range(0, len(ents)):
            ents[i].draw()
        
        pygame.draw.rect(output, [50, 50, 50], [188, 0, 70, 240])
        scoretext = text.render(padnumber(score, 8), 0, [250, 250, 250])
        output.blit(scoretext, [190, 10])
        output.blit(spr_text[9], [190, 30])
        healthtext = text.render(str(ents[0].health), 0, [250, 250, 250])
        output.blit(healthtext, [230, 40])
        frames = text.render(str(clock.get_fps()), 0, [250, 250, 250])
        output.blit(frames, [200, 100])
        
        # --- update
        update()
        
pygame.quit()