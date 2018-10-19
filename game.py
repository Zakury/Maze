import pyglet.window.key as py_keyboard
import pyglet

from maze import Maze

class GameWindow(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        """
        Creates the window and sets the base variables.
        """

        super().__init__(*args, **kwargs)

        # Set the size of the maze, cells, and multiplier.
        self.maze_size = 5
        self.cell_size = 20
        self.size_mult = 1.20

        # Generate maze and start at the bottom left.
        self.maze = Maze(self.maze_size)
        self.maze.generate_maze()
        self.cell_cur = self.maze.cell(0, 0)

        # Score label
        self.score_label = pyglet.text.Label(
            "0",
            font_name='Times New Roman',
            font_size=40,
            x=self.width//2, y=self.height - 50,
            anchor_x='center', anchor_y='center'
        )

    def move_cell(self, direction):
        """
        Move to the next cell in a direction.
        """

        pass

    def on_key_press(self, symbol, modifiers):
        """
        Handles user input for movement.
        """

        movement_bindings = {
            "n": (py_keyboard.W, py_keyboard.UP),
            "e": (py_keyboard.D, py_keyboard.RIGHT),
            "s": (py_keyboard.S, py_keyboard.DOWN),
            "w": (py_keyboard.A, py_keyboard.LEFT)
        }

        # Get the player's cell.
        player_cell = self.cell_cur

        # Handle movement going up.
        if (symbol in [py_keyboard.W, py_keyboard.UP]) and (not player_cell.walls[0]):
            self.cell_cur = self.maze.cell(self.cell_cur.x, self.cell_cur.y + 1)

        # Handle movement going right.
        if (symbol in [py_keyboard.D, py_keyboard.RIGHT]) and (not player_cell.walls[1]):
            self.cell_cur = self.maze.grid[self.cell_cur.y][self.cell_cur.x + 1]
        
        # Handle movement going down.
        if (symbol in [py_keyboard.S, py_keyboard.DOWN]) and (not player_cell.walls[2]):
            self.cell_cur = self.maze.grid[self.cell_cur.y - 1][self.cell_cur.x]

        # Handle movement going left.
        if (symbol in [py_keyboard.A, py_keyboard.LEFT]) and (not player_cell.walls[3]):
            self.cell_cur = self.maze.grid[self.cell_cur.y][self.cell_cur.x - 1]    

        # Handle level complete
        if self.cell_cur.x == self.maze_size - 1 and self.cell_cur.y == self.maze_size - 1:
            self.maze_size = int(self.maze_size * self.size_mult)
            # self.maze = Maze(self.maze_size)
            self.maze.size = self.maze_size
            self.maze.generate_grid()
            self.maze.generate_maze()
            self.cell_cur = self.maze.cell(0, 0)

            self.score_label.text = str(int(self.score_label.text) + 1)
            print("Level Complete!")

    def on_draw(self):
        """
        Render the maze.
        """

        # Clear the screen.
        self.clear()

        # Draw score
        self.score_label.draw()

        # Get the center of the screen in cell coordinates.
        center_x = (self.width  // 2) / self.cell_size
        center_y = (self.height // 2) / self.cell_size

        # Get the player's cell.
        player_cell = self.cell_cur

        # Iterate over all cells in the maze
        for row in self.maze.grid:
            for cell in row:
                if abs(cell.x - player_cell.x) < self.height/self.cell_size/2 and abs(cell.y - player_cell.y) < self.width/self.cell_size/2:
                    # Get the correct render coordinates for the cell.
                    render_x = (cell.x + center_x - player_cell.x) * self.cell_size
                    render_y = (cell.y + center_y - player_cell.y) * self.cell_size

                    # Handle rendering for the top wall.
                    if cell.walls[0]:
                        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                            ("v2f", (
                                render_x, 
                                render_y + self.cell_size, 
                                render_x + self.cell_size, 
                                render_y + self.cell_size
                            ))
                        )

                    # Handle rendering for the right wall.
                    if cell.walls[1]:
                        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                            ("v2f", (
                                render_x + self.cell_size, 
                                render_y + self.cell_size, 
                                render_x + self.cell_size, 
                                render_y
                            ))
                        )

                    # Handle rendering for the bottom wall.
                    if cell.walls[2]:
                        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                            ("v2f", (
                                render_x, 
                                render_y, 
                                render_x + self.cell_size, 
                                render_y
                            ))
                        )

                    # Handle rendering for the left wall.
                    if cell.walls[3]:
                        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                            ("v2f", (
                                render_x, 
                                render_y, 
                                render_x, 
                                render_y + self.cell_size
                            ))
                        )

        # Convert the center coordinates to pixel coordinates.
        render_x = center_x * self.cell_size
        render_y = center_y * self.cell_size
        
        # The pixel offset from the edge of the cell.
        offset = 4

        # Draw the player square in the center of the screen.
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
            ("v2f", (
                render_x + offset, render_y + offset,
                render_x + offset, render_y + self.cell_size - offset,
                render_x + self.cell_size - offset, render_y + self.cell_size - offset,
                render_x + self.cell_size - offset, render_y + offset
            ))
        )

if __name__ == "__main__":
    window = GameWindow(500, 500, "Labyrinth")
    pyglet.app.run()