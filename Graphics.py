""" This file is used for displaying graphs and the pygame window to the user
Anything visual used in our project is in this file
This includes buttons, graphs, and images

Additionally, this file also deals with mouse and key inputs
Reference for button: https://www.youtube.com/watch?v=4_9twnEduFA
"""
import random
import data
import math
import pygame
import matplotlib.pyplot as plt
import pandas as pd

pygame.init()

screen_width = 1200
screen_height = 750
background_colour = (125, 235, 255)

window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('CSC111 Project 2: The Analysis of Summer Olympics Through External Effects')
graph = data.load_graph('summer_modified.csv', 'country_codes_modified.csv')
YEARS = [x for x in range(1940, 2021)]

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
        self.height = 80
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
# Making the graphs
####################################################


# def single_plot(names: list[str], title:str, bar: bool, style: str, y: list[list[int]], x: list[list[int]] = 0):
def single_plot():
    """ An instance of this class requires the graph name, y and (optionally) the x values. x and y MUST be lists
    This class will display a single or multiple graphs on the same window, depending on how many

    Instance Attributes:
        - names: a list containing the title of each graph
        - style: the type of graph, either 'line' or 'bar'
        - y: a list of y coordinates
        - x: a list of x coordinates. If nothing is entered for it, the x coordinates are every num 1940-2020

    Representation Invariants:
        - style in ['single line', 'many lines']
        - bar == True or bar == False
        - len(y) == len(x) or x == 0
        - if a value is given for x cords, then y must have the same number of values
    """
    style = 'single line'
    apples = [1, 2, 3]
    pears = [2, 3, 7]
    bananas = [2, 3, 5]
    oranges = [1, 3, 5]
    title = 'Random Graph'
    bar = False
    # if x == 0:
    #     x = YEARS
    names = ['apples', 'pears', 'oranges', 'bananas']
    y = [apples, pears, oranges, bananas]

    # Keep
    line_explanation = {names[i]: y[i] for i in range(len(names))}

    if style == 'many lines':  # Single graph with one or multiple lines in it
        # Single graph, multiple lines
        df = pd.DataFrame(line_explanation)

        # Plot individual lines
        for i in line_explanation:
            plt.plot(pears, df[i], label=i, linewidth=4, color=generate_random_colour())

    elif style == 'single line':
        if bar:
            plt.bar(x=apples, height=pears)
        else:
            plt.plot(oranges, pears, label="My Line", color="blue", linewidth=2)

    # Add legend, axis labels, and title
    plt.ylabel('Medals', fontsize=14)
    plt.xlabel('Years', fontsize=14)
    plt.title(title, fontsize=16)
    plt.grid(True)
    plt.show()


#########################################
# Below function still under construction
#########################################


def multiple_plots(names: list[str], title:str, bar: bool, style: str, y: list[list[int]], x: list[list[int]] = 0):
    """ An instance of this class requires the graph name, y and (optionally) the x values. x and y MUST be lists
    This class will display a single or multiple graphs on the same window, depending on how many

    Instance Attributes:
        - names: a list containing the title of each graph
        - style: the type of graph, either 'line' or 'bar'
        - y: a list (or nested list) of y coordinates
        - x: a list (or nested list) of x coordinates. If nothing is entered for it, the x coordinates are 1940-2020

    Representation Invariants:
        - len(names) > 0
        - style in ['many graphs', 'single line', 'bar']
        - len(names) == len(y) or all(len(names) == len(sub_y) for sub_y in y)
        - if a value is given for x cords, then x must have the same length as names
    """
    if x == 0:
        x = YEARS
    style = random.choice(['many graphs', 'single or many line'])
    names = ['Rank', 'Performance', 'Host Effect', 'Team vs Indi']
    side_length = int(math.sqrt(len(names)))

    apples = [1, 2, 3]
    pears = [2, 3, 7]
    bananas = [2, 3, 5]
    oranges = [x // 3 for x in range(1940, 2021)]

    if style == 'many graphs':  # Multiple graphs all with one line
        fig, axs = plt.subplots(side_length, side_length)
        name_i = 0
        for i in range(side_length):
            for j in range(side_length):
                colour = random.choice(['blue', 'red', 'pink', 'green', 'purple', 'gray', 'cyan', 'olive'])
                axs[i, j].plot(YEARS, oranges, f'tab:{colour}')
                axs[i, j].set_title(names[name_i])  # Sets graph title
                axs[i, j].set_xlabel('Years')  # Sets x-axis title
                axs[i, j].set_ylabel('Medals')  # Sets y-axis title
                name_i += 1
    elif style == 'single or many line':  # Single graph with one or multiple lines in it
        # Single graph, multiple lines
        df = pd.DataFrame({'apples': apples, 'pears': pears, 'oranges': apples, 'bananas': bananas})

        # Plot individual lines
        plt.plot(df['apples'], label='apples', color='red')
        plt.plot(df['apples'], label='oranges', color='orange', linewidth=4)
        plt.plot(df['bananas'], label='bananas', color='yellow', linestyle='dashed')

        # Add legend, axis labels, and title
        plt.legend()
        plt.ylabel('Amount', fontsize=14)
        plt.xlabel('Fruits', fontsize=14)
        plt.title('Fruit Sales', fontsize=16)

    plt.show()


def generate_random_colour() -> tuple[float, float, float]:
    """ Generates a random tuple of rgb values which will be used for the line colours in the graphs
    """
    rgb = []

    for i in range(3):
        rgb.append(random.randint(0, 255) / 255)

    return rgb[0], rgb[1], rgb[2]

####################################################
# Game loop
####################################################


# Create buttons
annual_medals = Button((0, 255, 0), 100, 50, 'Annual Medals')
given_area = Button((0, 255, 0), 600, 50, 'Given Area')
gsb = Button((0, 255, 0), 100, 170, 'Gold, Silver, and Bronze')
rankings = Button((0, 255, 0), 600, 170, 'Rank')
annual_data = Button((0, 255, 0), 100, 290, 'Annual Data')
historical = Button((0, 255, 0), 600, 290, 'Impact of Historical Events')
host_effect = Button((0, 255, 0), 100, 410, 'Host Effect')
team_vs_indi = Button((0, 255, 0), 600, 410, 'Team vs Individual Sports')
performance = Button((0, 255, 0), 100, 530, 'Performance')
countries = Button((0, 255, 0), 600, 530, 'Country Statistics')
sports = Button((0, 255, 0), 350, 650, 'Sport Statistics')

# Store buttons in a list
buttons_main = [annual_medals, given_area, gsb, rankings, annual_data, historical, host_effect, team_vs_indi]
buttons_main.extend([performance, countries, sports])


def redraw_window():
    window.fill(background_colour)

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


show_graph = False
run = True
while run:

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
        for button in buttons_main:
            if event.type == pygame.MOUSEBUTTONDOWN and button.is_over(pos):
                show_graph = True
            if event.type == pygame.MOUSEMOTION:
                if button.is_over(pos):
                    button.colour = (255, 0, 0)
                else:
                    button.colour = (0, 255, 0)

    # Draws the graph
    if show_graph:
        show_graph = False
        single_plot()

    # updates the visuals
    redraw_window()
    pygame.display.update()
