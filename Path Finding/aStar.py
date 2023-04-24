from grid import Point
import heapq
import math

def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def aStar(source, destination, polygons):
    def heuristic(current):
        return euclidean_distance(current, destination)

    heap = [(0, source)]
    visited = {source}
    parent = {source: None}
    cost = {source: 0}
    expanded = 0

    while heap:
        _, current = heapq.heappop(heap)
        if current == destination:
            break
        for neighbor in get_neighbors(current, polygons):
            new_cost = cost[current] + 1
            if neighbor not in visited or new_cost < cost[neighbor]:
                visited.add(neighbor)
                cost[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(heap, (new_cost + heuristic(neighbor), neighbor))
                expanded += 1

    if destination not in parent:
        return None, None

    path = []
    current = destination
    while current:
        path.append(Point(*current))
        current = parent[current]

    path.reverse()
    cost = cost[destination]
    return path,expanded

def isValidPoint(x, y, polygons):
    for polygon in polygons:
        for point in polygon:
            if point == (x, y):
                return False
    else:
        return True


def get_neighbors(cell, polygons):
    neighbors = []
    rows, cols = 50, 50
    x, y = cell

    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        result = isValidPoint(nx, ny, polygons)
        if 0 <= nx < rows and 0 <= ny < cols and result:
            neighbors.append((nx, ny))

    return neighbors


if __name__ == "__main__":
    source = (8, 10)
    destination = (43, 45)

    path = aStar(source, destination, [])

    if path is None:
        print("No path found.")
    else:
        print("Path found:", path)
