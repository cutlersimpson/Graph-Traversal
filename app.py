"""
Script to traverse a directed acyclic graph and
print the vertices in order of time delay as defined by graph edges
"""

import json
import time
from collections import deque
from exceptions import NoStartVertexException, MultipleStartVerticesException


def get_graph():
    graph_json = """
    {
        "A": {"start": true, "edges": {"B": 5, "C": 7}},
        "B": {"start": false, "edges": {"D": 1}},
        "C": {"edges": {}},
        "D": {"edges": {}}
    }
    """

    return json.loads(graph_json)


def traverse_graph(graph):
    start_vertex = find_start_vertex(graph)

    if start_vertex is None:
        raise NoStartVertexException("No start vertex found.")

    vertices = bfs(start_vertex, graph)

    return sorted(vertices, key=lambda x: x[1])  # Sort the vertices by total delay


def find_start_vertex(graph):
    start_vertex = None

    for vertex, props in graph.items():
        if props.get("start"):
            if start_vertex is not None:
                raise MultipleStartVerticesException("Multiple start vertices found.")
            start_vertex = vertex
    return start_vertex


def bfs(start_vertex, graph):
    visited = set()
    visited.add(start_vertex)

    queue = deque([(start_vertex, 0)])  # (vertex, total_delay)
    vertices = [(start_vertex, 0)]

    while queue:
        vertex, total_delay = queue.popleft()

        if vertex not in graph:
            continue

        edges = graph[vertex]["edges"]

        for next_vertex, delay in edges.items():
            if next_vertex not in visited:
                visited.add(next_vertex)
                queue.append((next_vertex, total_delay + delay))
                vertices.append((next_vertex, total_delay + delay))
    return vertices


def print_vertices(vertices):
    if vertices is None:
        return

    previous_time = 0
    for vertex, delay in vertices:
        sleep_delay = delay - previous_time
        time.sleep(sleep_delay)
        print(vertex)
        previous_time = delay


if __name__ == "__main__":
    graph_data = get_graph()
    sorted_vertices = traverse_graph(graph_data)
    print_vertices(sorted_vertices)
