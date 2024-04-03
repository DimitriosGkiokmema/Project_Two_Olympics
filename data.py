"""
CSC111 Project 2: The Analysis of Summer Olympics Through External Effects (1896 - 2012)
"""
from __future__ import annotations
from typing import Any, List, Tuple
import csv
import networkx as nx
import pandas as pd  # remember to install the package pandas! (my version is 2.2.1)


CITIES = ['Athens', 'Paris', 'St Louis', 'London', 'Stockholm', 'Antwerp', 'Amsterdam', 'Beijing', 'Los Angeles',
          'Berlin', 'Helsinki', 'Melbourne / Stockholm', 'Rome', 'Tokyo', 'Mexico', 'Munich', 'Montreal', 'Moscow',
          'Seoul', 'Barcelona', 'Atlanta', 'Sydney']
COUNTIES = ['Greece', 'France', 'United States of America', 'England', 'Sweden', 'Belgium', 'Netherlands', 'China',
            'United States of America', 'Germany', 'Finland', 'Australia / Germany', 'Italy', 'Japan', 'Mexico',
            'Germany', 'Canada', 'Russia', 'South Korea', 'Spain', 'United States of America', 'Australia']
CITY_TO_COUNTRY = {CITIES[i]: COUNTIES[i] for i in range(len(CITIES))}


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
        - host: if this vertex is a year, this is the country that held the Olympics at that year. '' if not year
        - neighbours: The vertices that are adjacent to this vertex, and their corresponding
            edge weights.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'year', 'country', 'region'}
    """
    item: Any
    kind: str
    host: str
    neighbours: dict[_SportVertex, Sport]

    def __init__(self, item: Any, kind: str, host: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'year', 'country', 'region'}
        """
        super().__init__(item, kind)
        self.host = host
        self.neighbours = {}

    def get_years(self) -> list[int]:
        """Return a list of year vertices that this vertex is adjacent to, in ascending order."""
        lst_yr = []
        for y in self.neighbours:
            if y.kind == 'year':
                lst_yr.append(y.item)
        return sorted(lst_yr)

    def get_neighbours(self, kind: str = '') -> list:
        """Return a list of _SportVertex according to the input kind."""
        if kind != '':
            return [v for v in self.neighbours if v.kind == kind]
        else:
            return [v for v in self.neighbours]


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

    def add_vertex(self, item: Any, kind: str, host: str) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'year', 'country', 'region'}
        """
        if item not in self._vertices:
            self._vertices[item] = _SportVertex(item, kind, host)

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
            - kind in {'year', 'country', 'region'}
        """
        if kind != '':
            return {v.item for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.keys())

    ##################################################################################
    # Our additional methods
    ##################################################################################

    def to_networkx(self, max_vertices: int = 5000) -> nx.Graph:
        """Convert this graph into a networkx Graph.

        max_vertices specifies the maximum number of vertices that can appear in the graph.
        (This is necessary to limit the visualization output for large graphs.)

        Note that this method is provided for you, and you shouldn't change it.
        """
        graph_nx = nx.Graph()
        for v in self._vertices.values():
            graph_nx.add_node(v.item, kind=v.kind)

            for u in v.neighbours:
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.item, kind=u.kind)

                if u.item in graph_nx.nodes:
                    graph_nx.add_edge(v.item, u.item, sport=v.neighbours[u])

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx

    def i_th_place(self, i: int, year: int) -> list[tuple[Any, int]] | str:
        """ Ranking (which country, continent, or region ranked the ith place for the number of
        (gold/silver/bronze/total) medals in the given year?)

        Pseudocode:
        - loop through dict of countries connected to the year
        - for each country, access its Sport and count its Medals
        - to count medals, iterate through indi and team dicts, use dict.i.total_medals to get [g, s, b]
        - add g, s, b values to this function's dicts

        Graph: _vertices: dict[Any, _SportVertex]
        _SportVertex:   item: Any
                        kind: str
                        host: str
                        neighbours: dict[_SportVertex, Sport]
        Sport:  team_sports: dict[str, Medal]
                individual_sports: dict[str, Medal]
        Medal:  num_g: int
                num_s: int
                num_b: int
        """
        if year not in self._vertices:
            return 'Invalid input for year'

        gold = []
        silver = []
        bronze = []

        for vertex in self._vertices[year].neighbours:
            if self._vertices[year].neighbours[vertex] is not None:
                medals = self.rank_helper(year, vertex)

                # Records the number of medals in dicts
                gold.append((vertex.item, medals[0]))
                silver.append((vertex.item, medals[1]))
                bronze.append((vertex.item, medals[2]))

        if i < len(gold):
            insertion_sort(gold)
            insertion_sort(silver)
            insertion_sort(bronze)
            return [gold[len(gold) - i], silver[len(silver) - i], bronze[len(bronze) - i]]
        else:
            num_participants = len(self._vertices[year].neighbours)
            return f'Invalid rank; only {num_participants} countries participated in the {year} Olympic games'

    def rank_helper(self, year: int, vertex: _SportVertex) -> list[int]:
        """ This is a helper function for rank (above)
        Given a Sport object, this function returns the total number of medals for that sport."""
        g, s, b = 0, 0, 0

        # Records the number of total medals won in team sports
        for team_sport in self._vertices[year].neighbours[vertex].team_sports:
            medals = self._vertices[year].neighbours[vertex].team_sports[team_sport]
            g += medals.num_g
            s += medals.num_s
            b += medals.num_b

        # Records the number of total medals won in individual sports
        for individual_sport in self._vertices[year].neighbours[vertex].individual_sports:
            medals = self._vertices[year].neighbours[vertex].individual_sports[individual_sport]
            g += medals.num_g
            s += medals.num_s
            b += medals.num_b

        return [g, s, b]

    def host_wins(self, country: str) -> list[dict[Any, int]] | str:
        """ This function returns a dict in the format [{year_hosted, num of wins}, {year_played: num of wins}]
        If the inputted country never held the Olympics, a message stating this is returned
        """
        is_host = False
        host_medals = {}

        for year in self._vertices:
            if self._vertices[year].kind == 'year' and self._vertices[year].host == country:
                is_host = True
                for participant in self._vertices[year].neighbours:
                    self.add_to_host_medals(year, country, participant, host_medals)

        if is_host:
            return [host_medals, self.host_wins_helper(country)]
        else:
            return 'The given country has never hosted the Olympics!'

    def add_to_host_medals(self, year: Any, country: str, participant: _SportVertex, host_medals: dict[int, int]):
        """ This is a helper for the function above.
        It calculates the total medals for a country at a specific year,
        and assigns it to the host_medals by mutating host_medals
        """
        if participant.kind == 'country' and participant.item == country:
            medals = self._vertices[year].neighbours[participant].total_medal()
            host_medals[int(self._vertices[year].item)] = medals

    def host_wins_helper(self, country: str) -> dict[Any, int]:
        """ Searches the Graph for the years the given country participated in the Olympics and returns
        the medals awarded to the country at each year it participated (but not hosted!)
        """
        played_medals = {}

        for year in self._vertices[country.title()].neighbours:
            if self._vertices[year.item].kind == 'year':
                played_medals[int(year.item)] = 0

                for participant in year.neighbours:
                    # if participant.item == country:
                    #     medals = year.neighbours[participant].total_medal()
                    #     played_medals[int(year.item)] = medals
                    self.add_to_played_medals(year, country, participant, played_medals)
                # played_medals =

        return played_medals

    def add_to_played_medals(self, year: Any, country: str, participant: _SportVertex, played_medals: dict[int, int]):
        """ This is a helper for the function above.
        It calculates the total medals for a country at a specific year,
        and assigns it to the host_medals
        """
        if participant.item == country:
            medals = year.neighbours[participant].total_medal()
            played_medals[int(year.item)] = medals

    def compare_medals(self, country1: str, country2: str, year: int) -> Any:
        """Compare the number of Gold, Silver, and Bronze medals between two countries for a specific year.
        Return a tuple of two lists [num_g, num_s, num_b] for each country, if they participated together that year.
        Otherwise, return None. If any of these inputs is not in this graph items, also return None.

            country1: The name of the first country.
            country2: The name of the second country.
            year: The year for which to compare the medals.
        """
        if country1 in self._vertices and country2 in self._vertices and year in self._vertices:
            if self.adjacent(country1, year) and self.adjacent(country2, year):
                sport1, sport2 = self.get_edge(country1, year), self.get_edge(country2, year)
                return sport1.medals_by_kind(), sport2.medals_by_kind()
            else:
                return None
        else:
            return None

    def compare_medal(self, country1: str, country2: str, year: int) -> str:
        """Compare the number of Gold, Silver, and Bronze medals between two countries for a specific year.
        Return a string summarizing the comparison of medals between the two countries.

            country1 : The name of the first country.
            country2 : The name of the second country.
            year : The year for which to compare the medals.
        """
        country1_gold = 0
        country1_silver = 0
        country1_bronze = 0
        country2_gold = 0
        country2_silver = 0
        country2_bronze = 0
        # Get the annual data for both countries
        if country1 in self._vertices and year in self._vertices:
            v_country = self._vertices[country1]
            v_year = self._vertices[year]
            if v_country in v_year.neighbours:
                sport_data = v_country.neighbours[v_year]
                teams = sport_data.team_sports
                for sport in teams:
                    medals = teams[sport]
                    country1_gold += medals.num_g
                    country1_silver += medals.num_s
                    country1_bronze += medals.num_b
        if country2 in self._vertices and year in self._vertices:
            v_country = self._vertices[country1]
            v_year = self._vertices[year]
            if v_country in v_year.neighbours:
                sport_data = v_country.neighbours[v_year]
                teams = sport_data.team_sports
                for sport in teams:
                    medals = teams[sport]
                    country2_gold += medals.num_g
                    country2_silver += medals.num_s
                    country2_bronze += medals.num_b
        # Generate the comparison summary string
        comparison_summary = f"Comparison of Medals in {year}:\n"
        comparison_summary += f"{country1}:\n"
        comparison_summary += f"Gold: {country1_gold}, Silver: {country1_silver}, Bronze: {country1_bronze}\n"
        comparison_summary += f"{country2}:\n"
        comparison_summary += f"Gold: {country2_gold}, Silver: {country2_silver}, Bronze: {country2_bronze}\n"

        return comparison_summary

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
        else:
            raise ValueError

    def years_during_selected(self, start: int, end: int) -> list[int]:  # AMY CHANGED THE NAME
        """Return a list of years that are expected to have Olympics games, from the first year (min year)
        to the end year (max year) recorded in this graph. That means we record the year from
        range(min_year, max_year + 1, 4).
        Secial years when the Olympics was cancelled (1916, 1940, 1944) still count to this list.

        Representation Invariants:
            - There must be at least one 'year' vertex in this graph.
        """
        # This is Amy's original code, I changed it to start and end at select years
        # all_years = self.get_all_vertices('year')
        # min_year, max_year = min(all_years), max(all_years)
        lst_year = []
        for y in range(start, end, 4):
            lst_year.append(y)
        return lst_year
        # lst_year = []
        # for y in range(start, end + 1, 4):
        #     lst_year.append(y)
        # return lst_year

    def years_during(self) -> list:
        """Return a list of years that are expected to have Olympics games, from the first year (min year)
        to the end year (max year) recorded in this graph. That means we record the year from
        range(min_year, max_year + 1, 4).
        Secial years when the Olympics was cancelled (1916, 1940, 1944) still count to this list.

        Representation Invariants:
            - There must be at least one 'year' vertex in this graph.
        """
        all_years = self.get_all_vertices('year')
        min_year, max_year = min(all_years), max(all_years)
        lst_year = []
        for y in range(min_year, max_year + 1, 4):
            lst_year.append(y)
        return lst_year

    def annual_data_sentence(self, country: str, year: int) -> str:
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

                return (f"In {year}, {country} participated and had medals on {sport_data.total_num_sport()} sports,\n"
                        f"including {sport_data.total_num_sport('team')} team sports and "
                        f"{sport_data.total_num_sport('individual')} individual sports. \n In terms of the number of "
                        f"medals, {country} in that year \nhas achieved the total of \n{sport_data.total_medal()} "
                        f"medals, with {sport_data.total_medal('team')} medals on team sports and \n the other"
                        f"{sport_data.total_medal('individual')} medals earned individually.")
        else:
            return 'Something went wrong. Please check your input and try again.'

    def performance(self) -> dict:
        """Returns the average rate of change of medals weight starting from the start year of participation to the last
         year of participation for all the countries in a dictionary.
        """
        countries = []
        for key in self._vertices:
            vertex = self._vertices[key]
            if vertex.kind == 'country':
                countries.append(vertex.item)
        country_wise_performance = {}
        for country in countries:
            years_participated = []
            sum_of_change = 0
            v_country = self._vertices[country]
            for vertice in v_country.neighbours:
                if vertice.kind == 'year':
                    years_participated.append(vertice.item)
            years_participated.sort()
            prev_medals_weight = 0
            for year in years_participated:
                v_year = self._vertices[year]
                sport_data = v_country.neighbours[v_year]
                curr_weight = sport_data.total_scores()
                sum_of_change += (curr_weight - prev_medals_weight)
                prev_medals_weight = curr_weight
            country_wise_performance[country] = sum_of_change / len(years_participated)
        return country_wise_performance

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
                return
        else:
            raise ValueError

    def medal_number_in_year(self, input_year: int) -> int:
        """
        Computes the number of medals in the given year (= input_year).
        """
        # Raises ValueError if the input_year is not in the Graph.
        if input_year not in self._vertices:
            return 0  # AMY CHANGED THIS
        else:

            # Follows an accumulator pattern.
            medals_so_far = 0

            v_year = self._vertices[input_year]

            countries = v_year.get_neighbours('country')

            for country in countries:
                sport = self.get_edge(input_year, country.item)
                # Counts separately the number of medal achieved in team_sport and individual_sport.
                for team_sport in sport.team_sports:
                    medals_so_far += sport.team_sports[team_sport].total_medal()

                for individual_sport in sport.team_sports:
                    medals_so_far += sport.team_sports[individual_sport].total_medal()

            return medals_so_far

    def medal_number_location(self, input_location: str) -> int:
        """
        Computes the number of medals in the input_location overtime.
        Whenever the input_location is not in self, raise ValueError.
        """
        if input_location not in self._vertices:
            raise ValueError
        else:

            # Follows an accumulator pattern.
            medals_so_far = 0
            for year in self._vertices[input_location].neighbours:
                sport = self._vertices[year].neighbours[year]

                # Counts separatedly the number of medal achieved in team_sport and individual_sport.
                for team_sport in sport.team_sports:
                    medals_so_far += sport.team_sports[team_sport].total_medal()
                for individual_sport in sport.team_sports:
                    medals_so_far += sport.team_sports[individual_sport].total_medal()
        return medals_so_far

############################################################################################
# About historical events
###########################################################################################

    def participation_in_year(self, input_year: int) -> int:
        """Return the number of countries participated in the Summer Olympic in a given year.
        In other words, count the number of countries that the input_year vertex """
        if input_year not in self._vertices:  # the key, as the load_graph, is str
            return 0
        else:
            v_year = self._vertices[input_year]
            count = 0
            for vertex in v_year.neighbours:
                if vertex.kind == 'country':
                    count += 1

            return count

    def medal_all_years(self, start_year: int, end_year: int) -> list:
        """Return the total number of medals for each year from start_year to end_year, INCLUSIVE"""
        selected_years = []
        for y in range(start_year, end_year + 1, 4):
            selected_years.append(self.medal_number_in_year(y))

        return selected_years

    def weight_in_year(self, input_year: int) -> int:
        """Return the weighted score of medals in the given year."""
        if input_year not in self._vertices:
            return 0
        else:
            v_year = self._vertices[input_year]
            count = 0
            countries = v_year.get_neighbours('country')
            for country in countries:
                sport = self.get_edge(input_year, country.item)
                count += sport.total_scores()

            return count

    def participation_all_years(self, start_year: int, end_year: int) -> list:
        """Return the total number of countries participated in each year from start_year to end_year, INCLUSIVE"""
        selected_years = []
        for y in range(start_year, end_year + 1, 4):  # Since Olympics happens every 4 years.
            selected_years.append(self.participation_in_year(y))

        return selected_years

    def medal_overall_average(self) -> float | int:
        """Return the overall average number of medals for all years between the first recorded year and the last
        recorded year. Rounded to the second decimal place.
        Notice: Still need to count the year with no medals. For example our data has two years: 2013, and 2015 with
        the number of medals respectively are 20,10. Although the vertice 2014 isn't shown in the graph, it is still
        between the start and end years, so we still need to count the year 2014, to make the average to be
        (20 + 0 + 10) / 3, not (20 + 10) / 2.
        """
        all_years = self.get_all_vertices('year')
        min_year, max_year = min({year.item for year in all_years}), max({year.item for year in all_years})
        total = sum(self.medal_all_years(min_year, max_year))
        return round(total / (max_year - min_year + 1), 2)

    def medal_period_average(self, start_year: int, end_year: int) -> float | int:
        """Return the period average number of medals from start_year to end_year, INCLUSIVE. Rounded to the
        second decimal place.
        Representation Invariants:
            - start_year and end_year must be among [min_year, max_year] recorded in the dataset.
        """
        total = sum(self.medal_all_years(start_year, end_year))
        return round(total / (end_year - start_year + 1), 2)

    def sport_flow(self, start_year: int, end_year: int) -> dict[int, int]:
        """Return the total number of sports for each year from start_year to end_year, INCLUSIVE.
        If there is a year that is not included in self, it will be represented with sports number 0."""
        years_flow = {}
        for y in range(start_year, end_year + 1, 4):
            sport_number = 0
            if y in self._vertices:
                for country in self._vertices[y].neighbours:
                    sport_number += len(self._vertices[y].neighbours[country].team_sports) + len(
                        self._vertices[y].neighbours[country].team_sports)
            years_flow[y] = sport_number
        return years_flow

    def participation_overall_average(self) -> float | int:
        """Return the overall average number of participants for all years between the first recorded year and the
        last recorded year. Rounded to the second decimal place.
        Similar notice as medal_overall_average.
        """
        all_years = self.get_all_vertices('year')
        min_year, max_year = min({year.item for year in all_years}), max({year.item for year in all_years})
        total = sum(self.participation_all_years(min_year, max_year))
        return round(total / (max_year - min_year + 1), 2)

    def participation_period_average(self, start_year: int, end_year: int) -> float | int:
        """Return the period average number of participants from start_year to end_year, INCLUSIVE. Rounded to the
        second decimal place.
        Representation Invariants:
            - start_year and end_year must be among [min_year, max_year] recorded in the dataset."""
        total = sum(self.participation_all_years(start_year, end_year))
        return round(total / (end_year - start_year + 1), 2)

#######################################################
    def wins_one(self, year: int, country: str) -> tuple:
        """Return the total scores, calculated from the weighted number of medals achieved by a country in year, in the
        category of team sports and individual sports, respectively.
        """
        if self.adjacent(year, country):
            v_country = self._vertices[country]
            v_year = self._vertices[year]
            sport_data = v_country.neighbours[v_year]

            # Calculate team sports first
            team_so_far = 0
            for medal in sport_data.team_sports.values():
                team_so_far += medal.weighted_score()
            # Then calculate individual sports
            indiv_so_far = 0
            for medal in sport_data.individual_sports.values():
                indiv_so_far += medal.weighted_score()

            return team_so_far, indiv_so_far
        else:
            return 0, 0

    def wins_multiple(self, country: str) -> tuple[list, list]:
        """Return the total scores, calculated from the weighted number of medals achieved by a country throughout the
        recorded period, in the category of team sports and individual sports, respectively. The first list in the
        returned tuple will be for team, and the other one is for individual.
        """
        team = []
        indiv = []
        all_years = self.get_all_vertices('year')
        min_year, max_year = min(all_years), max(all_years)
        for i in range(min_year, max_year + 1, 4):  # Since we want the max_year inclusive
            one = self.wins_one(i, country)
            team.append(one[0])
            indiv.append(one[1])
        return team, indiv

##########################################
# For Region: compute the total number of medals gained in each year (bar), as well as the percentage from the world's
# total number of medals (line), displayed on the same graph. Do a similar thing for the total weighted scores.
##########################################
    def medal_year_by_region(self, year: int, region: str) -> int:
        """Return the number of medals gained in the given region in that year. It means that we only choose countries
        which are adjacent to that region instead of traversing through all country neighbours of that year.
        Representation Invariants:
            - region in self.get_all_vertices('region')
        """
        if year not in self._vertices:
            return 0
        else:
            all_countries = self._vertices[year].get_neighbours('country')
            medal_so_far = 0
            for country in all_countries:
                if self.adjacent(country, region):
                    medal_so_far += self.get_edge(year, country).total_medal()

            return medal_so_far

    def weight_year_by_region(self, year: int, region: str) -> int:
        """Returng the weight of medals gained in the given region in that year. It means that we only choose countries
        which are adjacent to that region instead of traversing through all country neighbours of that year.
        Representation Invariants:
            - region in self.get_all_vertices('region')
        """
        if year not in self._vertices:
            return 0
        else:
            all_countries = self._vertices[year].get_neighbours('country')
            weight_so_far = 0
            for country in all_countries:
                if self.adjacent(country, region):
                    weight_so_far += self.get_edge(year, country).total_scores()

            return weight_so_far

    def total_medal_by_region(self, region: str) -> tuple[list, list] | str:
        """
        Return a tuple of 2 lists: the first list contains the total number of medals gained in the given region in
        each year, and the second one contains the percentage of number of medals gained here to the world's total.
        The time period is from the min year to the max year recorded in this graph.
        If the region input is not valid, return a message.
        """
        if region not in self.get_all_vertices('region'):
            return 'Region not found. Please check your input.'
        else:
            v_region = self._vertices[region]
            year_neighbours = v_region.get_neighbours('year')

            number = []
            percentage = []

            for yr in self.years_during():
                if yr not in year_neighbours:  # Might be redundant, but just to ensure everything goes right
                    number.append(0)
                    percentage.append(0)
                else:
                    medal_this_region = self.medal_year_by_region(yr, region)
                    medal_world = self.medal_number_in_year(yr)  # It must not be 0, since as soon as this year exists
                    # in this region, there is at least one country took part in that year.
                    number.append(medal_this_region)
                    percentage.append(medal_this_region / medal_world)

            return number, percentage

    def weight_by_region(self, region: str) -> tuple[list, list] | str:
        """
        Return a tuple of 2 lists: the first list contains the weighted score gained in the given region in each year,
        and the second one contains the percentage of weighted score gained here to the world's total. The time period
        is from the min year to the max year recorded in this graph.
        If the region input is not valid, return a message.
        """
        if region not in self.get_all_vertices('region'):
            return 'Region not found. Please check your input.'
        else:
            v_region = self._vertices[region]
            year_neighbours = v_region.get_neighbours('year')

            weight = []
            percentage = []

            for yr in self.years_during():
                if yr not in year_neighbours:  # Might be redundant, but just to ensure everything goes right
                    weight.append(0)
                    percentage.append(0)
                else:
                    weight_this_region = self.weight_year_by_region(yr, region)
                    weight_world = self.weight_in_year(yr)  # It must not be 0, since as soon as this year exists
                    # in this region, there is at least one country took part in that year.
                    weight.append(weight_this_region)
                    percentage.append(weight_this_region / weight_world)

            return weight, percentage


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
        self.num_b = b

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
            total_team_medals = sum([medal.total_medal() for medal in self.team_sports.values()])
            total_indi_medals = sum([medal.total_medal() for medal in self.individual_sports.values()])
            return total_team_medals + total_indi_medals
        elif kind == 'team':
            return sum([medal.total_medal() for medal in self.team_sports.values()])
        else:  # kind == 'individual'
            return sum([medal.total_medal() for medal in self.individual_sports.values()])

    def total_scores(self, kind: str = '') -> int:
        """Return the total number of weighted medals for all sports, according to whether kind is team of individual.
        If kind is left blanked, return towal weighted scores of medals for both groups.
        Representation Invariants:
            - kind in {'team', 'individual'}
        """
        if kind == '':
            total_team_scores = sum([medal.weighted_score() for medal in self.team_sports.values()])
            total_indi_scores = sum([medal.weighted_score() for medal in self.individual_sports.values()])
            return total_indi_scores + total_team_scores
        elif kind == 'team':
            return sum([medal.weighted_score() for medal in self.team_sports.values()])
        else:
            return sum([medal.weighted_score() for medal in self.individual_sports.values()])

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

    def medals_by_kind(self) -> list[int]:
        """Return the list of total number of medals by kind (Gold, Silver, Bronze)."""
        gold = 0
        silver = 0
        bronze = 0
        for medal in self.team_sports.values():
            gold += medal.num_g
            silver += medal.num_s
            bronze += medal.num_b
        for medal in self.individual_sports.values():
            gold += medal.num_g
            silver += medal.num_s
            bronze += medal.num_b
        return [gold, silver, bronze]


def insertion_sort(lst: list[tuple[str, int]]) -> None:
    """ Helper for i_th_place function.
    Takes in a list of format [(country, medals)] and sorts it in terms of medals
    Note that this is a *mutating* function.
    """
    for i in range(0, len(lst)):
        j = i
        while not (j == 0 or lst[j - 1][1] <= lst[j][1]):
            # Swap lst[j - 1] and lst[j]
            lst[j - 1], lst[j] = lst[j], lst[j - 1]

            j -= 1


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
                    host: str
                    neighbours: dict[_SportVertex, Sport]
    Sport:  team_sports: dict[str, Medal]
            individual_sports: dict[str, Medal]
    Medal:  num_g: int
            num_s: int
            num_b: int
    """
    graph = Graph()

    country_dict = {}  # will be {isocode: (countryname, region)}
    with open(countries, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # skip the first header line
        for row in reader:
            country_dict[row[3]] = (row[2], row[1])

    with open(olympic_games, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # skip the first header line
        for row in reader:
            yr = int(row[1])
            graph.add_vertex(country_dict[row[6]][0], 'country', '')
            graph.add_vertex(country_dict[row[6]][1], 'region', '')
            graph.add_vertex(yr, 'year', CITY_TO_COUNTRY[row[2]])
            # We still need to find a way to
            # Have: edge - Sport class -> Sport - Medal class

            # Add edge for country and its corresponding region
            graph.add_edge(country_dict[row[6]][0], country_dict[row[6]][1])
            graph.add_edge(yr, country_dict[row[6]][1])

            # Add new edge (empty Sport) if not already adjacent
            if not graph.adjacent(country_dict[row[6]][0], yr):
                graph.add_edge(country_dict[row[6]][0], yr, Sport())

            if not graph.adjacent(country_dict[row[6]][1], yr):
                graph.add_edge(country_dict[row[6]][1], yr, Sport())

            # Update Sport
            sport_class = graph.get_edge(country_dict[row[6]][0], yr)  # get edge with that country and that year
            grp = find_group(groups, row[4])

            # Check to access the sport name if available, or create new key if not.
            if row[4] not in sport_class.team_sports and row[4] not in sport_class.individual_sports:
                # Create new medal
                if row[9] == 'Gold':
                    new_medal = Medal(g=1)
                elif row[9] == 'Silver':
                    new_medal = Medal(s=1)
                else:
                    new_medal = Medal(b=1)
                sport_class.add_sport(row[4], grp, new_medal)
            else:
                # Add new data to medal
                sport_class.update_medal(row[4], grp, row[9])

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


if __name__ == '__main__':

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
    # Rename countries to be consistent with country_codes
    olympics.loc[olympics['Country'] == 'GRE', 'Country'] = 'GRC'
    olympics.loc[olympics['Country'] == 'GER', 'Country'] = 'DEU'
    olympics.loc[olympics['Country'] == 'DEN', 'Country'] = 'DNK'
    olympics.loc[olympics['Country'] == 'SUI', 'Country'] = 'CHE'
    olympics.loc[olympics['Country'] == 'NED', 'Country'] = 'NLD'
    olympics.loc[olympics['Country'] == 'RSA', 'Country'] = 'ZAF'
    olympics.loc[olympics['Country'] == 'POR', 'Country'] = 'PRT'
    olympics.loc[olympics['Country'] == 'URU', 'Country'] = 'URY'
    olympics.loc[olympics['Country'] == 'HAI', 'Country'] = 'HTI'
    olympics.loc[olympics['Country'] == 'PHI', 'Country'] = 'PHL'
    olympics.loc[olympics['Country'] == 'CHI', 'Country'] = 'CHL'
    olympics.loc[olympics['Country'] == 'LAT', 'Country'] = 'LVA'
    olympics.loc[olympics['Country'] == 'SRI', 'Country'] = 'LKA'
    olympics.loc[olympics['Country'] == 'PUR', 'Country'] = 'PRI'
    olympics.loc[olympics['Country'] == 'IRI', 'Country'] = 'IRN'
    olympics.loc[olympics['Country'] == 'TRI', 'Country'] = 'TTO'
    olympics.loc[olympics['Country'] == 'BUL', 'Country'] = 'BGR'
    olympics.loc[olympics['Country'] == 'LIB', 'Country'] = 'LBN'
    olympics.loc[olympics['Country'] == 'BAH', 'Country'] = 'BHS'
    olympics.loc[olympics['Country'] == 'SIN', 'Country'] = 'SGP'
    olympics.loc[olympics['Country'] == 'NGR', 'Country'] = 'NGA'
    olympics.loc[olympics['Country'] == 'MGL', 'Country'] = 'MNG'
    olympics.loc[olympics['Country'] == 'NIG', 'Country'] = 'NER'
    olympics.loc[olympics['Country'] == 'BER', 'Country'] = 'BMU'
    olympics.loc[olympics['Country'] == 'TAN', 'Country'] = 'TZA'
    olympics.loc[olympics['Country'] == 'ZIM', 'Country'] = 'ZWE'
    olympics.loc[olympics['Country'] == 'ZAM', 'Country'] = 'ZMB'
    olympics.loc[olympics['Country'] == 'ALG', 'Country'] = 'DZA'
    olympics.loc[olympics['Country'] == 'CRC', 'Country'] = 'CRI'
    olympics.loc[olympics['Country'] == 'INA', 'Country'] = 'IDN'
    olympics.loc[olympics['Country'] == 'ISV', 'Country'] = 'VGB'
    olympics.loc[olympics['Country'] == 'EUN', 'Country'] = 'URS'  # Actually 2 different team but still in Soviet
    olympics.loc[olympics['Country'] == 'MAS', 'Country'] = 'MYS'
    olympics.loc[olympics['Country'] == 'CRO', 'Country'] = 'HRV'
    olympics.loc[olympics['Country'] == 'SLO', 'Country'] = 'SVK'
    olympics.loc[olympics['Country'] == 'TGA', 'Country'] = 'TON'
    olympics.loc[olympics['Country'] == 'BAR', 'Country'] = 'BRB'
    olympics.loc[olympics['Country'] == 'KSA', 'Country'] = 'SAU'
    olympics.loc[olympics['Country'] == 'KUW', 'Country'] = 'KWT'
    olympics.loc[olympics['Country'] == 'VIE', 'Country'] = 'VNM'
    olympics.loc[olympics['Country'] == 'PAR', 'Country'] = 'PRY'
    olympics.loc[olympics['Country'] == 'UAE', 'Country'] = 'ARE'
    olympics.loc[olympics['Country'] == 'SUD', 'Country'] = 'SDN'
    olympics.loc[olympics['Country'] == 'MRI', 'Country'] = 'MUS'
    olympics.loc[olympics['Country'] == 'TOG', 'Country'] = 'TGO'
    olympics.loc[olympics['Country'] == 'GUA', 'Country'] = 'GTM'
    olympics.loc[olympics['Country'] == 'GRN', 'Country'] = 'GRD'
    olympics.loc[olympics['Country'] == 'BOT', 'Country'] = 'BWA'

    # Convert back to a new csv file
    olympics.to_csv('summer_modified.csv')

    country_codes = pd.read_csv("country_codes.csv")
    country_codes = country_codes[['Region Name_en (M49)', 'Country or Area_en (M49)', 'ISO-alpha3 Code (M49)']]
    country_codes = country_codes.dropna()
    country_codes.reset_index(inplace=True, drop=True)
    country_codes.loc[len(country_codes.index)] = ['World', 'International Olympic Committee Mixed teams', 'ZZX']
    country_codes.loc[len(country_codes.index)] = ['Europe', 'Bohemia', 'BOH']
    country_codes.loc[len(country_codes.index)] = ['Oceania', 'Australasia', 'ANZ']
    country_codes.loc[len(country_codes.index)] = ['Europe', 'Russian Empire', 'RU1']
    country_codes.loc[len(country_codes.index)] = ['Europe', 'Czechoslovakia', 'TCH']
    country_codes.loc[len(country_codes.index)] = ['Europe', 'Yugoslavia', 'YUG']
    country_codes.loc[len(country_codes.index)] = ['Europe', 'Soviet Union', 'URS']
    country_codes.loc[len(country_codes.index)] = ['Europe', 'United Team of Germany', 'EUA']
    country_codes.loc[len(country_codes.index)] = ['Americas', 'British West Indies', 'BWI']
    country_codes.loc[130] = ['Asia', 'Chinese Taipei', 'TPE']
    country_codes.loc[len(country_codes.index)] = ['Europe', 'East Germany', 'GDR']
    country_codes.loc[len(country_codes.index)] = ['Europe', 'West Germany', 'FRG']
    country_codes.loc[len(country_codes.index)] = ['Europe', 'Netherlands Antilles', 'AHO']
    country_codes.loc[len(country_codes.index)] = ['World', 'Independent Olympic Participants', 'IOP']
    country_codes.loc[len(country_codes.index)] = ['Europe', 'Serbia and Montenegro', 'SCG']
    # Convert back to a new csv file
    country_codes.to_csv('country_codes_modified.csv')

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

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['csv', 'networkx', 'pandas'],  # the names (strs) of imported modules
        'allowed-io': ['print', 'open', 'input'],     # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
