import random

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

    def dfs_helper(row, col):
        if (row, col) == goal:
            return True

        if 0 <= row < len(maze) and 0 <= col < len(maze[0]) and maze[row][col] == '.' and (row, col) not in visited:
            visited.add((row, col))

            # Visualize the explored paths
            maze[row][col] = '*'
            for r in maze:
                print(' '.join(r))
            print()

            # Explore neighbors in a depth-first manner
            if (dfs_helper(row + 1, col) or dfs_helper(row - 1, col) or
                dfs_helper(row, col + 1) or dfs_helper(row, col - 1)):
                return True

        return False

    # Start DFS from the given starting point
    dfs_helper(start[0], start[1])

# Example usage
maze = generate_maze()
for row in maze:
    print(' '.join(row))
