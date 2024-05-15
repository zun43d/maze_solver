import heapq

def solve_maze(maze):
    start = find_start(maze)
    end = find_end(maze)
    shortest_path = astar(maze, start, end)
    return shortest_path

def find_start(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 'S':
                return (i, j)

def find_end(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 'E':
                return (i, j)

def heuristic(current, end):
    # Manhattan distance heuristic
    return abs(current[0] - end[0]) + abs(current[1] - end[1])

def astar(maze, start, end):
    priority_queue = [(0, start, [])]  # (f-score, current cell, path)
    visited = set()

    while priority_queue:
        _, current, path = heapq.heappop(priority_queue)
        if current == end:
            return path + [current]

        if current in visited:
            continue
        visited.add(current)

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up
        for dx, dy in directions:
            new_x, new_y = current[0] + dx, current[1] + dy
            if (0 <= new_x < len(maze) and 0 <= new_y < len(maze[0]) and
                    maze[new_x][new_y] != '#'):
                new_path = path + [current]
                g_score = len(new_path)  # Cost of reaching this cell
                h_score = heuristic((new_x, new_y), end)
                f_score = g_score + h_score
                heapq.heappush(priority_queue, (f_score, (new_x, new_y), new_path))

    return None
