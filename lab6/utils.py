import networkx as nx


def print_graph_to_stdo(graph: nx.Graph):
    """
     Helper function for visualizing the underlying graph structure of the game
    :param graph: grid_2d_graph from networkx library to visualize
    :return:
    """
    node: str = 'O'
    horizontal_edge: str = '|'
    vertical_edge: str = '-'

    max_x: int = max([pos[0] for pos in graph.nodes()])
    max_y: int = max([pos[1] for pos in graph.nodes()])

    # Initialize a 2D array with spaces
    grid: list[list[str]] = [[' ' for _ in range(2 * max_y + 1)] for _ in range(2 * max_x + 1)]

    # Add nodes to the grid
    for x, y in graph.nodes():
        grid[2 * x][2 * y] = node

    # Add edges to the grid
    for edge in graph.edges():
        x1, y1 = edge[0]
        x2, y2 = edge[1]

        if x1 == x2:
            # Vertical edge
            grid[2 * x1][2 * y1 + 1] = vertical_edge
        elif y1 == y2:
            # Horizontal edge
            grid[2 * x1 + 1][2 * y1] = horizontal_edge

    # Print the grid
    for row in grid:
        print(''.join(row))
