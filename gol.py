import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from argparse import ArgumentParser

def generate_random_state(dim):
    return [np.random.randint(2, size = dim) for _ in range(dim)]

def generate_initial_state_from_file(file):
    f = open(file, "r")
    grid = []
    for row in f.readlines():
        grid.append([int(col) for col in row if col.isnumeric()])
    return grid

def update_state(grid):
    tmp_grid = copy.deepcopy(grid)
    num_rows = len(grid)
    num_cols = len(grid[0])
    
    for row in range(0, num_rows):
        for col in range(0, num_cols):

            # moore neighborhood
            living_nbrs = grid[(row - 1) % num_rows][(col - 1) % num_cols] \
                + grid[(row - 1) % num_rows][col % num_cols] \
                + grid[(row - 1) % num_rows][(col + 1) % num_cols] \
                + grid[row % num_rows][(col - 1) % num_cols] \
                + grid[row % num_rows][(col + 1) % num_cols] \
                + grid[(row + 1) % num_rows][(col - 1) % num_cols] \
                + grid[(row + 1) % num_rows][col % num_cols] \
                + grid[(row + 1) % num_rows][(col + 1) % num_cols]
            
            # dead
            if grid[row][col] == 0:
                # resurrection
                if living_nbrs == 3:
                    tmp_grid[row][col] = 1
            # alive
            else:
                if living_nbrs < 2:
                    # solitude
                    tmp_grid[row][col] = 0
                elif living_nbrs > 3:
                    # overpopulation
                    tmp_grid[row][col] = 0
    return tmp_grid

def visualize_grid(grid):
    cmap = mpl.colors.ListedColormap(['#28bd5a', "k"])
    bounds = [0., 0.5, 1.]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    ax = plt.subplots()[1]

    for _ in range(100):
        grid = update_state(grid)
        ax.imshow(grid, interpolation = 'none', cmap = cmap, norm = norm)
        plt.pause(1e-17)

if __name__ == '__main__':

    parser = ArgumentParser(description = "Visualization for Conway's Game of Life")
    parser.add_argument("-r", "--random", type = int, required = False, metavar = "", help = "using random initial state of specified size")
    parser.add_argument("-i", "--input", type = str, required = False, metavar = "", help = "reading initial state from specified file")
    args = parser.parse_args()

    if args.random:
        print("generating random grid with size", args.random)
        grid = generate_random_state(args.random)
        visualize_grid(grid)
    elif args.input:
        print("generating grid from file", args.input)
        grid = generate_initial_state_from_file(args.input)
        visualize_grid(grid)
    else:
        print("since no initial state was specified, a random grid of size 64x64 is generated")
        grid = generate_random_state(64)
        visualize_grid(grid)