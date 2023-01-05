import pygame
import sys

from visualisation_colors import Colors
from graph import Node, bfs, a_star


class Visualisation(Colors):
    fps = 144

    def __init__(self) -> None:

        pygame.init()
        pygame.display.set_caption("Graph Visualisation App")

        self.width = 40
        self.height = 20
        self.block_size = 32

        self.window = pygame.display.set_mode((self.width*self.block_size,self.height*self.block_size))
        self.clock = pygame.time.Clock()

        self.visualising = False
        self.nextFrameIn = 0
        self.place_delay = 0

        self.gen = None

        self.start_marked = False
        self.end_marked = False
        self.start = (0, 0)
        self.end = (self.width-1, self.height-1)

        self.grid = self.get_clear_grid()

    def get_clear_grid(self):
        return [[Node(j, i, self.EMPTY_COLOR) for i in range(self.width)] for j in range(self.height)]

    def eventloop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == "b":
                    if self.start_marked and self.end_marked:
                        self.gen = bfs(self.start, self.grid)
                        self.visualising = True

                elif pygame.key.name(event.key) == "a":
                    if self.start_marked and self.end_marked:
                        self.gen = a_star(self.start, self.end, self.grid)
                        self.visualising = True

                elif pygame.key.name(event.key) == "r":
                    self.start_marked = False
                    self.end_marked = False
                    self.visualising = False
                    self.grid = self.get_clear_grid()

    def handle_fps(self):
        self.clock.tick(self.fps)


    def handleMouse(self):
        if self.visualising:
            return

        mx, my = pygame.mouse.get_pos()
        m_keys = pygame.mouse.get_pressed()

        row = mx//self.block_size
        col = my//self.block_size

        if self.place_delay > 0:
            self.place_delay -= 1

        if m_keys[0]:
            if self.place_delay <= 0:
                if self.start_marked and self.end_marked:
                    if self.grid[col][row].color == self.EMPTY_COLOR:
                        self.grid[col][row].color = self.WALL_COLOR

                if self.start_marked:
                    if not self.end_marked and self.start != (row, col):
                        self.end = (row, col)
                        self.end_marked = True
                        self.grid[col][row].color = self.END_COLOR
                        self.place_delay = 30
                else:
                    self.start = (row, col)
                    self.start_marked = True
                    self.grid[col][row].color = self.START_COLOR
                    self.place_delay = 30

        elif m_keys[2]:
            if self.grid[col][row].color == self.START_COLOR:
                self.start = None
            elif self.grid[col][row].color == self.END_COLOR:
                self.end = None
            self.grid[col][row].color = self.EMPTY_COLOR


    def visual(self):
        if self.visualising:
            if self.nextFrameIn < 0:
                try:
                    output = self.gen.__next__()
                    if isinstance(output, int):
                        print(f"Nodes explored: {output}")

                except StopIteration:
                    self.visualising = False
                    self.nextFrameIn = 0
                self.nextFrameIn = 1
            else:
                self.nextFrameIn += -1

    def draw(self):

        self.window.fill((255, 255, 255)) # Background colour

        for row in self.grid:
            for node in row:
                x = node.col*self.block_size
                y = node.row*self.block_size

                pygame.draw.rect(self.window, node.color, pygame.Rect(x+1, y+1, self.block_size-2, self.block_size-2))

        pygame.display.update()

    def mainloop(self):
        while True:
            self.handle_fps()
            self.handleMouse()

            self.eventloop()
            self.visual()

            self.draw()


def main():
    Visualisation().mainloop()


if __name__ == "__main__":
    main()
