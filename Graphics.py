""" This file is used for displaying graphs and the pygame window to the user
Anything visual used in our project is in this file
This includes buttons, graphs, and images

Additionally, this file also deals with mouse and key inputs
Reference for button: https://www.youtube.com/watch?v=4_9twnEduFA
"""
import pygame
import matplotlib
import data

pygame.init()

screen_width = 1200
screen_height = 700
background_colour = (255, 255, 255)

window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('CSC111 Project 2: The Analysis of Summer Olympics Through External Effects')
# graph = data.load_graph('summer_modified.csv', 'country_codes_modified.csv')

####################################################
# Buttons
####################################################


class Button:
    """ template for the buttons"""
    def __init__(self, colour, x, y, text=''):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = 450
        self.height = 40
        self.text = text

    def draw(self, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(window, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(window, self.colour, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('calibri', 40)
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

# Create buttons
annual_medals = Button((0, 255, 0), 100, 50, 'Annual Medals')
given_area = Button((0, 255, 0), 100, 100, 'Given Area')
gsb = Button((0, 255, 0), 100, 150, 'Gold, Silver, and Bronze')
rankings = Button((0, 255, 0), 100, 200, 'Rank')
annual_data = Button((0, 255, 0), 100, 250, 'Annual Data')
historical = Button((0, 255, 0), 100, 300, 'Impact of Historical Events')
host_effect = Button((0, 255, 0), 100, 350, 'Host Effect')
team_vs_indi = Button((0, 255, 0), 100, 400, 'Team vs Individual Sports')
performance = Button((0, 255, 0), 100, 450, 'Performance')
countries = Button((0, 255, 0), 100, 500, 'Country Statistics')
sports = Button((0, 255, 0), 100, 550, 'Sport Statistics')

# Store buttons in a list
buttons_main = [annual_medals, given_area, gsb, rankings, annual_data, historical, host_effect, team_vs_indi]
buttons_main.extend([performance, countries, sports])

def redraw_window():
    window.fill((125, 235, 255))

    for button in buttons_main:
        button.draw((0, 0, 0))


def alter_str(txt: str):
    txt = txt.split()
    final = ['']
    str = ''

    for word in txt:
        if len(word) + len(final[-1]) < 14:
            final[-1] += word + ' '
        else:
            final.append(word)

    for i in final:
        str += i + '\n'

    return str


run = True
while run:
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
        for button in buttons_main:
            if event.type == pygame.MOUSEBUTTONDOWN and button.is_over(pos):
                print(button.text + ' clicked')
            if event.type == pygame.MOUSEMOTION:
                if button.is_over(pos):
                    button.colour = (255, 0, 0)
                else:
                    button.colour = (0, 255, 0)

    # # updates the visuals
    redraw_window()
    pygame.display.update()
