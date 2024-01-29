
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
