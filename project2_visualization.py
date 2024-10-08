"""
The visualization of a GRAPH, similar to exercise 4.
"""
import networkx as nx
from plotly.graph_objs import Scatter, Figure
import data

# Colours to use when visualizing different clusters.
COLOUR_SCHEME = [
    '#2E91E5', '#E15F99', '#1CA71C', '#FB0D0D', '#DA16FF', '#222A2A', '#B68100',
    '#750D86', '#EB663B', '#511CFB', '#00A08B', '#FB00D1', '#FC0080', '#B2828D',
    '#6C7C32', '#778AAE', '#862A16', '#A777F1', '#620042', '#1616A7', '#DA60CA',
    '#6C4516', '#0D2A63', '#AF0038'
]

LINE_COLOUR = 'rgb(210,210,210)'
VERTEX_BORDER_COLOUR = 'rgb(50, 50, 50)'
YEAR_COLOUR = 'rgb(89, 205, 105)'
COUNTRY_COLOUR = 'rgb(105, 89, 205)'
REGION_COLOUR = 'rgb(205, 149, 89)'


def setup_graph(graph: data.Graph,
                layout: str = 'spring_layout',
                max_vertices: int = 5000,
                weighted: bool = False) -> list:
    """Use plotly and networkx to setup the visuals for the given GRAPH.

    Optional arguments:
        - weighted: True when weight data should be visualized. Weight in this case is the Sport class in the edge
        between a country and a year it participated.
    """

    graph_nx = graph.to_networkx(max_vertices)

    pos = getattr(nx, layout)(graph_nx)

    x_values = [pos[k][0] for k in graph_nx.nodes]
    y_values = [pos[k][1] for k in graph_nx.nodes]
    labels = list(graph_nx.nodes)

    if weighted:
        weights = nx.get_edge_attributes(graph_nx, 'sport')

    kinds = [graph_nx.nodes[k]['kind'] for k in graph_nx.nodes]

    colours = [YEAR_COLOUR if k == 'year' else (COUNTRY_COLOUR if k == 'country'else REGION_COLOUR) for k in kinds]

    x_edges = []
    y_edges = []
    weight_positions = []

    for edge in graph_nx.edges:
        x1, x2 = pos[edge[0]][0], pos[edge[1]][0]
        x_edges += [x1, x2, None]
        y1, y2 = pos[edge[0]][1], pos[edge[1]][1]
        y_edges += [y1, y2, None]
        if weighted:
            e = weights[(edge[0], edge[1])]
            if e is None:
                weight_positions.append(((x1 + x2) / 2, (y1 + y2) / 2, ''))
            else:
                weight_positions.append(((x1 + x2) / 2, (y1 + y2) / 2, e.total_scores()))

    trace3 = Scatter(x=x_edges,
                     y=y_edges,
                     mode='lines+text',
                     name='edges',
                     line=dict(color=LINE_COLOUR, width=1),
                     )

    trace4 = Scatter(x=x_values,
                     y=y_values,
                     mode='markers',
                     name='nodes',
                     marker=dict(symbol='circle-dot',
                                 size=5,
                                 color=colours,
                                 line=dict(color=VERTEX_BORDER_COLOUR, width=0.5)
                                 ),
                     text=labels,
                     hovertemplate='%{text}',
                     hoverlabel={'namelength': 0}
                     )

    data = [trace3, trace4]

    if weighted:
        return [weight_positions, data]
    else:
        return data


def visualize_graph(graph: data.Graph,
                    layout: str = 'spring_layout',
                    max_vertices: int = 5000,
                    output_file: str = '') -> None:
    """Use plotly and networkx to visualize the given GRAPH.

    Optional arguments:
        - layout: which GRAPH layout algorithm to use
        - max_vertices: the maximum number of vertices that can appear in the GRAPH
        - output_file: a filename to save the plotly image to (rather than displaying
            in your web browser)
    """

    draw_graph(setup_graph(graph, layout, max_vertices), output_file)


def visualize_weighted_graph(graph: data.Graph,
                             layout: str = 'spring_layout',
                             max_vertices: int = 5000,
                             output_file: str = '') -> None:
    """Use plotly and networkx to visualize the given weighted GRAPH.

    Optional arguments:
        - layout: which GRAPH layout algorithm to use
        - max_vertices: the maximum number of vertices that can appear in the GRAPH
        - output_file: a filename to save the plotly image to (rather than displaying
            in your web browser)
    """

    weight_positions, data = setup_graph(graph, layout, max_vertices, True)
    draw_graph(data, output_file, weight_positions)


def draw_graph(data: list, output_file: str = '', weight_positions=None) -> None:
    """
    Draw GRAPH based on given data.

    Optional arguments:
        - output_file: a filename to save the plotly image to (rather than displaying
            in your web browser)
        - weight_positions: weights to draw on edges for a weighted GRAPH
    """

    fig = Figure(data=data)
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    if weight_positions:
        for w in weight_positions:
            fig.add_annotation(
                x=w[0], y=w[1],  # Text annotation position
                xref="x", yref="y",  # Coordinate reference system
                text=w[2],  # Text content
                showarrow=False  # Hide arrow
            )

    if output_file == '':
        fig.show()
    else:
        fig.write_image(output_file)
