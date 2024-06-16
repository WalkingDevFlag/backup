# pathfinding.py

from numpy import sqrt

def get_path(food1, snake1, grid):
    for s in snake1:
        s.camefrom = []
    openset = [snake1[-1]]
    closedset = []
    dir_array1 = []
    while True:
        current1 = min(openset, key=lambda x: x.f)
        openset = [openset[i] for i in range(len(openset)) if not openset[i] == current1]
        closedset.append(current1)
        for neighbor in current1.neighbors:
            if neighbor not in closedset and not neighbor.obstrucle and neighbor not in snake1:
                tempg = neighbor.g + 1
                if neighbor in openset:
                    if tempg < neighbor.g:
                        neighbor.g = tempg
                else:
                    neighbor.g = tempg
                    openset.append(neighbor)
                neighbor.h = sqrt((neighbor.x - food1.x) ** 2 + (neighbor.y - food1.y) ** 2)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.camefrom = current1
        if current1 == food1:
            break
    while current1.camefrom:
        if current1.x == current1.camefrom.x and current1.y < current1.camefrom.y:
            dir_array1.append(2)  # down
        elif current1.x == current1.camefrom.x and current1.y > current1.camefrom.y:
            dir_array1.append(0)  # up
        elif current1.x < current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(3)  # left
        elif current1.x > current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(1)  # right
        current1 = current1.camefrom
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j].camefrom = []
            grid[i][j].f = 0
            grid[i][j].h = 0
            grid[i][j].g = 0
            grid[i][j].obstrucle = False
    return dir_array1

def draw_path(snake, dir_array, grid, screen, wr, hr):
    path = []
    current = snake[-1]
    for direction in reversed(dir_array):
        if direction == 0:  # down
            next_spot = grid[current.x][current.y + 1]
        elif direction == 1:  # right
            next_spot = grid[current.x + 1][current.y]
        elif direction == 2:  # up
            next_spot = grid[current.x][current.y - 1]
        elif direction == 3:  # left
            next_spot = grid[current.x - 1][current.y]
        path.append(next_spot)
        current = next_spot
    
    for i in range(len(path) - 1):
        start_pos = (path[i].y * wr + wr / 2, path[i].x * hr + hr / 2)
        end_pos = (path[i + 1].y * wr + wr / 2, path[i + 1].x * hr + hr / 2)
        pygame.draw.line(screen, (255, 0, 0), start_pos, end_pos, 2)
