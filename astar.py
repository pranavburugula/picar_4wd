from queue import PriorityQueue
from car import Car

LEFT_MAX = -100
RIGHT_MAX = 99
UP_MAX = 99
BASE_X = 100
BASE_Y = 99

GRID_ROWS = 100
GRID_COLS = 200

PATH_THRESHOLD = 5


class Node:
    def __init__(self, parent=None, pos=None):
        self.parent = parent
        self.pos = pos

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        if other == None:
            return False
        return self.pos == other.pos

    def __hash__(self):
        return hash(self.pos)
    
    def __lt__(self, other):
        if other == None:
            return False
        return self.f < other.f

def getPath(end, grid):
    path = []
    
    curr = end
    while curr != None:
        path.append(curr.pos)
        curr = curr.parent

    path.reverse()
    return path

def heuristic(curr, end):
    return abs(curr[0]-end[0])+abs(curr[1]-end[1])

def search(grid, start, end):
    start = Node(None, tuple(start))
    start.g = start.h = start.f = 0
    end = Node(None, tuple(end))
    end.g = end.h = end.f = 0

    q = PriorityQueue()
    visited = set() 
    
    q.put((start.f, start))

    adj = [[-1, 0],[0, -1],[1, 0],[0, 1]]

    while not q.empty():
        f, curr = q.get()

        visited.add(curr)

        if curr == end:
            return getPath(curr, grid)

        for pos in adj:
            newX, newY = curr.pos[0] + pos[0], curr.pos[1] + pos[1]
            # print("newX={x}, newY={y}".format(x = newX, y = newY))
            if newX >= GRID_COLS or newX < 0 or newY >= GRID_ROWS or newY < 0 or grid[newY][newX] == 1:
                continue

            newNode = Node(curr, (newX, newY))
            if newNode in visited:
                continue

            newNode.g = curr.g+1
            newNode.h = heuristic(newNode.pos, end.pos)
            newNode.f = newNode.g + newNode.h

            q.put((newNode.f, newNode))

def moveOnPath(path, target, car):
    prev = None
    totalMoves = (0, 0)
    if path is None:
        return None
    for idx, curr in enumerate(path):
        if idx == PATH_THRESHOLD or prev == target:
            break

        if prev == None:
            prev = curr
            continue
        
        move = (curr[0]-prev[0], curr[1]-prev[1])
        totalMoves = (totalMoves[0]+move[0], totalMoves[1]+move[1])
        # TODO: move the car in the given direction
        if move[0] == -1:       # left
            car.set_orientation(180, 2)
            car.move_distance(1, 2)
        elif move[0] == 1:      # right
            car.set_orientation(0, 2)
            car.move_distance(1, 2)
        elif move[1] == 1:     # down
            car.set_orientation(270, 2)
            car.move_distance(1, 2)
        elif move[1] == -1:      # up
            car.set_orientation(90, 2)
            car.move_distance(1, 2)
        prev = curr

    # target = (target[0]-totalMoves[0], target[1]-move[1])
    return totalMoves

def moveToPoint(x, y, car):
    while x != 0 or y != 0:
        remX, remY = 0, 0
        if x < LEFT_MAX:
            remX = x + LEFT_MAX
            x = LEFT_MAX
        elif x > RIGHT_MAX:
            remX = x-RIGHT_MAX
            x = RIGHT_MAX
        
        x = BASE_X+x

        if y < 0:
            y = -y
            x = -x
            # TODO: make 180 turn and continue
        elif y > UP_MAX:
            remY = y-UP_MAX
            y = UP_MAX

        y = BASE_Y-y

        # print(x, y, remX, remY)
        base = (int(car.get_x()), int(car.get_y()))
        moves_made = (0,0)
        while (x,y) != base:
            car.update_map()
            grid = car.get_env_grid()
            path = search(grid, base, (x, y))
            moves_made = moveOnPath(path, (x, y), car)
            
            base = (base[0]+moves_made[0], base[1]+moves_made[1])
            print("path = {p}, x = {x}, y = {y}, base = ({b_x}, {b_y})".format(p = path, x = x, y = y, b_x = base[0], b_y = base[1]))

        x = remX
        y = remY

if __name__ == "__main__":
    car = Car()
    moveToPoint(0, 20, car)
