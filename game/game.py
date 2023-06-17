from tkinter import *
from time import sleep
from random import randint
import pygame

# Opens Window
window = Tk()
window.title("Tetris")
cvs = Canvas(window, height = 800, width = 390, bg = "black")
cvs.pack()

width = 14
height = 22

block_width = 26
block_height = 26
block_gap = 2

block = []
block_value = []
 
# Calculates the space within the grid
for i in range(width):
    block.append([])
    block_value.append([])
    for j in range(height):
        x = i * (block_width + block_gap)
        y = j * (block_height + block_gap)
        if i == 0 or i == width - 1 or j == 0 or j == height - 1:
            value = 1
            f_color = "black"
        else:
            value = 0
            f_color = "white"
        block_id = cvs.create_rectangle(x, y, x + block_width, y + block_height, outline = "black", fill = f_color )
        block[i].append(block_id)
        block_value[i].append(value)
        
square = [[1, 1], [1, 2], [2, 1], [2, 2]]
straight = [[1,0], [1, 1], [1, 2], [1, 3], [0, 1], [1,1], [2, 1], [3,1]]
T_shape = [[0, 1], [1, 0], [1, 1], [1, 2], [0, 1], [1, 1], [1, 2], [2, 1], [1, 0], [1, 1], [1, 2], [2, 1], [0, 1], [1, 0], [1, 1], [2, 1]]
right_L = [[1, 0], [1, 1], [1, 2], [2, 2], [1, 1], [2, 1], [3, 1], [1, 2], [1, 1], [2, 1], [2, 2], [2, 3], [2, 1], [0, 2], [1, 2], [2, 2]]

shapes = [square, straight, T_shape, right_L]

pos_x = 5
pos_y = 0
shape_index = 0
rotation_index = 0
score = 0
score_text = cvs.create_text(100, 700, text = "Score: 0", font = ("Helvetica", 20), fill = "white" )

lose = False
colors = ["white", 'red', 'purple']

def can_move(move_x, move_y):
    global pos_x, pos_y, shape_index, rotation_index
    shape = shapes[shape_index]
    for i in range(rotation_index, rotation_index + 4):
        x = shape[i][0] + pos_x + move_x
        y = shape[i][0] + pos_y + move_y
        if block_value[x][y] > 0:
            return False
    return True

def move_shape(move_x, move_y):
    global pos_x, pos_y, shape_index, rotation_index
    if can_move(move_x, move_y):
        pos_x += move_x
        pos_y += move_y
        return True
    return False

def make_solid():
    global pos_x, pos_y, shape_index, rotation_index
    update_score(10)
    shape = shapes[shape_index]
    for i in range(rotation_index, rotation_index + 4):
        x = shape[i][0] + pos_x
        y = shape[i][1] + pos_y
        block_value[x][y] = 2

def move_down():
    global pos_x, pos_y, shape_index, rotation_index
    if not move_shape(0, 1):
        make_solid()
        check_full()
        pos_x = 5
        pos_y = 0
        shape_index = randint(0, 3)
        rotation_index = 0
    
def update_score(amt):
    global score
    score += amt
    cvs.itemconfig(score_text, text = "Score:" + str(score))

def update_display():
    global pos_x, pos_y, shape_index, rotation_index
    # Update matrix
    for i in range(1, width - 1):
        for j in range(1, height - 1):
            cvs.itemconfig(block[i][j], fill = colors[block_value[i][j]])
    # Update display for active shape
    shape = shapes[shape_index]
    for i in range(rotation_index, rotation_index + 4):
        x = shape[i][0] + pos_x
        y = shape[i][1] + pos_y
        cvs.itemconfig(block[x][y], fill = "blue")
        if block_value[x][y] == 2:
            lose = True
        
def delete_line(line):
    update_score(40)
    for x in range(1, width - 1):
        for y in range(line - 1, 1, -1):
            block_value[x][y + 1] - block_value[x][y]
        
def check_full():
    global pos_x, pos_y, shape_index, rotation_index
    for y in range(pos_y, pos_y + 4):
        if y >= height - 1:
            return
        is_full = True
        for x in range(1, height - 1):
            if block_value[x][y] == 0:
                is_full = False
                break
            if is_full:
                delete_line(y)
            
def key_press(event):
    global rotation_index
    if event.keysym == "Left":
        move_shape(-1, 0)
    if event.keysym == "Right":
        move_shape(1, 0)
    if event.keysym == "space":
        rotation_index = (rotation_index + 4) % len(shapes[shape_index])
        
cvs.bind_all("<Key>", key_press)
            
# Keeps window open
while not lose:
    sleep(0.2)
    move_down()
    update_display()
    window.update()
    
game_over_text = cvs.create_text(200, 300, text = "Game Over", font = ("Helvetica", 50), fill = "black")

window.mainloop()

