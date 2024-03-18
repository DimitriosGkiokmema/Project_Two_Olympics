""" This file is used for displaying graphs and the pygame window to the user
Anything visual used in our project is in this file
This includes buttons, graphs, and images

Additionally, this file also deals with mouse and key inputs
"""
import pygame
import matplotlib
pygame.init()

screen_width = 700
screen_height = 700
background_colour = (255, 255, 255)

window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('CSC111 Project 2: The Analysis of Summer Olympics Through External Effects')

####################################################
# Buttons
####################################################


class Button:
    """ template for the buttons"""
    def __init__(self, colour, x, y, width, height, text=''):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, window, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(window, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(window, self.colour, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            window.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 -
                                                                                        text.get_height() / 2)))

    def is_over(self, position):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < position[0] < self.x + self.width:
            if self.y < position[1] < self.y + self.height:
                return True

        return False


####################################################
# Game loop
####################################################


button = Button((0, 255, 0), 150, 225, 250, 100, 'Click Me')


def redraw_window():
    window.fill((255, 255, 255))
    button.draw(window, (0, 0, 0))


run = True
while run:
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and button.is_over(pos):
            print('red clicked')
        if event.type == pygame.MOUSEMOTION:
            if button.is_over(pos):
                button.colour = (255, 0, 0)
            else:
                button.colour = (0, 255, 0)

    # # updates the visuals
    redraw_window()
    pygame.display.update()
