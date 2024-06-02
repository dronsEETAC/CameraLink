import heapq

def heuristic(node, goal):
    # Aquí puedes definir tu heurística específica.
    # Por ejemplo, si los nodos son coordenadas (x, y) puedes usar la distancia euclidiana.
    return ((node[0] - goal[0]) ** 2 + (node[1] - goal[1]) ** 2) ** 0.5

def astar(graph, start, goal):
    frontier = [(0, start)]
    came_from = {}
    cost_so_far = {start: 0}

    while frontier:
        current_cost, current_node = heapq.heappop(frontier)

        if current_node == goal:
            break

        for next_node in graph[current_node]:
            new_cost = cost_so_far[current_node] + graph[current_node][next_node]
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(next_node, goal)
                heapq.heappush(frontier, (priority, next_node))
                came_from[next_node] = current_node

    path = []
    current_node = goal
    while current_node != start:
        path.append(current_node)
        current_node = came_from[current_node]
    path.append(start)
    path.reverse()

    return path

# Ejemplo de uso
graph = {
    'A': {'B': 5, 'C': 3},
    'B': {'D': 4},
    'C': {'D': 2},
    'D': {}
}
start = 'A'
goal = 'D'
print(astar(graph, start, goal))
