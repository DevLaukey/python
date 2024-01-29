import random
import time
from collections import deque

def generate_maze(size=10, density=0.2):
    maze = [['.' for _ in range(size)] for _ in range(size)]

    # Set random starting point (S) and goal point (G)
    start_row, start_col = random.randint(0, size - 1), random.randint(0, size - 1)
    goal_row, goal_col = random.randint(0, size - 1), random.randint(0, size - 1)

    maze[start_row][start_col] = 'S'
    maze[goal_row][goal_col] = 'G'

    # Add obstacles (X) based on density
    num_obstacles = int(density * size * size)
    for _ in range(num_obstacles):
        obstacle_row, obstacle_col = random.randint(0, size - 1), random.randint(0, size - 1)
        while maze[obstacle_row][obstacle_col] != '.':
            obstacle_row, obstacle_col = random.randint(0, size - 1), random.randint(0, size - 1)
        maze[obstacle_row][obstacle_col] = 'X'

    return maze

def depth_first_search(maze, start, goal):
    visited = set()
    path = []

    def dfs_helper(row, col):
        nonlocal path

        if (row, col) == goal:
            path.append((row, col))
            return True

        if 0 <= row < len(maze) and 0 <= col < len(maze[0]) and maze[row][col] == '.' and (row, col) not in visited:
            visited.add((row, col))
            path.append((row, col))

            # Visualize the explored paths
            maze[row][col] = '*'
            for r in maze:
                print(' '.join(r))
            print()
            time.sleep(0.1)  # Add a delay for better visualization

            # Explore neighbors in a depth-first manner
            if (dfs_helper(row + 1, col) or dfs_helper(row - 1, col) or
                dfs_helper(row, col + 1) or dfs_helper(row, col - 1)):
                return True

            # If the goal is not reached, backtrack and remove the current position from the path
            path.pop()

        return False

    # Start DFS from the given starting point
    dfs_helper(start[0], start[1])

    # Print the final path
    if path:
        print("Final DFS Path:")
        for position in path:
            maze[position[0]][position[1]] = 'P'  # Marking the path with 'P'

        # Visualize the final DFS solution
        for r in maze:
            print(' '.join(r))

def breadth_first_search(maze, start, goal):
    visited = set()
    queue = deque([(start[0], start[1])])
    parent = {}

    def is_valid(row, col):
        return 0 <= row < len(maze) and 0 <= col < len(maze[0]) and maze[row][col] == '.' and (row, col) not in visited

    while queue:
        current_row, current_col = queue.popleft()
        visited.add((current_row, current_col))

        # Visualize the explored paths
        maze[current_row][current_col] = '*'
        for r in maze:
            print(' '.join(r))
        print()

        if (current_row, current_col) == goal:
            break

        # Explore neighbors in a breadth-first manner
        neighbors = [(current_row + 1, current_col), (current_row - 1, current_col),
                      (current_row, current_col + 1), (current_row, current_col - 1)]

        for neighbor_row, neighbor_col in neighbors:
            if is_valid(neighbor_row, neighbor_col):
                queue.append((neighbor_row, neighbor_col))
                visited.add((neighbor_row, neighbor_col))
                parent[(neighbor_row, neighbor_col)] = (current_row, current_col)

    # Reconstruct the path from goal to start
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = parent[current]

    # Print the final BFS path
    if path:
        print("Final BFS Path:")
        path.reverse()
        for position in path:
            maze[position[0]][position[1]] = 'P'  # Marking the path with 'P'

        # Visualize the final BFS solution
        for r in maze:
            print(' '.join(r))

def heuristic(node, goal):
    # Manhattan distance heuristic
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def astar_search(maze, start, goal):
    visited = set()
    open_set = [(start[0], start[1])]
    parent = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    def is_valid(row, col):
        return 0 <= row < len(maze) and 0 <= col < len(maze[0]) and maze[row][col] == '.' and (row, col) not in visited

    while open_set:
        current = min(open_set, key=lambda node: f_score[node])
        open_set.remove(current)

        # Visualize the explored paths
        maze[current[0]][current[1]] = '*'
        for r in maze:
            print(' '.join(r))
        print()

        visited.add(current)

        if current == goal:
            break

        neighbors = [(current[0] + 1, current[1]), (current[0] - 1, current[1]),
                      (current[0], current[1] + 1), (current[0], current[1] - 1)]

        for neighbor in neighbors:
            if is_valid(neighbor[0], neighbor[1]):
                tentative_g_score = g_score[current] + 1

                if neighbor not in visited or tentative_g_score < g_score.get(neighbor, 0):
                    parent[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)

                    if neighbor not in open_set:
                        open_set.append(neighbor)

    # Reconstruct the path from goal to start
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = parent[current]

    # Print the final A* path
    if path:
        print("Final A* Path:")
        path.reverse()
        for position in path:
            maze[position[0]][position[1]] = 'P'  # Marking the path with 'P'

        # Visualize the final A* solution
        for r in maze:
            print(' '.join(r))

# Example usage with the generated maze
maze = generate_maze()
start_point = [(i, row.index('S')) for i, row in enumerate(maze) if 'S' in row][0]
goal_point = [(i, row.index('G')) for i, row in enumerate(maze) if 'G' in row][0]

print("Initial Maze:")
for row in maze:
    print(' '.join(row))
print()

# Run DFS
print("DFS Solution:")
depth_first_search(maze, start_point, goal_point)

print("\n----------------------------------------\n")

# Reset maze for BFS
maze = generate_maze()

print("Initial Maze:")
for row in maze:
    print(' '.join(row))
print()

# Run BFS
print("BFS Solution:")
breadth_first_search(maze, start_point, goal_point)

print("\n----------------------------------------\n")

# Reset maze for A*
maze = generate_maze()

print("Initial Maze:")
for row in maze:
    print(' '.join(row))
print()

# Run A*
print("A* Solution:")
astar_search(maze, start_point, goal_point)