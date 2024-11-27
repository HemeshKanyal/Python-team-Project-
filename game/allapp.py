import tkinter as tk
from tkinter import PhotoImage
import subprocess

def launch_pygame_game():
    subprocess.Popen(["python", "breakout_game.py"])

def launch_turtle_game():
    subprocess.Popen(["python", "snake_game.py"])

def launch_tkinter_game():
    subprocess.Popen(["python", "escape_the_dungeon_app.py"])

def launch_pygame_game1():
    subprocess.Popen(["python", "tetris.py"])

def launch_new_game():
    subprocess.Popen(["python", "flappy.py"])

def launch_new_game1():
    subprocess.Popen(["python", "tic_tac_toe.py"])

root = tk.Tk()
root.title("Arcadia")
root.state('zoomed')

breakout_image = PhotoImage(file="breakout.png")
snake_game_image = PhotoImage(file="snake_game.png")
escape_the_dungeon_image = PhotoImage(file="escape_the_dungeon.png")
tetris_image = PhotoImage(file="tetris.png")
flappy_image = PhotoImage(file="flappy.png")
tic_tac_toe = PhotoImage(file="tic_tac_toe.png")

button_width = 400
button_height = 400

frame_row1 = tk.Frame(root)
frame_row1.pack(pady=10)

btn_breakout = tk.Button(frame_row1, image=breakout_image, command=launch_pygame_game, width=button_width, height=button_height)
btn_breakout.config(text="breakout", compound="top")

btn_snake = tk.Button(frame_row1, image=snake_game_image, command=launch_turtle_game, width=button_width, height=button_height)
btn_snake.config(text="snake", compound="top")

btn_escape = tk.Button(frame_row1, image=escape_the_dungeon_image, command=launch_tkinter_game, width=button_width, height=button_height)
btn_escape.config(text="escape_the_dungeon", compound="top")

btn_breakout.pack(side="left", padx=20)
btn_snake.pack(side="left", padx=20)
btn_escape.pack(side="left", padx=20)

frame_row2 = tk.Frame(root)
frame_row2.pack(pady=10)

btn_tetris = tk.Button(frame_row2, image=tetris_image, command=launch_pygame_game1, width=button_width, height=button_height)
btn_tetris.config(text="tetris", compound="top")

btn_new_game = tk.Button(frame_row2, image=flappy_image, command=launch_new_game, width=button_width, height=button_height)
btn_new_game.config(text="new_game", compound="top")

btn_new_game_1 = tk.Button(frame_row2, image=tic_tac_toe, command=launch_new_game1, width=button_width, height=button_height)
btn_new_game.config(text="new_game1", compound="top")

btn_tetris.pack(side="left", padx=20)
btn_new_game.pack(side="left", padx=20)
btn_new_game_1.pack(side="left", padx =20)

root.mainloop()
