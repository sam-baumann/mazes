import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from copy import deepcopy
import numpy as np

fig, ax = plt.subplots()

class wall:
    def __init__(self):
        self.exists = True
    
    def remove(self):
        self.exists = False

    def __bool__(self):
        return self.exists
    
    def __repr__(self) -> str:
        return 'wall' if self.exists else 'no wall'

class cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.walls = []
        self.neighbors = []
        self.directions = {
            'N': 0,
            'S': 1,
            'E': 2,
            'W': 3
        }

    def index_from_dir_or_int(self, index):
        if isinstance(index, str):
            return self.directions[index]
        return index

    def remove_wall(self, direction):
        self.walls[self.index_from_dir_or_int(direction)].remove()

    def __getitem__(self, index):
        return self.walls[self.index_from_dir_or_int(index)]

class maze:
    def __init__(self, width, height = None):
        #intialize maze as 2d array of cells
        self.width = width
        if height is None:
            height = width
        self.height = height
        self.maze_arr = []
        for i in range(width):
            self.maze_arr.append([])
            for j in range(height):
                self.maze_arr[i].append(cell(i, j))
        #setup neighbors for each cell
        for y in range(height):
            for x in range(width):
                #every neighbor is a cell, unless it is on the edge of the maze,
                #in which case it is None
                curr_cell = self.maze_arr[x][y]
                curr_cell.neighbors.append(self.maze_arr[x][y - 1] if y > 0 else None) #north
                curr_cell.neighbors.append(self.maze_arr[x][y + 1] if y < height - 1 else None) #south
                curr_cell.neighbors.append(self.maze_arr[x + 1][y] if x < width - 1 else None) #east
                curr_cell.neighbors.append(self.maze_arr[x - 1][y] if x > 0 else None) #west


        #setup cell walls (neighboring cells share walls)
        for y in range(height):
            for x in range(width):
                curr_cell = self.maze_arr[x][y]
                #if we are the top row, we have to create our north wall
                if y == 0:
                    curr_cell.walls.append(wall())
                else: #otherwise, we can just use the north neighbor's south wall
                    curr_cell.walls.append(self.maze_arr[x][y - 1]['S'])
                #all cells create their south wall
                curr_cell.walls.append(wall())
                #all cells create their east wall
                curr_cell.walls.append(wall())
                #if we are the leftmost column, we have to create our west wall
                if x == 0:
                    curr_cell.walls.append(wall())
                else: #otherwise, we can just use the west neighbor's east wall
                    curr_cell.walls.append(self.maze_arr[x - 1][y]['E'])

        #cell (0, 0) will not have a west wall
        self.maze_arr[0][0]['W'].remove()
        #cell (width - 1, height - 1) will not have an east wall
        self.maze_arr[width - 1][height - 1]['E'].remove()

    def __getitem__(self, index):
        return self.maze_arr[index]    

    def plot(self, fname = None, animate = False):
        cell_size = 1
        # Create the plot
        for i in range(self.width):
            for j in range(self.height):
                curr_cell = self[i][j]
                x = i * cell_size
                y = (self.height - j - 1) * cell_size
                walls_count = 0
                if curr_cell['N']:
                    ax.plot([x, x + cell_size], [y + cell_size, y + cell_size], 'k')
                    walls_count += 1
                if curr_cell['S']:
                    ax.plot([x, x + cell_size], [y, y], 'k')
                    walls_count += 1
                if curr_cell['E']:
                    ax.plot([x + cell_size, x + cell_size], [y, y + cell_size], 'k')
                    walls_count += 1
                if curr_cell['W']:
                    ax.plot([x, x], [y, y + cell_size], 'k')
                    walls_count += 1

                #if all walls are drawn, fill in the cell
                if walls_count == 4:
                    ax.fill([x, x + cell_size, x + cell_size, x], [y, y, y + cell_size, y + cell_size], 'k')

        ax.set_aspect('equal')
        ax.axis('off')
        if fname is not None:
            print("Saving maze to " + fname)
            plt.savefig("./maze_images/" + fname)
        elif not animate: 
            plt.show()

def dfs_generate(m, animate = False):
    #initially used recursive implementation but it reached max recursion depth
    frames = []

    stack = []
    curr_cell = m[0][0]
    curr_cell.visited = True
    stack.append(curr_cell)

    while len(stack) > 0:
        curr_cell = stack[-1]
        stack.pop()

        to_visit = []

        for i in range(4):
            neighbor = curr_cell.neighbors[i]
            if neighbor is not None and not neighbor.visited:
                to_visit.append((i, neighbor))

        if len(to_visit) > 0:
            stack.append(curr_cell)
            i, neighbor = random.choice(to_visit)
            curr_cell.remove_wall(i)
            neighbor.visited = True
            stack.append(neighbor)
        
        if animate:
            frames.append(deepcopy(m))
    if animate:
        return frames



#create a maze and plot it
m = maze(10)
#dfs_generate(m)
#m.plot()

def animate(frame):
    curr_maze = frame
    ax.clear()
    curr_maze.plot(animate = True)
    return ax

#animate the maze generation
ani = FuncAnimation(fig, animate, dfs_generate(m, animate = True), interval = 100, repeat = False)
plt.show()