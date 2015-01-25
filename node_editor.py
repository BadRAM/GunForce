import pygame, math

pygame.init()
size = (275, 260)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("movement node test 1")
clock = pygame.time.Clock()
spr_enemy = pygame.image.load('enemy.bmp')
spr_enemy.convert()
spr_enemy.set_colorkey([255, 255, 255])

position = [0, 0]
speed = 1
node = 0
nodes = [[0, 0], [275, 0]]
nodetype = [0, 0]
history = [[0, 0], [0, 0]]
dist = 5


def vectro(origin, destination):
    deltaY = destination[1] - origin[1]
    deltaX = destination[0] - origin[0]
    
    angle = math.atan2(deltaY, deltaX)
    
    length = math.sqrt(deltaX ** 2 + deltaY ** 2)
    
    return [angle, length]


# -------- Main Program Loop -----------
while 1:
    count = 0
    # --- Game logic should go here
    
    if nodetype[node] == 1:
        
        distance = vectro(nodes[node - 1], nodes[node + 1])[1]
        remdist = vectro(position, nodes[node + 1])[1]
        rotation = remdist / distance - 0.1
        
        target = vectro(nodes[node + 1], nodes[node])
        
        x = math.cos(target[0]) * target[1] * rotation
        y = math.sin(target[0]) * target[1] * rotation
        
        x += nodes[node + 1][0]
        y += nodes[node + 1][1]
        
        pygame.draw.circle(screen, [0, 200, 255], (int(x), int(y)), 10)
        
        angle = vectro(position, [x, y])
        finalangle = angle[0]
        if position[0] < nodes[node+1][0] + dist and position[0] > nodes[node+1][0] - dist:
            if position[1] < nodes[node+1][1] + dist and position[1] > nodes[node+1][1] - dist:
                node += 1

    else:
        angle = vectro(position, nodes[node])
        
        finalangle = angle[0]
        
        if position[0] < nodes[node][0] + dist and position[0] > nodes[node][0] - dist:
            if position[1] < nodes[node][1] + dist and position[1] > nodes[node][1] - dist:
                node += 1
    
    xmove = math.cos(finalangle) * speed
    ymove = math.sin(finalangle) * speed
    
    position[0] += xmove
    position[1] += ymove

    history.append(position[:])
    
    if node == len(nodes):
        node = 0
    
    
    # --- Drawing code should go here
    pygame.draw.rect(screen, [255, 255, 255], [10, 10, 255, 240], 1)
    pygame.draw.lines(screen, [100, 100, 100], False, nodes)
    for i in nodes:
        if nodetype[count] == 1:
            pygame.draw.circle(screen, [0,0,200], i, 10)
        else:
            pygame.draw.circle(screen, [100,0,100], i, 10)
        count += 1
    pygame.draw.line(screen, [200, 0, 0], position, nodes[node])
    pygame.draw.lines(screen, [100, 255, 100], False, history, 3)
    #pygame.draw.circle(screen, [0, 200, 0], (int(position[0]), int(position[1])), 15)
    tempspr = pygame.transform.rotate(spr_enemy, math.degrees(finalangle))
    screen.blit(tempspr, (int(position[0]), int(position[1])))
    pygame.draw.circle(screen, [100, 200, 255], nodes[node], 5)
    
    
    pygame.display.flip() # <---FLIP
    screen.fill([0, 0, 0])
    
    # --- Limit to 60 frames per second
    clock.tick(60)
	
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            buttons = pygame.mouse.get_pressed()
            nodes.append(pygame.mouse.get_pos())
            if buttons[0] == 1:
                nodetype.append(0)
            else:
                nodetype.append(1)

pygame.quit()
