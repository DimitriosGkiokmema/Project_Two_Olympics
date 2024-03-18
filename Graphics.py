""" This file is used for displaying graphs and the pygame window to the user
Anything visual used in our project is in this file
This includes buttons, graphs, and images

Additionally, this file also deals with mouse and key inputs
"""
import pygame
import matplotlib

pygame.init()

clock = pygame.time.Clock()

screen_width = 700
screen_height = 700
tile_size = 50
main_menu = True

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('CSC111 Project 2: The Analysis of Summer Olympics Through External Effects')

####################################################
# Buttons
####################################################


class Button:
    """ template for the buttons"""
    def __init__(self, x: int, y: int, image: str):
        self.image = None

        if image == 'start':
            img = pygame.image.load('C:\\Users\\')
            img = pygame.transform.scale(img, (6 * tile_size, 3 * tile_size))
            self.image = img
        elif image == 'exit':
            img = pygame.image.load('C:\\Users\\')
            img = pygame.transform.scale(img, (6 * tile_size, 3 * tile_size))
            self.image = img

        self.rect = self.image.get_rect()
        self.rect.x = x - 2 * tile_size
        self.rect.y = y - tile_size
        self.clicked = False

    def draw(self):
        """ draws the button"""
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouse over and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        screen.blit(self.image, self.rect)
        return action


####################################################
# Game loop
####################################################


start_button = Button(screen_width // 5, screen_height // 2, 'start')
exit_button = Button(4 * screen_width // 5, screen_height // 2, 'exit')

run = True
while run:
    if main_menu:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
