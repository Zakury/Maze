import pyglet
from maze import Maze

class Game(pyglet.window.Window):
    """
    The game portion of the maze.
    """

    # Store the already accessed colors.
    Colors = {}

    def __init__(self, *args, **kwargs):
        """
        Create the windows and set some properties.
        """

        super().__init__(*args, **kwargs)

        # Maze size in starter cells.
        self.maze_size = 20

        # Pixel size for each cell.
        self.cell_size = 16

        # Current player position.
        self.position = [1, 1]

        # Generate the maze.
        self.maze = Maze(self.maze_size).grid
    
    def create_cell(self, rgb):
        """
        Creates an RGB image the size of a cell.
        """

        # If the color hasn't been made already.
        if not Game.Colors.get(rgb, None):
            # Create the color.
            color = pyglet.image.SolidColorImagePattern(color=(*rgb, 255))
            
            # Create and store the image based on the color.
            Game.Colors[rgb] = color.create_image(self.cell_size, self.cell_size)

        # Return the image.
        return Game.Colors.get(rgb)

    def blit_cell(self, x, y, rgb):
        """
        Draws a cell of rgb color at x, y.
        """

        # Y has to be subtracted from height as 2d arrays start at the top left,
        # and pyglet starts at the top right.
        self.create_cell(rgb).blit(x * self.cell_size, self.height - ((y + 1) * self.cell_size))

    def on_draw(self):
        """
        Renders the game.
        """

        # Clear the window.
        self.clear()

        # Go through rows in grid.
        for y, row in enumerate(self.maze):
            # Go through cells in row.
            for x, cell in enumerate(row):
                # If the cell is a wall, blit it.
                if cell: self.blit_cell(x, y, (255, 255, 255))

        # Starting cell marker.
        self.blit_cell(1, 1, (255, 0, 0))
        
        # Ending cell marker.
        self.blit_cell((self.maze_size * 2) - 1, (self.maze_size * 2) - 1, (0, 255, 0))
        
        # Player cell marker.
        self.blit_cell(*self.position, (0, 0, 255))

    def on_key_press(self, symbol, modifiers):
        """
        Handles movement.
        """
        
        # W = Up
        if symbol == pyglet.window.key.W:
            # If no wall above.
            if not self.maze[self.position[1] - 1][self.position[0]]:
                # Go up.
                self.position[1] -= 1

        # A = Left
        if symbol == pyglet.window.key.A:
            # If no wall left.
            if not self.maze[self.position[1]][self.position[0] - 1]:
                # Go Left.
                self.position[0] -= 1

        # S = Down
        if symbol == pyglet.window.key.S:
            # If no wall down.
            if not self.maze[self.position[1] + 1][self.position[0]]:
                # Go down.
                self.position[1] += 1

        # D = Right
        if symbol == pyglet.window.key.D:
            # If no wall right.
            if not self.maze[self.position[1]][self.position[0] + 1]:
                # Go right.
                self.position[0] += 1

        # If the player is on the ending square.
        if self.position == [(self.maze_size * 2) - 1, (self.maze_size * 2) - 1]:
            # Create a new maze.
            self.new_maze = Maze(self.maze_size).grid

            # Move the player to the start.
            self.position = [1, 1]

if __name__ == "__main__":
    # Create the window.
    window = Game(656, 656, "Labyrinth")

    # Run the game.
    pyglet.app.run()