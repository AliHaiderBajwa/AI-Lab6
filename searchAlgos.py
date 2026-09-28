"""Search algorithms + hospital graph (Task 3) reused by the Streamlit GUI."""
import math
import heapq

# Graph, Use Case: Emergency Supply Robot
locations = {
    "Pharmacy": (0, 0),
    "Main_Corridor": (2, 1),
    "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2),
    "Laboratory": (5, 5),
    "Emergency_Ward": (8, 6)
}

hospital_graph = {
    "Pharmacy": {"Main_Corridor": 2.2, "Patient_Wing": 4.1},
    "Main_Corridor": {"Nursing_Station": 2.2},
    "Patient_Wing": {"Laboratory": 5.0},
    "Nursing_Station": {"Laboratory": 3.2, "Emergency_Ward": 6.0},
    "Laboratory": {"Emergency_Ward": 3.2},
    "Emergency_Ward": {}
}


# Heuristic: Euclidean distance
def heuristic(current, goal):
    (x1, y1), (x2, y2) = locations[current], locations[goal]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# Path reconstruction
def reconstruct_path(came_from, current):
    path = [current]
    while came_from[current] is not None:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def _path_cost(path):
    return sum(hospital_graph[a][b] for a, b in zip(path, path[1:]))


# GBFS: f(n) = h(n)  -> returns (path, cost, expansion_order); path is None if unreachable
def gbfs(start, goal):
    counter = 0
    frontier = [(heuristic(start, goal), counter, start)]
    came_from = {start: None}
    visited = set()
    expansion_order = []

    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)
        expansion_order.append(current)

        if current == goal:
            path = reconstruct_path(came_from, current)
            return path, _path_cost(path), expansion_order

        for neighbor in hospital_graph[current]:
            if neighbor not in visited and neighbor not in came_from:
                came_from[neighbor] = current
                counter += 1
                heapq.heappush(frontier, (heuristic(neighbor, goal), counter, neighbor))

    return None, float("inf"), expansion_order


# A*: f(n) = g(n) + h(n)  -> returns (path, cost, expansion_order); path is None if unreachable
def a_star(start, goal):
    counter = 0
    g_cost = {start: 0.0}
    came_from = {start: None}
    frontier = [(heuristic(start, goal), counter, 0.0, start)]
    expansion_order = []

    while frontier:
        _, _, g, current = heapq.heappop(frontier)
        if g > g_cost[current]:
            continue
        expansion_order.append(current)

        if current == goal:
            return reconstruct_path(came_from, current), g, expansion_order

        for neighbor, cost in hospital_graph[current].items():
            new_g = g_cost[current] + cost
            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                came_from[neighbor] = current
                counter += 1
                heapq.heappush(frontier, (new_g + heuristic(neighbor, goal), counter, new_g, neighbor))

    return None, float("inf"), expansion_order
