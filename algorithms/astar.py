import heapq

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def a_star_search(grid_model, start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            break

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            next_node = (current[0] + dx, current[1] + dy)
            
            if grid_model.get_tile(*next_node) == 1:
                new_cost = cost_so_far[current] + 1
                
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + manhattan_distance(next_node, goal)
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current

    if goal not in came_from:
        return []

    path = []
    curr = goal
    while curr is not None:
        path.append(curr)
        curr = came_from[curr]
    
    return path[::-1]