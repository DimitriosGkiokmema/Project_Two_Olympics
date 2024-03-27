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
        - self.kind in {'year', 'country'}
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


class Graph:
    """A graph used to represent a book review network.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any, kind: str) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'year', 'country'}
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, kind)

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
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
