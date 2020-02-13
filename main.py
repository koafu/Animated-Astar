import pygame 
from node import Node

def show_node(window, x, y, color, margin):
    '''Draws node in grid'''
    window.fill(color, rect=[(x*c) + margin, (y*c) + margin, c - margin, c - margin])

def recontstruct_path(current):
    '''
    finds path to end node
    '''
    total_path = []
    end = current
    temp = current
    while temp.cameFrom:
        total_path.insert(0,temp.cameFrom)
        temp = temp.cameFrom
    total_path.append(end)
    return total_path

def draw_grid(grid, margin):
    x,y = 0,0
    for cols in grid:
        pygame.draw.line(window, black, (x,0), (x,height), margin)
        for rows in cols:
            pygame.draw.line(window, black, (0,y), (width,y), margin)
        x += c
        y += c

def update_grid(grid_size, open_set, closed_set, margin):
    for y in range(grid_size):
        for x in range(grid_size):
            if grid[y][x].wall:
                show_node(window, x, y, black, margin)
            if grid[y][x] in open_set:
                show_node(window, x, y, green, margin)
            if grid[y][x] in closed_set:
                show_node(window, x, y, red, margin)
    pygame.display.update()

def draw_path(path):
    for y in range(grid_size):
        for x in range(grid_size):
            if grid[y][x] in path:
                show_node(window, x, y, blue, margin)
    pygame.display.update()

white = (255,255,255)
black = (0,0,0)
red =  (255,0,0)
green = (0,255,0)
blue = (44, 130, 230)
yellow = (252,223,3)

pygame.init()

width = 800
height = 800

window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Animated A*')
clock = pygame.time.Clock()
window.fill(white)

grid_size = 50
grid = [[] for n in range(grid_size)]
for y in range(grid_size):
    for x in range(grid_size):
        grid[y].append(Node(x,y))

for y in grid:
    for node in y:
        node.addNeighbours(grid)

margin = 1

start = grid[0][0]
start.wall = False
end = grid[grid_size-1][grid_size-1]
end.wall = False

c = width / grid_size 

draw_grid(grid, margin)
running = True
foundPath = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()

    if foundPath == False: 
        start.g = 0
        start.f = start.heuristic(end)
        open_set = [start]
        closed_set = []
        path = []

        while len(open_set) != 0:
            current = min(open_set, key=lambda x:x.f)

            if current == end:
                print("DONE")
                path = recontstruct_path(current)
                draw_path(path)
                foundPath = True
                break
                
            open_set.remove(current)
            closed_set.append(current)
            for neighbour in current.neighbours:

                if neighbour in closed_set or neighbour.wall == True:
                    continue

                tentative_g = current.g + 1
                if neighbour in open_set:
                    if tentative_g < neighbour.g:
                        neighbour.g = tentative_g
                        neighbour.cameFrom = current
                        neighbour.f = neighbour.g + neighbour.heuristic(end)

                else:
                    neighbour.g = tentative_g
                    open_set.append(neighbour)
                    neighbour.f = neighbour.g + neighbour.heuristic(end)
                    neighbour.cameFrom = current

            update_grid(grid_size, open_set, closed_set, margin)
    # running = False
    pygame.display.update()
    clock.tick(60)
