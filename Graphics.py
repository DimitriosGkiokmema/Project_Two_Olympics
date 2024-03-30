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

group = {'Archery': 0, 'Athletics': 0, 'Badminton': 0, 'Baseball': 1, 'Basketball': 1, 'Basque Pelota': 1,
         'Beach Volleyball': 1, 'Boxing': 0, 'Canoe / Kayak F': 0, 'Canoe / Kayak S': 0, 'Canoe Slalom': 0,
         'Canoe Sprint': 1, 'Cricket': 1, 'Croquet': 0, 'Cycling BMX': 0, 'Cycling Road': 0, 'Cycling Track': 0,
         'Diving': 0, 'Dressage': 0, 'Eventing': 0, 'Fencing': 0, 'Figure skating': 0, 'Football': 1, 'Golf': 0,
         'Gymnastics Artistic': 0, 'Gymnastics Rhythmic': 1, 'Handball': 1, 'Hockey': 1, 'Ice Hockey': 1,
         'Jeu de Paume': 0, 'Judo': 0, 'Jumping': 0, 'Lacrosse': 1, 'Marathon swimming': 0, 'Modern Pentathlon': 0,
         'Mountain Bike': 1, 'Polo': 1, 'Rackets': 0, 'Roque': 0, 'Rowing': 1, 'Rugby': 1, 'Sailing': 1, 'Shooting': 0,
         'Softball': 1, 'Swimming': 0, 'Synchronized Swimming': 1, 'Table Tennis': 0, 'Taekwondo': 0, 'Tennis': 0,
         'Trampoline': 0, 'Triathlon': 0, 'Tug of War': 1, 'Vaulting': 0, 'Volleyball': 1, 'Water Motorsport': 1,
         'Water Polo': 1, 'Weightlifting': 0, 'Wrestling Freestyle': 0, 'Wrestling Gre-R': 0}

graph = data.load_graph('summer_modified.csv', 'country_codes_modified.csv', group)

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
        """Draw the button on the screen"""
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


def single_plot(names: list[str], title: str, bar: bool, style: str, y: list[list[int]], x: list[int] = 0):
    # def single_plot():  # Used for quickly testing this function
    """ An instance of this class requires the graph name, y and (optionally) the x values. x and y MUST be lists
    This class will display a single or multiple graphs on the same window, depending on how many

    Instance Attributes:
        - names: a list containing the title of each graph
        - title: the title to display at the top of the window
        - bar: the type of graph, True if a bar graph, False if a line graph
        - style: many or single lined graph
        - y: a list of y coordinates
        - x: a list of x coordinates. If nothing is entered for it, the x coordinates are every num 1940-2020

    Representation Invariants:
        - len(names) > 0
        - style in ['single', 'many']
        - bar == True or bar == False
        - len(y) == len(x) or x == 0
        - if a value is given for x cords, then y must have the same number of values
    """
    # Below is used for testing
    # style = 'single'
    # apples = [1, 2, 3]
    # pears = [2, 3, 7]
    # bananas = [2, 3, 5]
    # oranges = [1, 3, 5]
    # y = [apples, pears, bananas, oranges]
    # names = ['apples', 'pears', 'bananas', 'oranges']
    # title = 'Random Graph'
    # bar = False
    # x = bananas

    # if x == 0:
    #     x = YEARS

    # Keep this line
    line_explanation = {names[i]: y[i] for i in range(len(names))}

    if style == 'many':  # Graph with one or multiple lines in it
        # Single graph, multiple lines
        df = pd.DataFrame(line_explanation)  # Shows a small table on the graph of what each line means

        # Plot individual lines
        for i in line_explanation:
            plt.plot(x, df[i], label=i, linewidth=4, color=generate_random_colour())

    elif style == 'single':
        if bar:
            plt.bar(x=x, height=y[0])
        else:
            plt.plot(x, y[0], label="My Line", color="blue", linewidth=2)

    # Add legend, axis labels, and title
    plt.ylabel('Medals', fontsize=14)
    plt.xlabel('Years', fontsize=14)
    plt.title(title, fontsize=16)
    plt.grid(True)
    plt.show()


def two_plots(names: list[str], title: str, bar: bool, s: str, y1: list[list[int]], y2: list[list[int]], x: list = 0):
    """ An instance of this class requires the graph name, y and (optionally) the x values. x and y MUST be lists
    This class will display one or two graphs on the same window, depending on how many are needed

    Instance Attributes:
        - names: a list containing the title of each graph
        - title: the title to display at the top of the window
        - bar: the type of graph, True if a bar graph, False if a line graph
        - s: many or single lined graph. Same as style variable from above function
        - y: a list of y coordinates
        - x: a list of x coordinates. If nothing is entered for it, the x coordinates are every num 1940-2020

    Representation Invariants:
        - len(names) > 0
        - s in ['many', 'single']
        - len(y) == len(x) or x == 0
        - if a value is given for x cords, then y must have the same number of values
    """
    if x == 0:
        x = YEARS

    # Keep this line
    line_explanation = {names[i]: y1[i] for i in range(len(names))}

    for y in y2:
        line_explanation[names[y2.index(y) + len(line_explanation)]] = y

    if s == 'single' and not bar:  # Two graphs with one line
        fig, axs = plt.subplots(1, 2)

        for y in [y1, y2]:
            i = [y1, y2].index(y)
            if not bar:
                axs[i].plot(x, y, color=generate_random_colour())
            else:
                axs[i].bar(x=x, height=y, color=generate_random_colour())

            axs[i].set_title(names[i])  # Sets graph title
            axs[i].set_xlabel('Years')  # Sets x-axis title
            axs[i].set_ylabel('Medals')  # Sets y-axis title
    elif s == 'many':  # Two graphs with  multiple lines
        fig, axs = plt.subplots(1, 2)
        df = pd.DataFrame(line_explanation)

        for y in [y1, y2]:
            i = [y1, y2].index(y)

            for line in y:
                name_i = y.index(line)

                if line not in y1:
                    name_i += len(y1)

                axs[i].plot(df[line], label=names[name_i], color='red', linestyle='dashed')

            axs[i].set_title(names[i])
            axs[i].set_xlabel('Years')
            axs[i].set_ylabel('Medals')
            axs[i].legend()

    plt.title(title, fontsize=16)
    plt.grid(True)
    plt.show()


def generate_random_colour() -> tuple[float, float, float]:
    """ Generates a random tuple of rgb values which will be used for the line colours in the graphs
    """
    rgb = []

    for i in range(3):
        rgb.append(random.randint(0, 255) / 255)

    return rgb[0], rgb[1], rgb[2]

####################################################
# Changes screen background and displays text
####################################################
# Under Construction


def display_info(button_name: str) -> None:
    """ This function is only ever called when a button is clicked.
    The name of the button is given in the function header adn depending on what it is,
    this function changes the screen display accordingly, shows a graph, and prints
    text on the screen (if required)
    """
    # single_plot()

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
sports = Button((0, 255, 0), 100, 650, 'Sport Statistics')
visualize = Button((0, 255, 0), 600, 650, 'Visualize Graph')

# Store buttons in a list
buttons_main = [annual_medals, given_area, gsb, rankings, annual_data, historical, host_effect, team_vs_indi]
buttons_main.extend([performance, countries, sports, visualize])


def redraw_window():
    """Redraw window"""
    window.fill(background_colour)

    for curr_button in buttons_main:
        curr_button.draw((0, 0, 0))


show_graph = False
run = True
while run:
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
        for button in buttons_main:
            if event.type == pygame.MOUSEBUTTONDOWN and button.is_over(pos):
                display_info(button.text)
                # show_graph = True
            if event.type == pygame.MOUSEMOTION:
                if button.is_over(pos):
                    button.colour = (255, 0, 0)
                else:
                    button.colour = (0, 255, 0)

    # Draws the graph
    # if show_graph:
    #     show_graph = False

    # updates the visuals
    redraw_window()
    pygame.display.update()
