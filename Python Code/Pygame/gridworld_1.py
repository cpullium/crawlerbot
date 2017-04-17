# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://cs.simpson.edu/?q=python_pygame_examples

import pygame, sys
from pygame.locals import *
from colors import *

STATE_ROWS = 3;
STATE_COL = 3;
NUM_ACTIONS = 4;
Q = np.zeros((STATE_ROWS,STATE_COL,NUM_ACTIONS))

# Data Definition
class GridWorld:
    '''Create a resizable hello world window'''
    def __init__(self):
        pygame.init()
        self.width = 300
        self.height = 300
        DISPLAYSURF = pygame.display.set_mode((self.width,self.height), RESIZABLE)
        DISPLAYSURF.fill(BLACK)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == VIDEORESIZE:
                    self.CreateWindow(event.w,event.h)
            pygame.display.update()
            
    def DrawGrid(self, width, height):
        MARGIN = width/50
        BOXWIDTH = width/(STATE_ROWS)
        BOXHEIGHT = BOXWIDTH
        for row in range(STATE_ROWS):
            for column in range(STATE_COLUMNS):
                color = WHITE
                if Q[row][column] > 0:
                    color = GREEN
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + width) * column + MARGIN,
                                  (MARGIN + height) * row + MARGIN,
                                  BOXWIDTH,
                                  BOXHEIGHT],2)

    def CreateWindow(self,width,height):
        '''Updates the window width and height '''
        pygame.display.set_caption("Press ESC to quit")
        DISPLAYSURF = pygame.display.set_mode((width,height),RESIZABLE)
        DISPLAYSURF.fill(BLACK)
        self.DrawGrid(width, height)


if __name__ == '__main__':

    GridWorld().run()