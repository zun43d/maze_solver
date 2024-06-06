import tkinter as tk
from maze_generator import autogen
from maze_solver import solve_maze

w = 15
h = 15

class MazeGame:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=1000, height=900)
        self.canvas.pack()
        self.maze = autogen(w, h)  # Auto-generate maze

        self.step_count = 0
        self.step_label = tk.Label(master, text=f"Steps: {self.step_count}")
        self.step_label.pack()

        self.draw_maze()
        self.player_position = self.find_start_position()
        self.draw_player()

        master.bind("<Key>", self.move_player)

        solve_button = tk.Button(master, text="Auto Solve", command=self.auto_solve)
        regenerate_btn = tk.Button(master, text="Re-Generate", command=self.regen)
        solve_button.pack()
        regenerate_btn.pack()
       
    def regen(self):
        self.maze = autogen(w,h)
        self.draw_maze()
        self.player_position = self.find_start_position()
        self.draw_player()
        
        # Reset step count
        self.step_count = 0
        self.step_label.config(text=f"Steps: {self.step_count}")
    
    def draw_maze(self):
        for i, row in enumerate(self.maze):
            for j, cell in enumerate(row):
                color = "black" if cell == "#" else "white"
                self.canvas.create_rectangle(j * 30, i * 30, (j + 1) * 30, (i + 1) * 30, fill=color)

    def draw_player(self):
        x, y = self.player_position
        self.canvas.create_oval(y * 30 + 10, x * 30 + 10, (y + 1) * 30 - 10, (x + 1) * 30 - 10, fill="blue")

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
        if 0 <= new_x < len(self.maze) and 0 <= new_y < len(self.maze[0]) and self.maze[new_x][new_y] != '#':
            # Clear the previous position
            x, y = self.player_position
            self.canvas.create_rectangle(y * 30, x * 30, (y + 1) * 30, (x + 1) * 30, fill="white")
            
            # Update the player's position
            self.player_position = (new_x, new_y)
            
            # Draw the player at the new position
            self.draw_player()

            # Increment step count and update label
            self.step_count += 1
            self.step_label.config(text=f"Steps: {self.step_count}")
            
            # Check if the player has reached the end
            if self.maze[new_x][new_y] == 'E':
                self.show_win_message()

    def auto_solve(self):
        solution = solve_maze(self.maze)
        if solution:
            for x, y in solution:
                self.canvas.create_oval(y * 30 + 20, x * 30 + 20, (y + 1) * 30 - 20, (x + 1) * 30 - 20, fill="green")

    def show_win_message(self):
        self.canvas.create_text(500, 450, text="Congratualtions! Maze was Solved!", font=("Helvetica", 24), fill="red")

def main():
    root = tk.Tk()
    root.title("Maze Game")
    maze_game = MazeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
