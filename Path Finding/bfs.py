from grid import Point
from collections import deque


def bfs(source, destination, polygons):
    queue = deque([source])
    visited = {source}
    parent = {source: None}
    cost = {source: 0}
    nodes_expanded = 0

    while queue:
        current = queue.popleft()
        nodes_expanded += 1
        if current == destination:
            break
        for neighbor in get_neighbors(current, polygons):
            new_cost = cost[current] + 1
            if neighbor not in visited or new_cost < cost[neighbor]:
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current
                cost[neighbor] = new_cost

    if destination not in parent:
        return None, nodes_expanded

    path = []
    current = destination
    while current:
        path.append(Point(*current))
        current = parent[current]

    path.reverse()
    return path, nodes_expanded


def is_valid_point(x, y, polygons):
    for polygon in polygons:
        for point in polygon:
            if point == (x, y):
                return False
    return True


def get_neighbors(cell, polygons):
    neighbors = []
    rows, cols = 50, 50
    x, y = cell

    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        result = is_valid_point(nx, ny, polygons)
        if 0 <= nx < rows and 0 <= ny < cols and result:
            neighbors.append((nx, ny))

    return neighbors


if __name__ == "__main__":
    source = (8, 10)
    destination = (43, 45)
    polygons = [[(35, 45), (41, 45), (41, 30), (35, 30)]]

    path, nodes_expanded = bfs(source, destination, polygons)

    if path is None:
        print("No path found.")
    else:
        print("Path found:", path)
        print("Path cost:", len(path) - 1)
        print("Nodes expanded:", nodes_expanded)
