from collections import deque

def find_path_bfs(grid_matrix, start, end):
    rows = len(grid_matrix)
    cols = len(grid_matrix[0]) if rows > 0 else 0
    queue = deque([[start]])
    visited = {start}

    while queue:
        path = queue.popleft()
        cx, cy = path[-1]

        if (cx, cy) == end:
            return path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy

            if 0 <= nx < cols and 0 <= ny < rows:
                if (nx, ny) not in visited:
                    if grid_matrix[ny][nx] in {1, 3, 4} or (nx, ny) == end or (nx, ny) == start:
                        visited.add((nx, ny))
                        queue.append(path + [(nx, ny)])
    return None