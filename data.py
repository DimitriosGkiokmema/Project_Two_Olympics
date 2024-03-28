"""
TODO
"""
from __future__ import annotations

import csv
from typing import Any
import pandas as pd  # remember to install the package pandas! (my version is 2.2.1)

olympics = pd.read_csv("summer.csv")
olympics = olympics.dropna()
olympics.to_csv('summer_modified.csv')


country_codes = pd.read_csv("country_codes.csv")
country_codes = country_codes[['Region Name_en (M49)', 'Country or Area_en (M49)', 'ISO-alpha3 Code (M49)']]
country_codes.dropna()
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

    def i_th_place(self, place: int, year: int):
        """ Ranking (which country, continent, or region ranked the ith place for the number of
        (gold/silver/bronze/total) medals in the given year?)

        {score, country}
        Psuedocode:
        - loop through dict of countries connected to the year
        - for each country, access its Sport and count its Medals
        - to count medals, iterate through indi and team dicts, use dict.i.total_medals to get [g, s, b]
        - add g, s, b values to this function's dicts
        """
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

            gold[country] = g
            silver[country] = s
            bronze[country] = b



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


####################################################################################################################
def load_graph(olympic_games: str, countries: str) -> Graph:
    """ Return a Summer Olympic Medal Graph.
    The input for olympic_games is 'summer_modified.csv', and the input for countries is
    'country_codes_modified.csv'.

    """
    graph = Graph()
    book_dict = {}
    with open(olympic_games, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            book_dict[row[0]] = row[1]

    with open(countries, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            graph.add_vertex(row[0], 'user')
            graph.add_vertex(book_dict[row[1]], 'book')
            graph.add_edge(row[0], book_dict[row[1]])
    return graph
