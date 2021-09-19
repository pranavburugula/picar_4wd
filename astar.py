from queue import PriorityQueue

LEFT_MAX = -4
RIGHT_MAX = 5
UP_MAX = 4
BASE_X = 4
BASE_Y = 4

GRID_ROWS = 5
GRID_COLS = 10

PATH_THRESHOLD = 3

def updateGrid():
    # TODO: Placeholder for actual method
    grid = [[0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,1,1,1,1,1,1,1,1,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0]]

    return grid

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
            if newX >= GRID_COLS or newX < 0 or newY >= GRID_ROWS or newY < 0 or grid[newY][newX] == 1:
                continue

            newNode = Node(curr, (newX, newY))
            if newNode in visited:
                continue

            newNode.g = curr.g+1
            newNode.h = heuristic(newNode.pos, end.pos)
            newNode.f = newNode.g + newNode.h

            q.put((newNode.f, newNode))

def moveOnPath(path, target):
    prev = None
    totalMoves = (0, 0)
    for idx, curr in enumerate(path):
        if idx == PATH_THRESHOLD or prev == target:
            break

        if prev == None:
            prev = curr
            continue
        
        move = (curr[0]-prev[0], curr[1]-prev[1])
        totalMoves = (totalMoves[0]+move[0], totalMoves[1]+move[1])
        # TODO: move the car in the given direction

        prev = curr

    target = (target[0]-totalMoves[0], target[1]-move[1])
    return target

def moveToPoint(x, y):
    while x != 0 and y != 0:
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

        print(x, y, remX, remY)
        base = (BASE_X, BASE_Y)
        while (x, y) != base:
            grid = updateGrid()
            path = search(grid, (BASE_X, BASE_Y), (x, y))
            x, y = moveOnPath(path, (x, y))
            print(path, x, y)

        x = remX
        y = remY

if __name__ == "__main__":
    moveToPoint(1, 5)
