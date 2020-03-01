import pygame
import random
import time

from Ant import Ant

class Logic():
    def __init__(self, width, height, pixel_size, display):
        self.width = width
        self.height = height
        self.pixel_size = pixel_size
        self.cols = int(width / self.pixel_size)
        self.rows = int(height / self.pixel_size)
        self.display = display
        self.grid = self.generate_pop(self.generate_grid())

    def generate_grid(self):
        grid = []
        for x in range(0, self.cols):
            grid.append([])
            for y in range(0, self.rows):
                grid[x].append(0)
        return grid

    def generate_pop(self, grid):
        for x in range(0, self.width):
            for y in range(0, self.height):
                if x % self.pixel_size == 0 and y % self.pixel_size == 0:
                    col = self.display.get_at((x, y))
                    coloursum = col[0] + col[1] + col[2]
                    if coloursum > 383: #383
                        x_index = int(x/self.pixel_size)-1
                        y_index = int(y/self.pixel_size)-1
                        grid[x_index][y_index] = 1
        return grid


        # for x in grid:
        #     for y in range(0, len(x)):
        #         if random.random() >= 0.5:
        #             x[y] = 1
        # return grid

    def draw(self):
        self.display.fill((0,0,0))
        for x in range(0, self.cols):
            for y in range(0, self.rows):
                if self.grid[x][y] == 1:
                    x_pos = x * self.pixel_size
                    y_pos = y * self.pixel_size
                    colour = (random.randint(7,138), random.randint(7,232), random.randint(180,232))
                    pygame.draw.rect(self.display, colour, (x_pos, y_pos, self.pixel_size-1, self.pixel_size-1))
        pygame.display.update()

        #compute
        next_grid = self.generate_grid()
        for x in range(0, self.cols):
            for y in range(0, self.rows):
                state = self.grid[x][y]
                neighbour_count = self.count_neighbours(self.grid, x, y)
                if state == 0 and neighbour_count == 3:
                    next_grid[x][y] = 1
                elif state == 1 and (neighbour_count < 2 or neighbour_count > 3):
                    next_grid[x][y] = 0
                else:
                    next_grid[x][y] = state
        self.grid = next_grid

    def count_neighbours(self, grid, x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                col = (x + i + self.cols) % self.cols
                row = (y + j + self.rows) % self.rows
                count = count + grid[col][row]
        return count - grid[x][y]  # remove self from count


if __name__ == '__main__':
    pygame.init()


    ps = 10
    img = pygame.image.load('/Users/zak/Desktop/bluemarble.jpg')
    w = img.get_size()[0]
    h = img.get_size()[1]
    window = pygame.display.set_mode((w,h))
    window.blit(img, (0,0))
    pygame.display.update()
    logic = Logic(w, h, ps, window)
    clock = pygame.time.Clock()
    while True:
        logic.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # clock.tick(1)
        # pygame.display.update()
