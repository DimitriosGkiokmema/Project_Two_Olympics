"""CSC111 Project 2: The Analysis of Summer Olympics Through External Effects (1896 - 2012)
AMY IS MAKING IT TO BECOME A NEW MAIN.PY SO THAT THE FUNCTIONS WILL BE HIDDEN AND THE USER CAN HAVE BETTER EXPERIENCES?
"""
import data
import pygame
from main import Button, display_info, redraw_window
if __name__ == "__main__":
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
             'Mountain Bike': 1, 'Polo': 1, 'Rackets': 0, 'Roque': 0, 'Rowing': 1, 'Rugby': 1, 'Sailing': 1,
             'Shooting': 0,
             'Softball': 1, 'Swimming': 0, 'Synchronized Swimming': 1, 'Table Tennis': 0, 'Taekwondo': 0, 'Tennis': 0,
             'Trampoline': 0, 'Triathlon': 0, 'Tug of War': 1, 'Vaulting': 0, 'Volleyball': 1, 'Water Motorsport': 1,
             'Water Polo': 1, 'Weightlifting': 0, 'Wrestling Freestyle': 0, 'Wrestling Gre-R': 0}

    graph = data.load_graph('summer_modified.csv', 'country_codes_modified.csv', group)

    YEARS = [x for x in range(1940, 2013)]

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
