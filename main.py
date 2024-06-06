import tkinter as tk
from maze_generator import autogen
from maze_solver import solve_maze

w = 15
h = 15

class MazeGame:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1000x900")  # Set the fixed window size
        self.master.resizable(False, False)  # Disable resizing
        self.main_menu()

    def main_menu(self):
        self.clear_screen()

        title_label = tk.Label(self.master, text="Maze Game", font=("Helvetica", 24))
        title_label.pack(pady=20)

        pvp_button = tk.Button(self.master, text="Player vs Player", font=("Helvetica", 16), command=self.start_pvp)
        pvc_button = tk.Button(self.master, text="Player vs Computer", font=("Helvetica", 16), command=self.start_pvc)
        exit_button = tk.Button(self.master, text="Exit Game", font=("Helvetica", 16), command=self.master.quit)

        pvp_button.pack(pady=10)
        pvc_button.pack(pady=10)
        exit_button.pack(pady=10)

    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def start_pvp(self):
        self.player1_steps = 0
        self.player2_steps = 0
        self.current_player = 1
        self.maze = autogen(w, h)
        self.pvp_mode()

    def start_pvc(self):
        self.player_steps = 0
        self.computer_steps = 0
        self.current_player = 1
        self.maze = autogen(w, h)
        self.pvc_mode()

    def pvp_mode(self):
        self.clear_screen()

        self.step_count = 0
        self.canvas = tk.Canvas(self.master, width=1000, height=900)
        self.canvas.pack()

        self.draw_maze()
        self.player_position = self.find_start_position()
        self.draw_player()

        self.step_label = tk.Label(self.master, text=f"Steps: {self.step_count}")
        self.step_label.pack()

        self.master.bind("<Key>", self.move_player_pvp)
        self.update_player_label()

    def pvc_mode(self):
        self.clear_screen()

        self.step_count = 0
        self.canvas = tk.Canvas(self.master, width=1000, height=900)
        self.canvas.pack()

        self.draw_maze()
        self.player_position = self.find_start_position()
        self.draw_player()

        self.step_label = tk.Label(self.master, text=f"Steps: {self.step_count}")
        self.step_label.pack()

        if self.current_player == 1:
            self.master.bind("<Key>", self.move_player_pvc)
            self.update_player_label()
        else:
            self.auto_solve_computer()

    def update_player_label(self):
        if hasattr(self, 'player_label'):
            self.player_label.destroy()
        self.player_label = tk.Label(self.master, text=f"Player {self.current_player}'s Turn", font=("Helvetica", 18))
        self.player_label.pack()

    def move_player_pvp(self, event):
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
                self.end_turn_pvp()

    def move_player_pvc(self, event):
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
                self.end_turn_pvc()

    def end_turn_pvp(self):
        if self.current_player == 1:
            self.player1_steps = self.step_count
            self.current_player = 2
            self.clear_screen()
            turn_label = tk.Label(self.master, text="Turn for Player 2", font=("Helvetica", 24))
            turn_label.pack(pady=20)
            self.master.after(2000, self.pvp_mode)
        else:
            self.player2_steps = self.step_count
            self.display_winner_pvp()

    def end_turn_pvc(self):
        if self.current_player == 1:
            self.player_steps = self.step_count
            self.current_player = 2
            self.auto_solve_computer()
        else:
            self.computer_steps = self.step_count
            self.display_winner_pvc()

    def auto_solve_computer(self):
        solution_path = solve_maze(self.maze)
        if solution_path:
            self.step_count = len(solution_path)
            self.end_turn_pvc()

    def display_winner_pvp(self):
        self.clear_screen()
        if self.player1_steps < self.player2_steps:
            winner_text = f"Player 1 wins with {self.player1_steps} steps!"
        elif self.player2_steps < self.player1_steps:
            winner_text = f"Player 2 wins with {self.player2_steps} steps!"
        else:
            winner_text = f"It's a tie! Both took {self.player1_steps} steps."

        winner_label = tk.Label(self.master, text=winner_text, font=("Helvetica", 24))
        winner_label.pack(pady=20)

        back_button = tk.Button(self.master, text="Back to Home Screen", font=("Helvetica", 16), command=self.main_menu)
        back_button.pack(pady=20)

    def display_winner_pvc(self):
        self.clear_screen()
        if self.player_steps < self.computer_steps:
            winner_text = f"Player wins with {self.player_steps} steps!"
        elif self.computer_steps < self.player_steps:
            winner_text = f"Computer wins with {self.computer_steps} steps!"
        else:
            winner_text = f"It's a tie! Both took {self.player_steps} steps."

        winner_label = tk.Label(self.master, text=winner_text, font=("Helvetica", 24))
        winner_label.pack(pady=20)

        back_button = tk.Button(self.master, text="Back to Home Screen", font=("Helvetica", 16), command=self.main_menu)
        back_button.pack(pady=20)

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

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Maze Game")
    game = MazeGame(root)
    root.mainloop()
