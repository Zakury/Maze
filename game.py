import pyglet
import maze

class Window(pyglet.window.Window):

    Colors = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.maze_size = 20
        self.cell_size = 16
        self.size_mult = 1.20

        self.position = [1, 1]
        self.latest = []
        self.maze = maze.Maze(self.maze_size)
    
    def create_cell(self, rgb):
        if not Window.Colors.get(rgb, None):
            Window.Colors[rgb] = pyglet.image.SolidColorImagePattern(color=(*rgb, 255)).create_image(self.cell_size, self.cell_size)

        return Window.Colors.get(rgb)

    def blit_cell(self, x, y, rgb):
        self.create_cell(rgb).blit(x * self.cell_size, self.height - ((y + 1) * self.cell_size))

    def on_draw(self):
        self.clear()

        for y, row in enumerate(self.maze.grid):
            for x, cell in enumerate(row):
                if cell: self.blit_cell(x, y, (255, 255, 255))

        self.blit_cell(1, 1, (255, 0, 0))
        self.blit_cell((self.maze_size * 2) - 1, (self.maze_size * 2) - 1, (0, 255, 0))
        self.blit_cell(*self.position, (0, 0, 255))

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.W:
            if not self.maze.grid[self.position[1] - 1][self.position[0]]:
                self.position[1] -= 1
        if symbol == pyglet.window.key.A:
            if not self.maze.grid[self.position[1]][self.position[0] - 1]:
                self.position[0] -= 1
        if symbol == pyglet.window.key.S:
            if not self.maze.grid[self.position[1] + 1][self.position[0]]:
                self.position[1] += 1
        if symbol == pyglet.window.key.D:
            if not self.maze.grid[self.position[1]][self.position[0] + 1]:
                self.position[0] += 1

        if self.position == [(self.maze_size * 2) - 1, (self.maze_size * 2) - 1]:
            self.position = [1, 1]
            self.maze = maze.Maze(self.maze_size)

if __name__ == "__main__":
    window = Window(656, 656, "Labyrinth")
    pyglet.app.run()