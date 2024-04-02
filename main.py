""" This file is used for displaying graphs and the pygame window to the user
Anything visual used in our project is in this file
This includes buttons, graphs, and images

Additionally, this file also deals with mouse and key inputs
Reference for button: https://www.youtube.com/watch?v=4_9twnEduFA
"""
import random
import sys

import data
import math
import pygame
import matplotlib.pyplot as plt
import pandas as pd

pygame.init()

screen_width = 1200
screen_height = 750
# background_colour = (125, 235, 255)
background_colour = pygame.image.load('Olympics Wallpaper.jpg')
background_colour = pygame.transform.scale(background_colour, (screen_width, screen_height))


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

YEARS = [x for x in range(1896, 2013, 4)]  # EVERY 4 YEARS

####################################################
# Buttons
####################################################


class Button:
    """ template for the buttons"""
    def __init__(self, x, y, text=''):
        self.colour = (208, 206, 206)
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
            window.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y +
                               (self.height / 2 - text.get_height() / 2)))

    def is_over(self, position):
        """Is over"""
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < position[0] < self.x + self.width:
            if self.y < position[1] < self.y + self.height:
                return True

        return False

####################################################
# Making the graphs
####################################################


def single_plot(names: list[str], title: str, bar: bool, style: str, y: list[list[int]], x: list[int]):
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


def two_plots(names: list[str], title: str, bar: list, s: str, y1: list[int], y2: list[int], x: list = 0):
    """ An instance of this class requires the graph name, y and (optionally) the x values. x and y MUST be lists
    This class will display one or two graphs on the same window, depending on how many are needed

    Instance Attributes:
        - names: a list containing the title of each graph
        - title: the title to display at the top of the window
        - bar: a list of bools representing the type of graph, True if a bar graph, False if a line graph
        - s: many or single lined graph. Same as style variable from above function
        - y: a list of y coordinates
        - x: a list of x coordinates. If nothing is entered for it, the x coordinates are every num 1940-2020

    Representation Invariants:
        - len(names) > 0
        - s in ['many', 'single']
        - len(y) == len(x) or x == 0
        - if a value is given for x cords, then y must have the same number of values
    """
    x1 = x[0]
    x2 = x[1]

    if s == 'single':  # Two graphs with one line
        fig, axs = plt.subplots(1, 2)

        if not bar[0]:
            axs[0].plot(x1, y1, color=generate_random_colour())
        else:
            axs[0].bar(x=x1, height=y1, color=generate_random_colour())

        if not bar[1]:
            axs[1].plot(x2, y2, color=generate_random_colour())
        else:
            axs[1].bar(x=x2, height=y2, color=generate_random_colour())

        # Putting details on first graph
        axs[0].set_title(names[0])  # Sets graph title
        axs[0].set_xlabel('Years')  # Sets x-axis title
        axs[0].set_ylabel('Medals')  # Sets y-axis title

        # Putting details on second graph
        axs[1].set_title(names[1])  # Sets graph title
        axs[1].set_xlabel('Years')  # Sets x-axis title
        axs[1].set_ylabel('Medals')  # Sets y-axis title
    elif s == 'many':  # Two graphs with  multiple lines
        fig, axs = plt.subplots(1, 2)

        if bar[0]:
            axs[0].bar(x=x1, height=y1, color=generate_random_colour())
        else:
            axs[0].plot(x1, y1, label=names[0], color=generate_random_colour())

        if bar[1]:
            axs[1].bar(x=x2, height=y2, color=generate_random_colour())
        else:
            axs[1].plot(x2, y2, label=names[1], color=generate_random_colour())

        for i in range(2):
            axs[i].set_title(names[i])
            axs[i].set_xlabel('Years')
            axs[i].set_ylabel('Medals')
            axs[i].legend()

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
# Shows graphs and displays text
####################################################
# Under Construction


def display_info(button_name: str) -> None:
    """ This function is only ever called when a button is clicked.
    The name of the button is given in the function header adn depending on what it is,
    this function changes the screen display accordingly, shows a graph, and prints
    text on the screen (if required)
    """
    # single_plot()
    # if button_name == 'Annual Medals':
    # elif button_name == 'Given Area':
    # elif button_name == 'Gold, Silver, and Bronze':
    # elif button_name == 'Rank':
    # elif button_name == 'Annual Data':
    # elif button_name == 'Impact of Historical Events':
    if button_name == 'Host Effect':
        question = 'Enter a country to see its Host Effect: '
        country = get_user_response(question).title()
        cords = graph.host_wins(country)  # [{year_hosted, num of wins}, {year_played: num of wins}]

        if not isinstance(cords, str):
            print(cords)
            x1 = [year for year in cords[0]]
            x2 = [year for year in cords[1]]
            y1 = [cords[0][win] for win in cords[0]]
            y2 = [cords[1][win] for win in cords[1]]
            title = 'Host Country Effect'
            names = ['Wins Hosted by Country', 'Wins When Country Participated']
            two_plots(names, title, [True, False], 'single', y1, y2, [x1, x2])
        else:
            print(cords)

    # elif button_name == 'Team vs Individual Sports':
    # elif button_name == 'Performance':
    # elif button_name == 'Country Statistics':
    # elif button_name == 'Sport Statistics':
    # elif button_name == 'Visualize Graph':


def get_user_response(question: str) -> str:
    """ Displays a new window that asks for user input, then returns that input"""
    # Set up the colors
    black = (0, 0, 0)
    gray = (255, 255, 255)

    # Set up the font
    font = pygame.font.Font(None, 32)

    # Set up the input box
    input_box = pygame.Rect(screen_width // 2 - 100, screen_height // 2, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    response = ''

    # Set up the question
    question = font.render(question, True, black)
    question_rect = question.get_rect(center=(screen_width // 2, screen_height // 2 - 50))

    # Main loop
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active flag.
                    active = not active
                else:
                    active = False
                # Change the color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        response = text
                        text = ''
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        # Render the input box
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width

        # Blit everything to the screen
        window.fill(gray)
        pygame.draw.rect(window, color, input_box, 2)
        window.blit(question, question_rect)
        window.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.display.flip()

    redraw_window()
    return response

####################################################
# Game loop
####################################################


# Create buttons
annual_medals = Button(100, 50, 'Annual Medals')
given_area = Button(600, 50, 'Given Area')
gsb = Button(100, 170, 'Gold, Silver, and Bronze')
rankings = Button(600, 170, 'Rank')
annual_data = Button(100, 290, 'Annual Data')
historical = Button(600, 290, 'Impact of Historical Events')
host_effect = Button(100, 410, 'Host Effect')
team_vs_indi = Button(600, 410, 'Team vs Individual Sports')
performance = Button(100, 530, 'Performance')
countries = Button(600, 530, 'Country Statistics')
sports = Button(100, 650, 'Sport Statistics')
visualize = Button(600, 650, 'Visualize Graph')

# Store buttons in a list
buttons_main = [annual_medals, given_area, gsb, rankings, annual_data, historical, host_effect, team_vs_indi]
buttons_main.extend([performance, countries, sports, visualize])


def redraw_window():
    """Redraw window"""
    window.blit(background_colour, (0, 0))

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
            if event.type == pygame.MOUSEMOTION:
                if button.is_over(pos):
                    button.colour = (255, 0, 0)
                else:
                    button.colour = (208, 206, 206)

    # updates the visuals
    redraw_window()
    pygame.display.update()
