import pygame
import heapq
import random
import time
from collections import deque

pygame.init()


WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver: Search vs Optimization")

font = pygame.font.SysFont("Arial", 20)

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,150,255)
YELLOW = (255,255,0)

dirs = [(1,0),(-1,0),(0,1),(0,-1)]
# Stats
time_taken = 0
nodes_visited = 0
algo_name = ""

def generate_maze():
    maze = [[0]*COLS for _ in range(ROWS)]
    for i in range(ROWS):
        for j in range(COLS):
            if random.random() < 0.25:
                maze[i][j] = 1
    maze[0][0] = 0
    maze[ROWS-1][COLS-1] = 0
    return maze

maze = generate_maze()
start = (0,0)
goal = (ROWS-1, COLS-1)

def draw(grid, visited=set(), path=[]):
    screen.fill(WHITE)

    for i in range(ROWS):
        for j in range(COLS):
            x, y = j*CELL, i*CELL

            if grid[i][j] == 1:
                pygame.draw.rect(screen, BLACK, (x,y,CELL,CELL))
            elif (i,j) in visited:
                pygame.draw.rect(screen, BLUE, (x,y,CELL,CELL))
            elif (i,j) in path:
                pygame.draw.rect(screen, YELLOW, (x,y,CELL,CELL))

            pygame.draw.rect(screen, (200,200,200), (x,y,CELL,CELL), 1)

    pygame.draw.rect(screen, GREEN, (start[1]*CELL, start[0]*CELL, CELL, CELL))
    pygame.draw.rect(screen, RED, (goal[1]*CELL, goal[0]*CELL, CELL, CELL))

    info1 = font.render(f"Algorithm: {algo_name}", True, (0,0,0))
    info2 = font.render(f"Time: {time_taken:.4f} sec", True, (0,0,0))
    info3 = font.render(f"Nodes: {nodes_visited}", True, (0,0,0))

    screen.blit(info1, (10,10))
    screen.blit(info2, (10,35))
    screen.blit(info3, (10,60))

    pygame.display.update()
def bfs():
    global time_taken, nodes_visited, algo_name

    algo_name = "BFS"
    start_time = time.time()

    q = deque([start])
    parent = {}
    visited = set([start])

    while q:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return None

        x,y = q.popleft()

        if (x,y) == goal:
            break

        for dx,dy in dirs:
            nx,ny = x+dx,y+dy
            if 0<=nx<ROWS and 0<=ny<COLS and maze[nx][ny]==0 and (nx,ny) not in visited:
                visited.add((nx,ny))
                parent[(nx,ny)] = (x,y)
                q.append((nx,ny))

        nodes_visited = len(visited)
        time_taken = time.time() - start_time
        draw(maze, visited)
        pygame.time.delay(10)

    return parent

def dfs():
    global time_taken, nodes_visited, algo_name

    algo_name = "DFS"
    start_time = time.time()

    stack = [start]
    parent = {}
    visited = set([start])

    while stack:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return None

        x,y = stack.pop()

        if (x,y) == goal:
            break

        for dx,dy in dirs:
            nx,ny = x+dx,y+dy
            if 0<=nx<ROWS and 0<=ny<COLS and maze[nx][ny]==0 and (nx,ny) not in visited:
                visited.add((nx,ny))
                parent[(nx,ny)] = (x,y)
                stack.append((nx,ny))

        nodes_visited = len(visited)
        time_taken = time.time() - start_time
        draw(maze, visited)
        pygame.time.delay(10)

    return parent
def heuristic(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar():
    global time_taken, nodes_visited, algo_name

    algo_name = "A*"
    start_time = time.time()

    pq = [(0,start)]
    g = {start:0}
    parent = {}
    visited = set()

    while pq:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return None

        _, (x,y) = heapq.heappop(pq)

        if (x,y) in visited:
            continue

        visited.add((x,y))

        if (x,y) == goal:
            break

        for dx,dy in dirs:
            nx,ny = x+dx,y+dy
            if 0<=nx<ROWS and 0<=ny<COLS and maze[nx][ny]==0:
                new_g = g[(x,y)] + 1
                if (nx,ny) not in g or new_g < g[(nx,ny)]:
                    g[(nx,ny)] = new_g
                    f = new_g + heuristic((nx,ny), goal)
                    parent[(nx,ny)] = (x,y)
                    heapq.heappush(pq,(f,(nx,ny)))

        nodes_visited = len(visited)
        time_taken = time.time() - start_time
        draw(maze, visited)
        pygame.time.delay(10)

    return parent

#path
def build_path(parent):
    path = []
    cur = goal
    while cur in parent:
        path.append(cur)
        cur = parent[cur]
    path.append(start)
    return path[::-1]

def animate_path(path):
    for i in range(len(path)):
        draw(maze, path=path[:i])
        pygame.time.delay(30)

#  genetic mutation
def mutate(path):
    if len(path) < 3:
        return path

    path = path.copy()
    idx = random.randint(1, len(path)-2)

    x,y = path[idx]
    dx,dy = random.choice(dirs)
    nx,ny = x+dx,y+dy

    if 0<=nx<ROWS and 0<=ny<COLS and maze[nx][ny]==0:
        path[idx] = (nx,ny)

    return path

def fitness(path):
    return len(path) + heuristic(path[-1], goal)

def optimize(path, iterations=100):
    best = path
    best_fit = fitness(best)

    for _ in range(iterations):
        new_path = mutate(best)
        fit = fitness(new_path)

        if fit < best_fit:
            best = new_path
            best_fit = fit

    return best

running = True

while running:
    draw(maze)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.KEYDOWN:

            # BFS 
            if e.key == pygame.K_b:
                res = bfs()
                if res:
                    path = build_path(res)
                    opt = optimize(path)
                    animate_path(opt)

            # DFS 
            if e.key == pygame.K_d:
                res = dfs()
                if res:
                    path = build_path(res)
                    opt = optimize(path)
                    animate_path(opt)

            # A* 
            if e.key == pygame.K_a:
                res = astar()
                if res:
                    path = build_path(res)
                    opt = optimize(path)
                    animate_path(opt)

            # Regenerate maze
            if e.key == pygame.K_r:
                maze = generate_maze()

pygame.quit()