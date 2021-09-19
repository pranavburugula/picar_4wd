from queue import PriorityQueue

LEFT_MAX = -99
RIGHT_MAX = 100
UP_MAX = 99
BASE_X = 99
BASE_Y = 99

GRID_ROWS = 100
GRID_COLS = 200

def updateGrid():
    # Placeholder for actual method
    pass

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
        
def moveToPoint(x, y):
    while x != 0 and y != 0:
        grid = updateGrid()

        remX, remY = 0, 0
        if x < LEFT_MAX:
            remX = x + LEFT_MAX
            x = LEFT_MAX
        elif x > RIGHT_MAX:
            remX = x-RIGHT_MAX
            x = RIGHT_MAX
        
        x = BASE_X+x

        if y < 0:
            remY = -y
            # turn around and call function again
        elif y > UP_MAX:
            remY = y-UP_MAX
            y = UP_MAX
        
        y = BASE_Y-y

        path = search(grid, (BASE_X, BASE_Y), (x, y))
        # TODO: move on path THRESHOLD steps at a time

        x = remX
        y = remY

def getPath(end, grid):
    path = []
    
    curr = end
    while curr != None:
        path.append(curr.position)
        current = current.parent

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

    while len(q) > 0:
        f, curr = q.get()

        visited.add(curr)

        if curr == end:
            return getPath(curr, grid)

        for pos in adj:
            newX, newY = curr.position[0] + pos[0], curr.position[1] + pos[1]

            if newX >= GRID_COLS or newX < 0 or newY >= GRID_ROWS or newY < 0 or grid[newX][newY] == 1:
                continue

            newNode = Node(curr, (newX, newY))
            if newNode in visited:
                continue

            newNode.g = curr.g + 1
            newNode.h = heuristic(newNode.position, end.position)
            newNode.f = newNode.g + newNode.h

            q.put((newNode.f, newNode))
