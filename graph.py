from queue import PriorityQueue

from visualisation_colors import Colors


class Node(Colors):

    def __init__(self, row, col, color) -> None:

        self.row = row
        self.col = col
        self.color = color

    def is_empty(self):
        return self.color == self.EMPTY_COLOR or self.color == self.END_COLOR

    def is_end(self):
        return self.color == self.END_COLOR

    def is_wall(self):
        return self.color == self.WALL_COLOR

    def visit(self):
        if self.color != self.START_COLOR:
            self.color = self.VISITED_COLOR

    def add_to_path(self):
        self.color = self.PATH_COLOR


def reconstructPath(prev, foundNode):
    print(foundNode)
    for k, v in prev.items():
        print(k,v)
    at = (foundNode)
    path = []
    while prev[at]:
        at = prev[at]
        path.append(at)
    return path[::-1]


def bfs(src, grid):
    x1, y1 = src
    width = len(grid[0])
    height = len(grid)

    queue = [(x1, y1)]
    prev = {(x1, y1): None}

    x2, y2 = -1, -1

    visited = set()
    while queue:
        x, y = queue.pop(0)

        if grid[y][x].is_end():
            x2, y2 = x, y
            break

        grid[y][x].visit()  # visualise node as visited

        yield grid  # yield the grid state

        for dx, dy in [[1, 0], [-1, 0], [0, 1], [0, -1]]:  # for x, y pairs in adjacent nodes
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= width or ny < 0 or ny >= height:
                continue

            if grid[ny][nx].is_empty() and ((nx, ny) not in visited):  # if empty
                visited.add((nx, ny))
                queue.append((nx, ny))  # Adds to new (x,y) pair to the stack

                prev[(nx, ny)] = (x, y)  # stores adjacent node and central node in dictionary

    if x2 > -1 and y2 > -1:
        path = reconstructPath(prev, (x2, y2))
        for x, y in path:
            grid[y][x].color = Node.PATH_COLOR
            yield grid


def manhattan_distance(x1, y1, x2, y2):

    return abs(x1-x2) + abs(y1-y2)


def a_star(p1, p2, grid):
    print(f"{p1}->>>{p2}")
    visited_counter = 0

    inf = float("inf")
    width = len(grid[0])
    height = len(grid)

    x1, y1 = p1
    x2, y2 = p2

    distances = [[inf for _ in range(len(grid[0]))] for _ in range(len(grid))]
    distances[y1][x1] = 0

    prev = {(x1, y1): None}

    queue = PriorityQueue()

    # Heuristic, x , y , Distance
    queue.put(
        (manhattan_distance(x1, y1, x2, y2), x1, y1, 0)
    )
    while not queue.empty():

        _, x, y, distance = queue.get()

        if x == x2 and y == y2:
            break

        grid[y][x].visit()
        visited_counter += 1

        yield

        for dx, dy in [[1, 0], [-1, 0], [0, 1], [0, -1]]:  # for x, y pairs in adjacent nodes
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= width or ny < 0 or ny >= height:
                continue

            if grid[ny][nx].is_empty() and distances[ny][nx] == inf:

                manhattan_dist = manhattan_distance(nx, ny, x2, y2)
                queue.put(
                    (manhattan_dist+distance, nx, ny, distance)
                )

            if distances[ny][nx] > distance:
                prev[(nx, ny)] = (x, y)
                distances[ny][nx] = distance

    if (x2, y2) in prev:
        print("finding shortest path")
        for x, y in reconstructPath(prev, (x2, y2)):
            grid[y][x].color = Node.PATH_COLOR
            yield
    yield visited_counter

