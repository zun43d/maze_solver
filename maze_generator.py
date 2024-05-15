import random

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.walls = [True, True, True, True]  # top, right, bottom, left

def remove_walls(current, next_cell):
    dir_x = current.col - next_cell.col
    dir_y = current.row - next_cell.row

    if dir_x == 1:
        current.walls[3] = False
        next_cell.walls[1] = False
    elif dir_x == -1:
        current.walls[1] = False
        next_cell.walls[3] = False

    if dir_y == 1:
        current.walls[0] = False
        next_cell.walls[2] = False
    elif dir_y == -1:
        current.walls[2] = False
        next_cell.walls[0] = False

def generate_path(grid, start, end):
    path = [start]
    current = start
    while current != end:
        neighbors = []
        row, col = current.row, current.col

        if row > 0 and grid[row - 1][col] not in path:
            neighbors.append(grid[row - 1][col])
        if row < len(grid) - 1 and grid[row + 1][col] not in path:
            neighbors.append(grid[row + 1][col])
        if col > 0 and grid[row][col - 1] not in path:
            neighbors.append(grid[row][col - 1])
        if col < len(grid[0]) - 1 and grid[row][col + 1] not in path:
            neighbors.append(grid[row][col + 1])
        if row > 0 and col > 0 and grid[row - 1][col - 1] not in path:
            neighbors.append(grid[row - 1][col - 1])
        if row > 0 and col < len(grid[0]) - 1 and grid[row - 1][col + 1] not in path:
            neighbors.append(grid[row - 1][col + 1])
        if row < len(grid) - 1 and col > 0 and grid[row + 1][col - 1] not in path:
            neighbors.append(grid[row + 1][col - 1])
        if row < len(grid) - 1 and col < len(grid[0]) - 1 and grid[row + 1][col + 1] not in path:
            neighbors.append(grid[row + 1][col + 1])

        if not neighbors:
            return None
        next_cell = random.choice(neighbors)
        path.append(next_cell)
        current = next_cell

    return path

def generate_maze(size):
    grid = [[Cell(i, j) for j in range(size)] for i in range(size)]
    stack = []
    current = grid[0][0]
    current.visited = True

    while True:
        neighbors = []
        row, col = current.row, current.col

        if row > 0 and not grid[row - 1][col].visited:
            neighbors.append(grid[row - 1][col])
        if col < size - 1 and not grid[row][col + 1].visited:
            neighbors.append(grid[row][col + 1])
        if row < size - 1 and not grid[row + 1][col].visited:
            neighbors.append(grid[row + 1][col])
        if col > 0 and not grid[row][col - 1].visited:
            neighbors.append(grid[row][col - 1])

        if neighbors:
            next_cell = random.choice(neighbors)
            next_cell.visited = True
            stack.append(current)
            remove_walls(current, next_cell)
            current = next_cell
        elif stack:
            current = stack.pop()
        else:
            break

    start_row, start_col = random.randint(0, size - 1), random.randint(0, size - 1)
    end_row, end_col = random.randint(0, size - 1), random.randint(0, size - 1)
    while abs(start_row - end_row) + abs(start_col - end_col) < size // 2:
        end_row, end_col = random.randint(0, size - 1), random.randint(0, size - 1)

    path = generate_path(grid, grid[start_row][start_col], grid[end_row][end_col])

    if path is None:
        return generate_maze(size)

    maze = [['#' if cell.walls[0] else ' ' for cell in row] for row in grid]
    for row in maze:
        row[0] = '#'  # Left border
        row[-1] = '#'  # Right border

    maze[start_row][start_col] = 'S'  # Place 'S' at the starting position
    maze[end_row][end_col] = 'E'      # Place 'E' at the ending position
    for cell in path:
        maze[cell.row][cell.col] = ' '  # Mark path cells as traversable space

    return maze

# Example usage:
maze_size = 10
maze = generate_maze(maze_size)
for row in maze:
    print(''.join(row))
