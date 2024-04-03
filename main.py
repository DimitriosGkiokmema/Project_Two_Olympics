""" This file is used for displaying graphs and the pygame window to the user
Anything visual used in our project is in this file
This includes buttons, graphs, and images

Additionally, this file also deals with mouse and key inputs
Reference for button: https://www.youtube.com/watch?v=4_9twnEduFA
"""
import random
import numpy as np
import data
import pygame
import matplotlib.pyplot as plt
import pandas as pd
import project2_visualization as vis

pygame.init()

screen_width = 1200
screen_height = 750
# background_image = (125, 235, 255)
back_button_image = pygame.image.load('back_button.png')
back_button_image = pygame.transform.scale(back_button_image, (50, 50))
background_image = pygame.image.load('Olympics Wallpaper.jpg')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

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

####################################################
# Buttons
####################################################


class Button:
    """ template for the buttons"""
    def __init__(self, x, y, text='', image=None):
        self.colour = (208, 206, 206)
        self.x = x
        self.y = y
        self.text = text
        self.image = image

        if image == back_button_image:
            self.width = 50
            self.height = 50
        else:
            self.width = 450
            self.height = 80

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
        else:
            window.blit(self.image, (self.x, self.y))

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


def plot_word(names: list[str], bar: list[bool], x: list[list[int]], x_names: list[list[str]], y: list[list[int]]):
    x1 = np.array(x[0])
    y1 = np.array(y[0])

    if len(x) == 2:
        fig, axs = plt.subplots(1, 2)

        if bar[0]:
            axs[0].bar(x=x1, height=y1, tick_label=x_names[0], color=generate_random_colour())
        else:
            axs[0].plot(x1, y1, tick_label=x_names[0], color=generate_random_colour())

        x2 = np.array(x[1])
        y2 = np.array(y[1])
        if bar[1]:
            axs[1].bar(x=x2, height=y2, tick_label=x_names[1], color=generate_random_colour())
        else:
            axs[1].plot(x2, y2, tick_label=x_names[1], color=generate_random_colour())

        for i in range(len(x)):
            axs[i].set_title(names[i])
            axs[i].set_ylabel('Medals')
    else:
        plt.xticks(x[0], x_names[0])
        plt.bar(x[0], y[0])
        plt.title(names[0])
        plt.ylabel('Medals')

    plt.show()


def horizontal_bar_graph(name: str, x_names: list[str], y: list[int]) -> None:
    """ Unlike the above graph functions, this function displays a vertical bar graph """
    # Create a horizontal bar graph
    plt.barh(x_names, y, color=generate_random_colour())

    # Customize labels and title
    plt.xlabel('Medals')
    plt.ylabel('Regions')
    plt.title(name)

    # Show the plot
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
    if button_name == 'Annual Medals':
        question = 'Enter the year you want to see the number of medals awarded: '
        year = int(get_user_response(question))
        medals = graph.medal_number_in_year(year)

        if medals == 0:
            output = 'There were no medals awarded that year'
        else:
            output = f'In {year}, {medals} medals were awarded!'

        display_text(output)
    elif button_name == 'Given Area':
        question = 'Enter the location you want to see the number of medals awarded overtime: '
        location = get_user_response(question)
        medals = graph.medal_number_location(location)

        if medals == ValueError:
            output = f'There were no medals ever awarded in {location}'
        else:
            output = f'In {location}, {medals} medals were awarded!'

        display_text(output)
    elif button_name == 'Gold, Silver, and Bronze':
        question1 = 'Enter the first country you want to compare: '
        question2 = 'Enter a country you want to compare the first to: '
        question3 = 'Enter the year the two countries participated in the Olympics'
        country1 = get_user_response(question1)
        country2 = get_user_response(question2)
        year = int(get_user_response(question3))
        output = graph.compare_medals(country1, country2, year)

        if len(output) > 1:
            nums = extract_integers(output)
            names = [country1 + "'s Medals", country2 + "'s Medals"]
            y1 = [nums[0], nums[1], nums[2]]
            y2 = [nums[3], nums[4], nums[5]]
            y = [y1, y2]
            x = ['gold', 'silver', 'bronze']
            bar = [True, True]
            plot_word(names, bar, [[1, 2, 3], [1, 2, 3]], [x, x], y)
        else:
            display_text(f'In {year}, {country1} and {country2} never participated together!')
    elif button_name == 'Rank':
        # SHOW COUNTRY NAME
        year = int(get_user_response('Enter the year: '))
        rank = int(get_user_response('Enter the desired rank: '))
        output = graph.i_th_place(rank, year)
        name = f'Country at ith place in {year}'

        if 'Invalid' not in output:
            y = [i[1] for i in output]
            x = [1, 2, 3]
            x_name = ['Gold', 'Silver', 'Bronze']
            plot_word([name], [True], [x], [x_name], [y])
        else:
            display_text(output)
    elif button_name == 'Annual Data':
        country = get_user_response('Enter the country you would like to see data for: ')
        year = int(get_user_response('Enter the year: '))
        output = graph.annual_data_sentence(country, year)
        display_text(output)
    elif button_name == 'Impact of Historical Events':
        question1 = 'Enter a start year (within known years): '
        start_year = int(get_user_response(question1))
        question2 = 'Enter an end year (within known years): '
        end_year = int(get_user_response(question2))
        x1 = graph.years_during(start_year, end_year)
        x2 = graph.years_during(start_year, end_year)
        y1 = graph.medal_all_years(x1[0], x1[-1])
        y2 = graph.participation_all_years(x2[0], x2[-1])
        title = "World's Medal and Participation over years"
        names = ["Total Number of Medals", "Total Number of Participants"]
        two_plots(names, title, [False, False], 'single', y1, y2, [x1, x2])
    elif button_name == 'Host Effect':
        # ps = 'Click the back button to proceed (we know that its not ideal)'
        # display_text(ps)
        # # HELP ME CONTINUE CONSTRUCTING IT
        # question1 = 'Enter a start year (within known years): '
        # start_year = get_user_response(question1)
        # question2 = 'Enter an end year (within known years): '
        # end_year = get_user_response(question2)
        question = 'Enter a country to see its Host Effect: '
        country = get_user_response(question)
        output = graph.host_wins(country)  # [{year_hosted, num of wins}, {year_played: num of wins}]

        if not isinstance(output, str):
            x1 = [year for year in output[0]]
            x2 = [year for year in output[1]]
            y1 = [output[0][win] for win in output[0]]
            y2 = [output[1][win] for win in output[1]]
            title = 'Host Country Effect'
            names = ['Medals Won When Hosted by Country', 'Total Medals Won']
            two_plots(names, title, [True, False], 'single', y1, y2, [x1, x2])
        else:
            display_text(output)
    elif button_name == 'Team vs Individual Sports':
        question = 'Enter a country to compare Team and Individual Sports scores: '
        country = get_user_response(question)
        output = graph.wins_multiple(country)

        x1 = [year for year in range(1896, 2013, 4)]
        x2 = [year for year in range(1896, 2013, 4)]
        y1 = output[0]
        y2 = output[1]
        title = 'Weighted Scores by Medals Awarded'
        names = ['Team Sports', 'Individual Sports']
        two_plots(names, title, [True, True], 'single', y1, y2, [x1, x2])
    elif button_name == 'Performance':
        perform = graph.performance()
        print(perform)
        x_names = []
        y = []
        for key in perform:
            x_names.append(key)
            y.append(perform[key])
        text = ('There are a lot of regions / countries in this graph.\n'
                'To view it more clearly, click the magnifying glass\n'
                'symbol and draw a rectangle in the graph to zoom in.\n'
                '(Click the back arrow to see the graph)')
        display_text(text)
        horizontal_bar_graph('Performance of regions and countries', x_names, y)
    # elif button_name == 'Country Statistics':
    #   participation_all_years
    # elif button_name == 'Sport Statistics':
    #   sport_flow
    if button_name == 'Visualize Graph':
        vis.visualize_graph(graph)


def extract_integers(text: str) -> list[int]:
    """Extracts all integers from the input text."""
    # Initialize an empty list to store integers
    result = []
    current_number = ""

    # Iterate through each character in the text
    for char in text:
        if char.isdigit():
            # If the character is a digit, add it to the current number
            current_number += char
        elif current_number:
            # If the character is not a digit and we have a current number,
            # convert it to an integer and add it to the result list
            result.append(int(current_number))
            current_number = ""

    # Add the last number (if any) to the result
    if current_number:
        result.append(int(current_number))

    assert len(result[1:]) == 6
    return result[1:]


def display_text(txt: str) -> None:
    """ Text is given and this function displays it on the pygame window"""
    # Create a font object
    font = pygame.font.Font('freesansbold.ttf', 32)
    text_colour = (255, 255, 0)
    background_colour = (0, 0, 128)
    window.fill((255, 255, 255))

    # Split the input text into separate lines
    lines = txt.split('\n')

    # Create a list to store text surfaces
    text_surfaces = []

    # Render each line of text
    for line in lines:
        text_surface = font.render(line, True, text_colour, background_colour)
        text_surfaces.append(text_surface)

    # Calculate total height of all text surfaces
    total_height = sum(surface.get_height() for surface in text_surfaces)

    # Position text surfaces vertically
    y_position = (screen_height - total_height) // 2
    for surface in text_surfaces:
        text_rect = surface.get_rect(center=(screen_width // 2, y_position))
        window.blit(surface, text_rect)
        y_position += surface.get_height()

    back_button = buttons_main[len(buttons_main) - 1]

    show_txt = True
    while show_txt:
        back_button.draw((0, 0, 0))
        position = pygame.mouse.get_pos()
        for action in pygame.event.get():
            if action.type == pygame.QUIT:
                show_txt = False
                pygame.quit()
            if action.type == pygame.MOUSEBUTTONDOWN and back_button.is_over(position):
                show_txt = False
        pygame.display.update()

    redraw_window()


def get_user_response(question: str) -> str:
    """ Displays a new window that asks for user input, then returns that input"""
    # Set up the colors
    black = (0, 0, 0)
    gray = (208, 206, 206)

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
    return response.title()

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
back = Button(screen_width - 55, 5, image=back_button_image)

# Store buttons in a list
buttons_main = [annual_medals, given_area, gsb, rankings, annual_data, historical, host_effect, team_vs_indi]
buttons_main.extend([performance, countries, sports, visualize, back])


def redraw_window():
    """Redraw window"""
    window.blit(background_image, (0, 0))

    for curr_button in buttons_main[:len(buttons_main) - 1]:
        curr_button.draw((0, 0, 0))


# print('performance: ', graph.performance())
print(graph.compare_medals('Greece', 'France', 1896))
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
