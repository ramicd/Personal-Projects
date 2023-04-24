from grid import Point


def dfs(source, destination, polygons):
    stack = [source]
    visited = {source}
    parent = {source: None}
    path_cost = {source: 0}
    num_expanded = 0

    while stack:
        current = stack.pop()
        num_expanded += 1
        if current == destination:
            break
        for neighbor in get_neighbors(current, polygons):

            if neighbor not in visited:
                stack.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    if destination not in parent:
        return None

    path = []
    current = destination
    while current:
        path.append(Point(*current))
        current = parent[current]

    path.reverse()
    return path, num_expanded


def isValidPoint(x,y,polygons):
    for polygon in polygons:
        for point in polygon:
            if(point==(x,y)):
                return False
    else:
        return True
    pass

def get_neighbors(cell,polygons):
    neighbors = []
    rows, cols = 50,50
    x, y = cell

    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        result=isValidPoint(nx,ny,polygons)
        if 0 <= nx < rows and 0 <= ny < cols and result:
            neighbors.append((nx, ny))

    return neighbors


if __name__=="__main__":
    source = (8,10)
    destination = (43,45)

    path = dfs(source, destination)

    if path is None:
        print("No path found.")
    else:
        print("Path found:", path)