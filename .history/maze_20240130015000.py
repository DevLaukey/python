import random
import time

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

def dfs_helper(row, col):
    nonlocal path

    if (row, col) == goal:
        path.append((row, col))
        return True

    if 0 <= row < len(maze) and 0 <= col < len(maze[0]) and maze[row][col] == '.' and (row, col) not in visited:
        visited.add((row, col))
        path.append((row, col))

        # Print the current coordinates and the maze
        print(f"Visiting: ({row}, {col})")
        for r in maze:
            print(' '.join(r))
        print()

        # Explore neighbors in a depth-first manner
        if (dfs_helper(row + 1, col) or dfs_helper(row - 1, col) or
            dfs_helper(row, col + 1) or dfs_helper(row, col - 1)):
            return True

        # If the goal is not reached, backtrack and remove the current position from the path
        path.pop()
    else:
        # Print why the current coordinates are not visited
        print(f"Skipping: ({row}, {col}) - Out of bounds or not a free path or already visited")

    return False
# Example usage
maze = generate_maze()
start_point = [(i, row.index('S')) for i, row in enumerate(maze) if 'S' in row][0]
goal_point = [(i, row.index('G')) for i, row in enumerate(maze) if 'G' in row][0]

print("Initial Maze:")
for row in maze:
    print(' '.join(row))
print()

print("DFS Solution:")
depth_first_search(maze, start_point, goal_point)
