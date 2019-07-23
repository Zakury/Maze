import random

class Maze:

    def __init__(self, size):
        """
        Gets the sizes and creates the grid.
        """

        # Size in only unvisited cells.
        self.size_cells = size

        # Size including walls.
        self.size_walls = self.include_walls(size)

        # Create the grid.
        self.grid = [
            # Create rows.
            [
                # Create individual cells.
                # If both the X and Y of the cell are odd, the cell is unvisited.
                # Otherwise, the cell is a wall.
                (x % 2 and y % 2) + 1 for x in range(self.size_walls)
            ] for y in range(self.size_walls)
        ]

        # Generate the maze over the grid.
        self.generate_maze(self.grid)

    def include_walls(self, value):
        """
        Changes the given value into including the walls.
        """
        
        # 2x + 1 converts a value into including walls.
        return value * 2 + 1

    def inside_grid(self, x, y):
        """
        Checks if the given x, y coordinates are within the grid.
        """

        # X and Y cannot be less than 0, or greater than the size.
        return not (x < 0 or y < 0 or x > self.size_cells * 2 or y > self.size_cells * 2)
    
    def next_neighbor(self, x, y):
        """
        Picks a random unvisited cell adjacent to the given x, y coordinates.
        """
        
        def validate_neighbor(neighbor):
            """
            Decides whether a neighbor is valid for being the next cell.
            """

            # Adds the neighbor's relative position the cell's position.
            # The neighbors absolute position is then converted into including walls.
            neighbor_x = self.include_walls(x + neighbor[0])
            neighbor_y = self.include_walls(y + neighbor[1])
            
            # If inside the grid and unvisited.
            return self.inside_grid(neighbor_x, neighbor_y) and self.grid[neighbor_y][neighbor_x] == 2

        # All of the adjacent cell's positions, relative to the given cell.
        neighbors = [[0, 1], [1, 0], [0, -1], [-1, 0]]

        # Filter the adjacent cells on what is valid.
        validated = list(filter(validate_neighbor, neighbors))
        
        # Return a random validated cell if there is one.
        # If there isnt a valid cell, return None.
        return random.choice(validated) if validated else None

    def generate_maze(self, grid):
        """
        Creates the maze using recursive backtracking.
        https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracker
        """
        # The current cell's x and y.
        current_x, current_y = 0, 0

        # All the previous cells.
        previous_cells = []

        # While any unvisited cells are in the grid.
        while any(2 in row for row in self.grid):
            # Pick the next neighbor to go to.
            direction = self.next_neighbor(current_x, current_y)

            # Convert the current cell into including the walls.
            converted = [self.include_walls(current_x), self.include_walls(current_y)]

            # Set the current cell to be open.
            self.grid[converted[1]][converted[0]] = 0

            # If there were no valid neighbors.
            if not direction: 
                # Go back one move.
                current_x, current_y = previous_cells.pop()

                # Restart the process
                continue    

            # Add the current position the moves list.
            previous_cells.append([current_x, current_y])

            # Move in the direction we chose.
            current_x += direction[0]
            current_y += direction[1]
            
            # Set the new cell to be open.
            self.grid[converted[1] + direction[1]][converted[0] + direction[0]] = 0

