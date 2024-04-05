""" This file is used for displaying graphs and the pygame window to the user
Anything visual used in our project is in this file
This includes buttons, graphs, and images

Additionally, this file also deals with mouse and key inputs
Reference for button: https://www.youtube.com/watch?v=4_9twnEduFA
"""
import random
import numpy as np
import pygame
import matplotlib.pyplot as plt
import project2_visualization as vis
import data

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750
BACK_BUTTON_IMAGE = pygame.image.load('back_button.png')
BACK_BUTTON_IMAGE = pygame.transform.scale(BACK_BUTTON_IMAGE, (50, 50))
BACKGROUND_IMAGE = pygame.image.load('Olympics Wallpaper.jpg')
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('CSC111 Project 2: The Analysis of Summer Olympics Through External Effects')

GROUP = {'Archery': 0, 'Athletics': 0, 'Badminton': 0, 'Baseball': 1, 'Basketball': 1, 'Basque Pelota': 1,
         'Beach Volleyball': 1, 'Boxing': 0, 'Canoe / Kayak F': 0, 'Canoe / Kayak S': 0, 'Canoe Slalom': 0,
         'Canoe Sprint': 1, 'Cricket': 1, 'Croquet': 0, 'Cycling BMX': 0, 'Cycling Road': 0, 'Cycling Track': 0,
         'Diving': 0, 'Dressage': 0, 'Eventing': 0, 'Fencing': 0, 'Figure skating': 0, 'Football': 1, 'Golf': 0,
         'Gymnastics Artistic': 0, 'Gymnastics Rhythmic': 1, 'Handball': 1, 'Hockey': 1, 'Ice Hockey': 1,
         'Jeu de Paume': 0, 'Judo': 0, 'Jumping': 0, 'Lacrosse': 1, 'Marathon swimming': 0, 'Modern Pentathlon': 0,
         'Mountain Bike': 1, 'Polo': 1, 'Rackets': 0, 'Roque': 0, 'Rowing': 1, 'Rugby': 1, 'Sailing': 1, 'Shooting': 0,
         'Softball': 1, 'Swimming': 0, 'Synchronized Swimming': 1, 'Table Tennis': 0, 'Taekwondo': 0, 'Tennis': 0,
         'Trampoline': 0, 'Triathlon': 0, 'Tug of War': 1, 'Vaulting': 0, 'Volleyball': 1, 'Water Motorsport': 1,
         'Water Polo': 1, 'Weightlifting': 0, 'Wrestling Freestyle': 0, 'Wrestling Gre-R': 0}

GRAPH = data.load_graph('summer_modified.csv', 'country_codes_modified.csv', GROUP)

REGIONS = ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania', 'World']
COUNTRIES = GRAPH.get_all_countries()
YEARS = list(range(1896, 2013, 4))


####################################################
# Buttons
####################################################


class Button:
    """ template for the buttons"""
    def __init__(self, x: int, y: int, text: str = '', image: pygame.Surface = None) -> None:
        self.colour = (208, 206, 206)
        self.x = x
        self.y = y
        self.text = text
        self.image = image

        if image == BACK_BUTTON_IMAGE:
            self.width = 50
            self.height = 50
        else:
            self.width = 450
            self.height = 80

    def draw(self, outline: tuple[int, int, int] = None) -> None:
        """Draw the button on the screen"""
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(WINDOW, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(WINDOW, self.colour, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('calibri', 40)
            text = font.render(self.text, 1, (0, 0, 0))
            WINDOW.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y +
                               (self.height / 2 - text.get_height() / 2)))
        else:
            WINDOW.blit(self.image, (self.x, self.y))

    def is_over(self, position: tuple[int, int]) -> bool:
        """Is over"""
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < position[0] < self.x + self.width:
            if self.y < position[1] < self.y + self.height:
                return True

        return False


####################################################
# Making the graphs
####################################################


def single_plot(names: list[str], title: str, is_bar: list, style: str, y: list[list[int]], x: list[int],
                y_label: str = '') -> None:
    """ An instance of this class requires the GRAPH name, y and (optionally) the x values. x and y MUST be lists
    This class will display a single or multiple graphs on the same window, depending on how many

    Instance Attributes:
        - names: a list containing the title of each graph
        - t: the title to display at the top of the window
        - is_bar: the type of graph, True if a bar GRAPH, False if a line GRAPH
        - style: many or single lined graph
        - y: a list of y coordinates
        - x: a list of x coordinates. If nothing is entered for it, the x coordinates are every num 1896-2012, 4.

    Representation Invariants:
        - len(names) > 0
        - style in ['single', 'many']
        - bar == True or bar == False
        - len(y) == len(x) or x == 0
        - if a value is given for x cords, then y must have the same number of values
    """
    if style == 'many':  # THIS CASE FOR 2 LINES/BARS ONLY
        # Amy modified this case for the "Host Effect" and it works! This will only be used for that button so,
        # although not generalized enough (I guess cuz I just somehow made it worked idk), still be good for one case.
        ax = plt.subplots()[1]

        for i in range(len(y)):
            if is_bar[i]:
                ax.bar(x, y[i], label=names[i], color=generate_random_colour())
            else:
                ax.plot(x, y[i], label=names[i], color=generate_random_colour())

    elif style == 'single':
        if is_bar[0]:
            plt.bar(x=x, height=y[0], color=generate_random_colour())
        else:
            plt.plot(x, y[0], label="My Line", color="blue", linewidth=2)

    # Add legend, axis labels, and title
    plt.ylabel(y_label, fontsize=14)
    plt.xlabel('Years', fontsize=14)
    plt.title(title, fontsize=16)
    plt.grid(True)
    plt.show()


def two_plots(names: list, title: str, is_bar: list, graph_type: str, y1: list[list[int]], y2: list[list[int]],
              x: list = 0) -> None:
    """ An instance of this class requires the GRAPH name, y and (optionally) the x values. x and y MUST be lists
    This class will display one or two graphs on the same window, depending on how many are needed

    Instance Attributes:
        - names: a list containing the title of each GRAPH
        - title: the title to display at the top of the window
        - is_bar: a list of bools representing the type of GRAPH, True if a bar GRAPH, False if a line GRAPH
        - s: many or single lined GRAPH. Same as style variable from above function
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

    if graph_type == 'single':  # Two graphs with one line
        fig, axs = plt.subplots(1, 2)

        if not is_bar[0]:
            axs[0].plot(x1, y1[0], color=generate_random_colour())
        else:
            axs[0].bar(x=x1, height=y1[0], color=generate_random_colour())

        if not is_bar[1]:
            axs[1].plot(x2, y2[0], color=generate_random_colour())
        else:
            axs[1].bar(x=x2, height=y2[0], color=generate_random_colour())

        # Putting details on first GRAPH
        axs[0].set_title(names[0])  # Sets GRAPH title
        axs[0].set_xlabel('Years')  # Sets x-axis title
        axs[0].set_ylabel('Medals')  # Sets y-axis title

        # Putting details on second GRAPH
        axs[1].set_title(names[1])  # Sets GRAPH title
        axs[1].set_xlabel('Years')  # Sets x-axis title
        axs[1].set_ylabel('Medals')  # Sets y-axis title

        fig.canvas.manager.set_window_title(title)
    elif graph_type == 'many':  # Two graphs with  multiple lines
        fig, axs = plt.subplots(1, 2)

        for i in range(len(y1)):
            if is_bar[0][i]:
                axs[0].bar(x=x, height=y1[i], color=generate_random_colour())
            else:
                axs[0].plot(x, y1[i], label=names[0][i], color=generate_random_colour())

        for i in range(len(y2)):
            if is_bar[1][i]:
                axs[1].bar(x=x, height=y2[i], color=generate_random_colour())
            else:
                axs[1].plot(x, y2[i], label=names[0][i], color=generate_random_colour())

        for i in range(2):
            axs[i].set_title(names[i])
            axs[i].set_xlabel('Years')
            axs[i].set_ylabel('Medals')
            axs[i].legend()

        fig.canvas.manager.set_window_title(title)

    plt.grid(True)
    plt.show()


def plot_word(names: list[str], is_bar: list[bool], x: list[list[int]], x_names: list[list[str]], y: list[list[int]])\
        -> None:
    """Plot a graph with the x-axis values being categorical variables (such as countries)."""
    x1 = np.array(x[0])
    y1 = np.array(y[0])

    if len(x) == 2:
        fig, axs = plt.subplots(1, 2)

        if is_bar[0]:
            axs[0].bar(x=x1, height=y1, tick_label=x_names[0], color=generate_random_colour())
        else:
            axs[0].plot(x1, y1, tick_label=x_names[0], color=generate_random_colour())

        x2 = np.array(x[1])
        y2 = np.array(y[1])
        if is_bar[1]:
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
    """ Unlike the above GRAPH functions, this function displays a vertical bar graph """
    # Create a horizontal bar GRAPH
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

    for _ in range(3):
        rgb.append(random.randint(0, 255) / 255)

    return rgb[0], rgb[1], rgb[2]


####################################################
# Shows graphs and displays text
####################################################
# Under Construction


def display_info(button_name: str) -> None:
    """ This function is only ever called when a button is clicked.
    The name of the button is given in the function header adn depending on what it is,
    this function changes the screen display accordingly, shows a GRAPH, and prints
    text on the screen (if required)
    """
    if button_name == 'Annual Medals':
        question = 'Enter the year you want to see the number of medals awarded: '
        year = int(get_user_response(question, 'year'))
        medals = GRAPH.medal_number_in_year(year)

        if medals == 0:
            output = 'There were no medals awarded that year'
        else:
            output = f'In {year}, {medals} medals were awarded!'

        display_text(output)
    elif button_name == 'Given Area':
        question = 'Enter the region you want to see the number of medals awarded overtime: '
        region = get_user_response(question, 'region')
        graph1 = GRAPH.total_medal_by_region(region)  # either a tuple of 2 lists or none
        graph2 = GRAPH.weight_by_region(region)  # either a tuple of 2 lists or none

        if graph1 is not None and graph2 is not None:
            names = ['Medals in ' + region, 'Weighted scores in ' + region]
            x = GRAPH.years_during()  # list of years from the beginning to the end
            y1_bar, y1_line = graph1[0], graph1[1]
            y2_bar, y2_line = graph2[0], graph2[1]
            title = f'{region} Awards'

            two_plots(names, title, [[1, 0], [1, 0]], 'many', [y1_bar, y1_line], [y2_bar, y2_line], x)
        else:
            display_text(f'Region not found. Please check your input.')

    elif button_name == 'Gold, Silver, and Bronze':
        question1 = 'Enter the first country you want to compare: '
        question2 = 'Enter a country you want to compare the first to: '
        question3 = 'Enter the year the two countries participated in the Olympics: '
        country1 = get_user_response(question1, 'country')
        country2 = get_user_response(question2, 'country')
        year = int(get_user_response(question3, 'year'))
        output = GRAPH.compare_medals(country1, country2, year)

        if output is not None:
            names = [country1 + "'s Medals in " + str(year), country2 + "'s Medals in " + str(year)]
            y1 = output[0]
            y2 = output[1]
            y = [y1, y2]
            x = ['gold', 'silver', 'bronze']
            bar = [True, True]
            plot_word(names, bar, [[1, 2, 3], [1, 2, 3]], [x, x], y)
        else:
            display_text(f'In {year}, {country1} and {country2} never participated together!')
    elif button_name == 'Rank':
        year = int(get_user_response('Enter the year: ', 'year'))
        rank = int(get_user_response('Enter the desired rank: ', 'rank'))
        output = GRAPH.i_th_place(rank, year)
        name = f'{output[0]} ranked {rank} in {year}'

        if 'Invalid' not in output:
            y = [output[1], output[2], output[3]]
            x = [1, 2, 3]
            x_name = ['Gold', 'Silver', 'Bronze']
            plot_word([name], [True], [x], [x_name], [y])
        else:
            display_text(output)
    elif button_name == 'Annual Data':
        country = get_user_response('Enter the country you would like to see data for: ', 'country')
        year = int(get_user_response('Enter the year: ', 'year'))
        output = GRAPH.annual_data_sentence(country, year)
        display_text(output)

    elif button_name == 'Impact of Historical Events':
        # Displays graphs
        question1 = 'Enter a start year (within known years): '
        start_year = int(get_user_response(question1, 'year'))
        question2 = 'Enter an end year (within known years): '
        end_year = int(get_user_response(question2, 'year'))

        while start_year > end_year:
            display_text('Start year must be less than end year!')
            start_year = int(get_user_response(question1, 'year'))
            end_year = int(get_user_response(question2, 'year'))

        x1 = GRAPH.years_during_selected(start_year, end_year)
        x2 = GRAPH.years_during_selected(start_year, end_year)
        y1 = GRAPH.medal_all_years(start_year, end_year)
        y2 = GRAPH.participation_all_years(start_year, end_year)
        title = "World's Medal and Participation over years"
        names = ["Total Number of Medals", "Total Number of Participants"]
        two_plots(names, title, [False, False], 'single', [y1], [y2], [x1, x2])

        # Displays analysis
        medal_overall = GRAPH.medal_period_average(start_year, end_year)
        medal_average = GRAPH.medal_overall_average()
        part_overall = GRAPH.participation_overall_average()
        part_average = GRAPH.participation_period_average(start_year, end_year)
        txt = (f'While the average number of medals in the whole period was {medal_overall}, in\n' +
               f'the period from {start_year} to {end_year}, the average number of medals was {medal_average}.\n' +
               f'Therefore, the difference between the two is {round(abs(medal_average - medal_overall), 2)}.\n\n'
               f'While the average number of participation in the whole period was {part_overall}, in the\n' +
               f'period from {start_year} to {end_year}, the average number of participants was {part_average}.\n' +
               f'Therefore, the difference between the two is {round(abs(part_average - part_overall), 2)}.\n\n'
               )
        display_text(txt)

    elif button_name == 'Host Effect':
        question1 = 'Enter a start year (within known years): '
        start = int(get_user_response(question1, 'year'))
        question2 = 'Enter an end year (within known years): '
        end = int(get_user_response(question2, 'year'))

        while start > end:
            display_text('Start year must be less than end year!')
            start = int(get_user_response(question1, 'year'))
            end = int(get_user_response(question2, 'year'))

        question = 'Enter a country to see its Host Effect: '
        country = get_user_response(question, 'country')
        output = GRAPH.host_wins(country, start, end)  # ([wins_hosted], [wins_all])

        if not isinstance(output, str):
            x = list(range(start, end + 1, 4))
            y1, y2 = output[0], output[1]
            title = 'Host Country Effect'
            names = ['Host Years Achievements', 'Overall Achievements']
            single_plot(names, title, [True, False], 'many', [y1, y2], x)
        else:
            display_text(output)

    elif button_name == 'Team vs Individual Sports':
        question = 'Enter a country to compare Team and Individual Sports scores: '
        country = get_user_response(question, 'country')
        output = GRAPH.wins_multiple(country)

        x1 = YEARS
        y1 = output[0]
        y2 = output[1]
        title = 'Weighted Scores by Medals Awarded'
        names = ['Team Sports', 'Individual Sports']
        two_plots(names, title, [True, True], 'single', [y1], [y2], [x1, x1])

    elif button_name == 'Performance':
        perform = GRAPH.performance()
        x_names = []
        y = []
        for key in perform:
            x_names.append(key)
            y.append(perform[key])
        text = ('There are a lot of regions / countries in this GRAPH.\n'
                'To view it more clearly, click the magnifying glass\n'
                'symbol and draw a rectangle in the GRAPH to zoom in.\n'
                '(Click the back arrow to see the GRAPH)')
        display_text(text)
        horizontal_bar_graph('Performance of regions and countries', x_names, y)

    elif button_name == 'Country Statistics':
        question1 = 'Enter the starting year: '
        start = int(get_user_response(question1, 'year'))
        question2 = 'Enter the ending year: '
        end = int(get_user_response(question2, 'year'))

        while start > end:
            display_text('Start year must be less than end year!')
            start = int(get_user_response(question1, 'year'))
            end = int(get_user_response(question2, 'year'))

        y = GRAPH.participation_all_years(start, end)
        x = [year for year in range(start, end + 1, 4)]
        title = 'Change in the Number of Participating Countries'
        single_plot([''], title, [False], 'single', [y], x, 'Number of Countries')

    elif button_name == 'Sport Statistics':
        question1 = 'Enter the starting year: '
        start = int(get_user_response(question1, 'year'))
        question2 = 'Enter the ending year: '
        end = int(get_user_response(question2, 'year'))

        while start > end:
            display_text('Start year must be less than end year!')
            start = int(get_user_response(question1, 'year'))
            end = int(get_user_response(question2, 'year'))

        stats = GRAPH.sport_flow(start, end)
        x = list(stats)
        y = [stats[y] for y in stats]
        title = 'Change in the Number of Sports Played'
        single_plot([''], title, [False], 'single', [y], x, 'Number of Sports')

    elif button_name == 'Visualize Graph':
        vis.visualize_graph(GRAPH)


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
    WINDOW.fill((255, 255, 255))

    # Split the input text into separate lines
    lines = txt.split('\n')

    # Create a list to store text surfaces
    text_surfaces = []

    # Render each line of text
    for line in lines:
        text_surface = font.render(line, True, text_colour, background_colour)
        text_surfaces.append(text_surface)

    # Calculate total height of all text surfaces
    total_height = sum(sf.get_height() for sf in text_surfaces)

    # Position text surfaces vertically
    y_position = (SCREEN_HEIGHT - total_height) // 2
    for surface in text_surfaces:
        text_rect = surface.get_rect(center=(SCREEN_WIDTH // 2, y_position))
        WINDOW.blit(surface, text_rect)
        y_position += surface.get_height()

    back_button = BUTTONS_MAIN[len(BUTTONS_MAIN) - 1]

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


def get_user_response(question: str, return_type: str) -> str:
    """ Displays a new window that asks for user input, then returns that input"""
    # Set up the colors
    black = (0, 0, 0)
    gray = (208, 206, 206)

    # Set up the font
    font = pygame.font.Font(None, 32)

    # Set up the input box
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    response = ''

    # Set up the question
    question = font.render(question, True, black)
    question_rect = question.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

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
                        if return_type == 'region' and isinstance(text, str) and text.title() in REGIONS:
                            response = text
                            text = ''
                            done = True
                        elif return_type == 'country' and isinstance(text, str) and text.title() in COUNTRIES:
                            response = text
                            text = ''
                            done = True
                        elif return_type == 'year' and text.isdigit() and int(text) in YEARS:
                            response = text
                            text = ''
                            done = True
                        elif return_type == 'rank' and text.isdigit() and int(text) > 0:
                            response = text
                            text = ''
                            done = True
                        else:
                            if return_type == 'year':
                                message = 'Please input a valid year from 1896-2012\nthat the Olympics took place!'
                            elif return_type == 'year':
                                message = 'Please input a valid rank of participants\nthat took place in the Olympics!'
                            else:
                                message = ('Please input a valid country / region\n' +
                                           'that participated or hosted the Olympics!')
                            display_text(message)
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        # Render the input box
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width

        # Blit everything to the screen
        WINDOW.fill(gray)
        pygame.draw.rect(WINDOW, color, input_box, 2)
        WINDOW.blit(question, question_rect)
        WINDOW.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.display.flip()

    redraw_window()
    return response.title()


####################################################
# Game loop
####################################################

def create_buttons():
    """ Create Button objects, store them in a list, and return that list"""
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
    back = Button(SCREEN_WIDTH - 55, 5, image=BACK_BUTTON_IMAGE)

    # Store buttons in a list
    buttons_main = [annual_medals, given_area, gsb, rankings, annual_data, historical, host_effect, team_vs_indi]
    buttons_main.extend([performance, countries, sports, visualize, back])

    return buttons_main


BUTTONS_MAIN = create_buttons()


def redraw_window():
    """Redraw window"""
    WINDOW.blit(BACKGROUND_IMAGE, (0, 0))

    for curr_button in BUTTONS_MAIN[:len(BUTTONS_MAIN) - 1]:
        curr_button.draw((0, 0, 0))


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['random', 'numpy', 'data', 'pygame', 'matplotlib.pyplot', 'project2_visualization'],
        'max-line-length': 120
    })
