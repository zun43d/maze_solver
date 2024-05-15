import tkinter as tk
# from maze_generator import generate_maze
from maze_solver import solve_maze

maze = [
    ['#', 'S', '#', '#', '#', '#', '#', '#', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', '#', ' ', '#', ' ', '#', '#'],
    ['#', ' ', ' ', ' ', ' ', '#', ' ', ' ', '#'],
    ['#', '#', ' ', ' ', '#', '#', '#', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', '#', '#', '#', '#', 'E', '#', '#', '#'],
]



maze2 = [
    ['#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', 'S', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', '#', '#', '#', '#', '#', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', '#', '#', '#', '#', '#', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', '#', '#', '#', '#', ' ', '#', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', 'E'],
    ['#', '#', '#', '#', '#', '#', '#', '#'],
]

maze3 = [
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', 'S', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#'],
    ['#', '#', '#', ' ', '#', '#', '#', ' ', '#', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', '#'],
    ['#', '#', '#', ' ', '#', ' ', '#', '#', ' ', '#'],
    ['#', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', '#', '#', '#', '#', '#', ' ', '#'],
    ['#', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', '#', '#', '#', ' ', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#', 'E', '#'],
]


class MazeGame:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=600, height=600)
        self.canvas.pack()
        self.maze = maze  # Auto-generate maze
        self.draw_maze()
        self.player_position = self.find_start_position()
        self.draw_player()

        master.bind("<Key>", self.move_player)

        solve_button = tk.Button(master, text="Auto Solve", command=self.auto_solve)
        solve_button.pack()

    def draw_maze(self):
        for i, row in enumerate(self.maze):
            for j, cell in enumerate(row):
                color = "black" if cell == "#" else "white"
                self.canvas.create_rectangle(j * 60, i * 60, (j + 1) * 60, (i + 1) * 60, fill=color)

    def draw_player(self):
        x, y = self.player_position
        self.canvas.create_oval(y * 60 + 10, x * 60 + 10, (y + 1) * 60 - 10, (x + 1) * 60 - 10, fill="blue")

    def find_start_position(self):
        for i, row in enumerate(self.maze):
            for j, cell in enumerate(row):
                if cell == 'S':
                    return (i, j)
        return None

    def move_player(self, event):
        key = event.keysym
        dx, dy = 0, 0
        if key == "Up":
            dx = -1
        elif key == "Down":
            dx = 1
        elif key == "Left":
            dy = -1
        elif key == "Right":
            dy = 1

        new_x, new_y = self.player_position[0] + dx, self.player_position[1] + dy
        if 0 <= new_x < len(self.maze) and 0 <= new_y < len(self.maze[0]) and self.maze[new_x][new_y] != "#":
            self.player_position = (new_x, new_y)
            self.canvas.delete("player")
            self.draw_player()
            if self.maze[new_x][new_y] == 'E':
                self.show_message("Congratulations! You reached the end of the maze.")

    def auto_solve(self):
        solution = solve_maze(self.maze)
        if solution:
            for x, y in solution:
                self.canvas.create_oval(y * 60 + 20, x * 60 + 20, (y + 1) * 60 - 20, (x + 1) * 60 - 20, fill="green")

    def show_message(self, message):
        self.canvas.create_text(300, 300, text=message, font=("Helvetica", 16), fill="red")

def main():
    root = tk.Tk()
    root.title("Maze Game")
    maze_game = MazeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
