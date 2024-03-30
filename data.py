"""
TODO
"""
from __future__ import annotations

import csv
from typing import Any
import pandas as pd  # remember to install the package pandas! (my version is 2.2.1)

olympics = pd.read_csv("summer.csv")
olympics = olympics.dropna()
# Renamed some sports to have consistent names
olympics.loc[olympics['Discipline'] == 'Beach volley.', 'Discipline'] = 'Beach Volleyball'
olympics.loc[olympics['Discipline'] == 'BMX', 'Discipline'] = 'Cycling BMX'
olympics.loc[olympics['Discipline'] == 'Modern Pentath.', 'Discipline'] = 'Modern Pentathlon'
olympics.loc[olympics['Discipline'] == 'Artistic G.', 'Discipline'] = 'Gymnastics Artistic'
olympics.loc[olympics['Discipline'] == 'Rhythmic G.', 'Discipline'] = 'Gymnastics Rhythmic'
olympics.loc[olympics['Discipline'] == 'Synchronized S.', 'Discipline'] = 'Synchronized Swimming'
olympics.loc[olympics['Discipline'] == 'Water polo', 'Discipline'] = 'Water Polo'
olympics.loc[olympics['Discipline'] == 'Wrestling Free.', 'Discipline'] = 'Wrestling Freestyle'
olympics.loc[olympics['Discipline'] == 'Water Motorspor', 'Discipline'] = 'Water Motorsport'
# Convert back to the csv file
olympics.to_csv('summer_modified.csv')


country_codes = pd.read_csv("country_codes.csv")
country_codes = country_codes[['Region Name_en (M49)', 'Country or Area_en (M49)', 'ISO-alpha3 Code (M49)']]
country_codes = country_codes.dropna()
country_codes.to_csv('country_codes_modified.csv')


class _Vertex:
    """A vertex in a book review graph, used to represent a user or a book.

    Each vertex item is either a user id or book title. Both are represented as strings,
    even though we've kept the type annotation as Any to be consistent with lecture.

    Instance Attributes:
        - item: The data stored in this vertex, representing a user or book.
        - kind: The type of this vertex: 'user' or 'book'.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'year', 'country', 'region'}  # Amy added region to this RI !?
    """
    item: Any
    kind: str
    neighbours: set[_Vertex]

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'year', 'country'}
        """
        self.item = item
        self.kind = kind
        self.neighbours = set()


class _SportVertex(_Vertex):
    """A vertex representing the weight of sports and medals.
    Instance Attributes:
        - item: The data stored in this vertex, representing a year, country, or region.
        - kind: The type of this vertex: 'year', 'country', or 'region'.
        - neighbours: The vertices that are adjacent to this vertex, and their corresponding
            edge weights.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'year', 'country', 'region'}
    """
    item: Any
    kind: str
    neighbours: dict[_SportVertex, Sport]

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'year', 'country', 'region'}
        """
        super().__init__(item, kind)
        self.neighbours = {}


class Graph:
    """A graph used to represent a book review network.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _SportVertex]  # Amy changed this into _SportVertex !?

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any, kind: str) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'year', 'country', 'region'}
        """
        if item not in self._vertices:
            self._vertices[item] = _SportVertex(item, kind)

    def add_edge(self, item1: Any, item2: Any, sport: Sport = None) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            v1.neighbours[v2] = sport
            v2.neighbours[v1] = sport
        else:
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'year', 'country'}
        """
        if kind != '':
            return {v.item for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.keys())

    ##################################################################################
    # Our additional methods
    ##################################################################################

    def i_th_place(self, year: int) -> list[dict[str, int]] | str:
        """ Ranking (which country, continent, or region ranked the ith place for the number of
        (gold/silver/bronze/total) medals in the given year?)

        Pseudocode:
        - loop through dict of countries connected to the year
        - for each country, access its Sport and count its Medals
        - to count medals, iterate through indi and team dicts, use dict.i.total_medals to get [g, s, b]
        - add g, s, b values to this function's dicts
        """
        if year not in [year.item for year in self._vertices]:
            return 'Invalid input for year'

        gold = {}
        silver = {}
        bronze = {}

        for country in self._vertices[year].neighbours:
            sport = self._vertices[year].neighbours[country]
            g, s, b = 0, 0, 0

            # Records the number of total medals won in team sports
            for team_sport in sport.team_sports:
                medals = sport.team_sports[team_sport]
                g += medals.num_g
                s += medals.num_s
                b += medals.num_b

            # Records the number of total medals won in individual sports
            for individual_sport in sport.team_sports:
                medals = sport.team_sports[individual_sport]
                g += medals.num_g
                s += medals.num_s
                b += medals.num_b

            # Records the number of medals in dicts
            gold[country.item] = g
            silver[country.item] = s
            bronze[country.item] = b

        return [gold, silver, bronze]

    def compare_medals(self, country1: str, country2: str, year: int) -> str:
        """Compare the number of Gold, Silver, and Bronze medals between two countries for a specific year.
        Return a string summarizing the comparison of medals between the two countries.

            country1 : The name of the first country.
            country2 : The name of the second country.
            year : The year for which to compare the medals.
        """
        try:
            # Get the annual data for both countries
            country1_data = self.annual_data_dict(country1, year)
            country2_data = self.annual_data_dict(country2, year)

            # Extract medal counts for each country
            country1_gold = country1_data.get('total medals', 0)
            country1_silver = country1_data.get('team medals', 0)
            country1_bronze = country1_data.get('indiv medals', 0)

            country2_gold = country2_data.get('total medals', 0)
            country2_silver = country2_data.get('team medals', 0)
            country2_bronze = country2_data.get('indiv medals', 0)

            # Generate the comparison summary string
            comparison_summary = f"Comparison of Medals in {year}:\n"
            comparison_summary += f"{country1}:\n"
            comparison_summary += f"Gold: {country1_gold}, Silver: {country1_silver}, Bronze: {country1_bronze}\n"
            comparison_summary += f"{country2}:\n"
            comparison_summary += f"Gold: {country2_gold}, Silver: {country2_silver}, Bronze: {country2_bronze}\n"

            return comparison_summary
        except ValueError as e:
            return str(e)

##################################################################################
# Our additional methods
##################################################################################
    def get_edge(self, item1: Any, item2: Any) -> Sport:
        """Return the Sport class of that edge if item1 and item2 are adjacent and are in the graph.
        Raise ValueError otherwise."""
        if item1 in self._vertices and item2 in self._vertices and self.adjacent(item1, item2):
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]
            return v1.neighbours[v2]

    def update_sport(self) -> None:
        """Update sport, as we want to add more sport data into the edge during load_graph."""

    def annual_data_sentence(self, country: str, year: int) -> None:
        """Print out annual data based on user's input about a country name and a year.
        Annual data includes:
        - total number of sports
        - number of team sports and individual sports that country participated in
        - total number of medals, and number of kind of medals
        """
        if country in self._vertices and year in self._vertices:
            v_country = self._vertices[country]
            v_year = self._vertices[year]
            if v_country not in v_year.neighbours:  # or vice versa
                print(f"Unfortunately, {country} didn't attend or didn't achieve any medals in {year}."
                      f"Please try looking for other data.")
            else:
                sport_data = v_country.neighbours[v_year]  # type Sport

                print(f"In {year}, {country} participated and had medals on {sport_data.total_num_sport()} sports,\n"
                      f"including {sport_data.total_num_sport('team')} team sports and "
                      f"{sport_data.total_num_sport('individual')} sports. \n In terms of the number of medals, "
                      f"{country} in that year has achieved the total of {sport_data.total_medal()} medals, with \n"
                      f"{sport_data.total_medal('team')} medals on team sports and the other "
                      f"{sport_data.total_medal('individual')} on individuals.")
        else:
            print(f"Something went wrong. Please check your input and try again.")

    def annual_data_dict(self, country: str, year: int) -> Any:
        """Return the annual data of a country in a specific year, dimilar to annual_data_sentence, but presented as
        a dictionary for further code usage.
        The dictionary will have the form like:
        {'total sports': ..., 'team sports': ..., 'indiv sports': ..., 'total medals': ..., 'team medals':...,
        'indiv medals': ...}

        Raise ValueError when country or year are not in self._vertices.
        If the country didn't participate in Summer Olympics that year, do nothing.
        """
        if country in self._vertices and year in self._vertices:
            v_country = self._vertices[country]
            v_year = self._vertices[year]

            if v_country in v_year.neighbours:
                sport_data = v_country.neighbours[v_year]
                return {'total sports': sport_data.total_num_sport(),
                        'team sports': sport_data.total_num_sport('team'),
                        'indiv sports': sport_data.total_num_sport('individual'),
                        'total medals': sport_data.total_medal(),
                        'team medals': sport_data.total_medal('team'),
                        'indiv medals': sport_data.total_medal('individual')}
        else:
            raise ValueError


class Medal:
    """A place to store number of medals for a given edge (which country - in which year - on which sport).
    Instance Attributes:
        - num_g: Number of gold medals for that edge
        - num_s: Number of silver medals for that edge
        - num_b: Number of bronze medals for that edge
    """
    num_g: int
    num_s: int
    num_b: int

    def __init__(self, g: int = 0, s: int = 0, b: int = 0) -> None:
        """Initialize."""
        self.num_g = g
        self.num_s = s
        self._num_b = b

    def add_medal(self, kind: str, num: int = 1) -> None:
        """Add a medal with the given kind. The default is 1 medal per time added."""
        if kind == 'Gold':
            self.num_g += num
        elif kind == 'Silver':
            self.num_s += num
        elif kind == 'Bronze':
            self.num_b += num
        else:  # Should not reach this branch
            raise ValueError

    def total_medal(self) -> int:
        """Return the total number of medals."""
        return sum([self.num_g, self.num_s, self.num_b])

    def weighted_score(self) -> int:
        """Calculate weighted score according to the number of medals.
        Each gold medal worths 3 points.
        Each silver medal worths 2 points
        Each bronze medal worths 1 point."""
        return 3 * self.num_g + 2 * self.num_s + self.num_b


class Sport:
    """A class storing the sports that a country partook as the key, and the medals they got at that sport in
    that year. Here we divided into group kind of sports: team sports and individual sports.
    Instance Attributes:
        - team_sports: A dictionary that matches a team sport name to its achievement, representing as the class Medal.
        - individual_sports: A dictionary that matches an individual sport name to its achievement, representing
        as the class Medal.
    """
    team_sports: dict[str, Medal]
    individual_sports: dict[str, Medal]

    def __init__(self) -> None:
        """Initialize"""
        self.team_sports = {}
        self.individual_sports = {}

    def add_sport(self, name: str, kind: str, medals: Medal) -> None:
        """Add new sport into this collection. Do nothing if the sport has already in here.
        Representation Invariants:
            - kind in {'team', 'individual'}
        """
        if kind == 'team' and name not in self.team_sports:
            self.team_sports[name] = medals
        elif kind == 'individual' and name not in self.individual_sports:
            self.individual_sports[name] = medals

    def update_medal(self, name: str, kind_sport: str, kind_medal: str, num: int = 1) -> None:
        """Update number of medal into existing Medal.
        Representation Invariants:
            - name in {self.team_sports, self.individual_sports}
            - kind_sport in {'team', 'individual'}
        """
        if kind_sport == 'team':
            self.team_sports[name].add_medal(kind_medal, num)
        else:
            self.individual_sports[name].add_medal(kind_medal, num)

    def total_medal(self, kind: str = '') -> int:
        """Return the total number of medals for all sports, according to whether kind is team or individual.
        If kind is left blanked, return total medals from both groups.
        Representation Invariants:
            - kind in {'', 'team', 'individual'}
        """
        if kind == '':
            total_team_medals = sum([medal.total_medal for medal in self.team_sports.values()])
            total_indi_medals = sum([medal.total_medal for medal in self.individual_sports.values()])
            return total_team_medals + total_indi_medals
        elif kind == 'team':
            return sum([medal.total_medal for medal in self.team_sports.values()])
        else:  # kind == 'individual'
            return sum([medal.total_medal for medal in self.individual_sports.values()])

    def total_num_sport(self, kind: str = '') -> int:
        """Return the total number of sports according to the kind (either team or individual).
        If kind is left blanked, return total sports from both groups.
        However, there is a flaw that a sport might be double counted. For example, tennis, which can be played
        individually or as a team, could be potentially counted twice if it appeared in both groups.
        Representation Invariants:
            - kind in {'', 'team', 'individual'}
        """
        if kind == '':
            return len(self.individual_sports) + len(self.team_sports)
        elif kind == 'team':
            return len(self.team_sports)
        else:
            return len(self.individual_sports)


####################################################################################################################
def load_graph(olympic_games: str, countries: str, groups: dict[str, str]) -> Graph:
    """ Return a Summer Olympic Medal Graph.
    The input for olympic_games is 'summer_modified.csv', and the input for countries is
    'country_codes_modified.csv'.

    countries format: Region Name,Country or Area, Code
    olympic_games format: Year,City,Sport,Discipline,Athlete,Country,Gender,Event,Medal

    Graph: _vertices: dict[Any, _SportVertex]
    _SportVertex:   item: Any
                    kind: str
                    neighbours: dict[_SportVertex, Sport]
    Sport:  team_sports: dict[str, Medal]
            individual_sports: dict[str, Medal]
    Medal:  num_g: int
            num_s: int
            num_b: int
    """
    graph = Graph()

    country_dict = {}  # will be {isocode: (countryname, region)}
    with open(countries, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip the first header line
        for row in reader:
            country_dict[row[3]] = (row[2], row[1])

    with open(olympic_games, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip the first header line
        for row in reader:
            graph.add_vertex(country_dict[row[6]][0], 'country')
            graph.add_vertex(country_dict[row[6]][1], 'region')
            graph.add_vertex(row[1], 'year')
            # We still need to find a way to
            # Have: edge - Sport class -> Sport - Medal class

            # Add edge for country and its corresponding region
            graph.add_edge(country_dict[row[6]][0], country_dict[row[6]][1])

            # Add new edge (empty Sport) if not already adjacent
            if not graph.adjacent(country_dict[row[6]][0], row[1]):
                graph.add_edge(country_dict[row[6]][0], row[1], Sport())

            # Update Sport
            sport_class = graph.get_edge()
            group = find_group(groups, row[4])

            # Check to access the sport name if available, or create new key if not.
            if row[4] not in sport_class.team_sports and row[4] not in sport_class.individual_sports:
                # Create new medal
                if row[9] == 'Gold':
                    new_medal = Medal(g=1)
                elif row[9] == 'Silver':
                    new_medal = Medal(s=1)
                else:
                    new_medal = Medal(b=1)
                sport_class.add_sport(row[4], group, new_medal)
            else:
                # Add new data to medal
                sport_class.update_medal(row[4], group, row[9])

    return graph


def find_group(groups: dict[str, str], sport: str) -> str:
    """Return the group (team or individual) that the sport belongs to.
    Note: the parameter groups has the form of {sportname: kind}, in which kind is either 'team' or 'individual'
    Note: 0 means 'individual', and 1 means 'team'!!
    Representation Invariants:
        - sport in groups
    """
    if groups[sport] == 0:
        return 'individual'
    else:
        return 'team'


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
