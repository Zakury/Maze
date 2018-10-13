import random

class Cell:

    def __init__(self, maze, x, y):
        """
        Creates the cell and sets the base variables.
        """

        # Link the cell to the maze.
        self.maze = maze

        # Sets the position of the cell in the maze.
        self.x = x
        self.y = y

        # Whether the walls exist, in the order of top, right, bottom, left
        self.walls = [True, True, True, True]

        # If the cell has been visited.
        self.visited = False

        # If the cell is the current one.
        self.current = False

    def remove_walls(self, other_index):
        """
        Remove the wall of the cell in the direction of the other cell.
        """

        # Convert the cell index into x and y coordinates.
        other_x = self.maze.grid[other_index].x
        other_y = self.maze.grid[other_index].y

        # If the other cell is up, remove the top wall.
        if self.y < other_y:
            self.walls[0] = False
        
        # If the other cell is right, remove the right wall.
        if self.x < other_x:
            self.walls[1] = False

        # If the other cell is down, remove the bottom wall.
        if self.y > other_y:
            self.walls[2] = False

        # If the other cell is left, remove the left wall.
        if self.x > other_x:
            self.walls[3] = False
        
class Maze:

    def __init__(self, cols, rows):
        # Create the grid and save the maze size.
        self.grid = [Cell(self, x, y) for x in range(cols) for y in range(rows)]
        self.cols = cols
        self.rows = rows

        # Select the bottom left cell and create the stack.
        self.select_cell(0)
        self.stack = []

    def index(self, x, y):
        """
        Get the index of a certain position in the grid array.
        """

        return y + x * self.cols

    def get_adjacent(self):
        """
        Get the valid adjacent cells.
        """
        
        # Create the list of valid cells.
        valid_cells = []

        def validate(x, y):
            """
            Check if a cell is valid.
            """

            cell_index = self.index(x, y)

            # Check if the cell is inbounds. 
            if x >= 0 and x < self.cols and y >= 0 and y < self.rows:
                # Check if the cell hasn't been visited
                if not self.grid[cell_index].visited:
                    # Push the cell to the valid cell list.
                    valid_cells.append(cell_index)

        # Get the x and y values of the current cell.
        x, y = self.grid[self.current].x, self.grid[self.current].y

        # Validate the cells in the four directions.
        validate(x, y + 1)
        validate(x + 1, y)
        validate(x, y - 1)
        validate(x - 1, y)
        
        # Return the valid cells.
        return valid_cells

    def select_cell(self, index):
        """
        Select a cell index as the current one.
        """

        # Mark the cell as visited.
        self.grid[index].visited = True

        # Set the cell as the current one.
        self.current = index

    def generate(self):
        """
        Generate the maze using:
        https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracker
        """

        # While any unvisited cells in the grid.
        while any(not cell.visited for cell in self.grid):
            # Get neighbors that has not been visited or are out of bounds.
            adjacents = self.get_adjacent()

            # If any neighbors that have not been visited or out of bounds
            if adjacents:
                # Choose a random neighbor.
                next_cell = random.choice(adjacents)

                # Push the current cell to the stack.
                self.stack.append(self.current)
                
                # Remove the wall between the current cell and the next cell.
                self.grid[self.current].remove_walls(next_cell)
                self.grid[next_cell].remove_walls(self.current)
                
                # Select the next cell.
                self.select_cell(next_cell)      

            # Otherwise if the stack is not empty,         
            elif self.stack:
                # Pop a cell from the stack and select it.
                self.select_cell(self.stack.pop())
