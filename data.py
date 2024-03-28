"""
TODO
"""
from __future__ import annotations

import csv
from typing import Any
import pandas as pd  # remember to install the package pandas! (my version is 2.2.1)

olympics = pd.read_csv("summer.csv")
olympics = olympics.dropna()
olympics = olympics.iloc[1:]  # I REMOVED THE HEADER FOR EASIER GRAPH LOAD
olympics.to_csv('summer_modified.csv')


country_codes = pd.read_csv("country_codes.csv")
country_codes = country_codes[['Region Name_en (M49)', 'Country or Area_en (M49)', 'ISO-alpha3 Code (M49)']]
country_codes = country_codes.dropna()
country_codes = country_codes.iloc[1:]  # I REMOVED THE HEADER FOR EASIER GRAPH LOAD
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

    def add_edge(self, item1: Any, item2: Any, sport: Sport) -> None:
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

    def __init__(self) -> None:
        """Initialize."""
        self.num_g = 0
        self.num_s = 0
        self._num_b = 0

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

    """
    graph = Graph()

    country_dict = {}  # will be {isocode: (countryname, region)}
    with open(countries, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            country_dict[row[3]] = (row[2], row[1])

    with open(olympic_games, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            graph.add_vertex(country_dict[row[6]][0], 'country')
            graph.add_vertex(country_dict[row[6]][1], 'region')
            graph.add_vertex(row[1], 'year')
            # We still need to find a way to
            graph.add_edge(country_dict[row[6]][0], row[1], Sport())
            group = find_group(groups, row[3])

            graph.add_edge(row[0], country_dict[row[1]])
    return graph


def find_group(groups: dict[str, str], sport: str) -> str:
    """Return the group (team or individual) that the sport belongs to.
    Note: the parameter groups has the form of {sportname: kind}, in which kind is either 'team' or 'individual'
    Representation Invariants:
        - sport in groups
    """
    return groups[sport]
