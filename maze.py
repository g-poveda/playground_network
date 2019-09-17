# Random Maze Generator using Depth-first Search
# http://en.wikipedia.org/wiki/Maze_generation_algorithm
# http://code.activestate.com/recipes/578356-random-maze-generator/
# FB36 - 20130106
import random
#from PIL import Image
from collections import defaultdict
import numpy as np

def do_maze(mx, my):
    maze = np.zeros((my, mx))
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0] # 4 directions to move in the maze
    # start the maze from a random cell
    cx = random.randint(0, mx - 1); cy = random.randint(0, my - 1)
    maze[cy, cx] = 1
    stack = [(cx, cy, 0)] # stack element: (x, y, direction)
    graph = defaultdict(set, set())
    while len(stack) > 0:
        (cx, cy, cd) = stack[-1]
        # to prevent zigzags:
        # if changed direction in the last move then cannot change again
        if len(stack) > 2:
            if cd != stack[-2][2]:
                dirRange = [cd]
            else: 
                dirRange = range(4)
        else: dirRange = range(4)

        # find a new cell to add 
        cx_c, cy_c = cx, cy
        nlst = [] # list of available neighbors
        for i in dirRange:
            nx = cx + dx[i]
            ny = cy + dy[i]
            if nx >= 0 and nx < mx and ny >= 0 and ny < my:
                if maze[ny][nx] == 0:
                    ctr = 0 # of occupied neighbors must be 1
                    for j in range(4):
                        ex = nx + dx[j]
                        ey = ny + dy[j]
                        if ex >= 0 and ex < mx and ey >= 0 and ey < my:
                            if maze[ey,ex] == 1: 
                                ctr += 1
                    if ctr == 1: 
                        nlst.append(i)
        # if 1 or more neighbors available then randomly select one and move
        if len(nlst) > 0:
            ir = nlst[random.randint(0, len(nlst) - 1)]
            cx += dx[ir]
            cy += dy[ir]
            maze[cy, cx] = 1
            stack.append((cx, cy, ir))
            graph[(cx_c, cy_c)].add((cx, cy))
            graph[(cx, cy)].add((cx_c, cy_c))
        else: stack.pop()
    return maze, graph

def example():
    imgx = 500
    imgy = 500
    color = [(0, 0, 0), (255, 255, 255)] # RGB colors of the maze
    mx = 200
    my = 200
    maze, graph = do_maze(mx, my)
    image = Image.new("RGB", (imgx, imgy))
    pixels = image.load()
    # paint the maze
    for ky in range(imgy):
        for kx in range(imgx):
            pixels[kx, ky] = color[maze[int(my * ky / imgy)][int(mx * kx / imgx)]]
    image.save("Maze_" + str(mx) + "x" + str(my) + ".png", "PNG")

if __name__ == "__main__":
    example()