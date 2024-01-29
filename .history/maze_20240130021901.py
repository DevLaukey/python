import pygame
import random
import time
import heapq

# Maze Generation
def generate_maze(size, density):
    maze = [[' ' if random.random() > density else '#' for _ in range(size)] for _ in range(size)]
    start = (0, 0)
    goal = (size - 1, size - 1)
    maze[start[0]][start[1]] = 'S'
    maze[goal[0]][goal[1]] = 'G'
    return maze, start, goal

# Visualization
def draw_maze(screen, maze):
    cell_size = 30
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            color = (255, 255, 255) if cell == ' ' else (0, 0, 0)
            pygame.draw.rect(screen, color, (j * cell_size, i * cell_size, cell_size, cell_size))
            if cell == 'S':
                pygame.draw.circle(screen, (0, 255, 0), (j * cell_size + cell_size // 2, i * cell_size + cell_size // 2), cell_size // 2)
            elif cell == 'G':
                pygame.draw.circle(screen, (255, 0, 0), (j * cell_size + cell_size // 2, i * cell_size + cell_size // 2), cell_size // 2)

# Depth-First Search
def dfs(maze, start, goal):
    stack = [start]
    visited = set()

    while stack:
        current = stack.pop()
        if current == goal:
            return True
        if current not in visited:
            visited.add(current)
            neighbors = [(current[0] + 1, current[1]), (current[0] - 1, current[1]), (current[0], current[1] + 1), (current[0], current[1] - 1)]
            neighbors = [(i, j) for i, j in neighbors if 0 <= i < len(maze) and 0 <= j < len(maze[0]) and maze[i][j] != '#']
            stack.extend(neighbors)

    return False

# Breadth-First Search
def bfs(maze, start, goal):
    queue = [start]
    visited = set()

    while queue:
        current = queue.pop(0)
        if current == goal:
            return True
        if current not in visited:
            visited.add(current)
            neighbors = [(current[0] + 1, current[1]), (current[0] - 1, current[1]), (current[0], current[1] + 1), (current[0], current[1] - 1)]
            neighbors = [(i, j) for i, j in neighbors if 0 <= i < len(maze) and 0 <= j < len(maze[0]) and maze[i][j] != '#']
            queue.extend(neighbors)

    return False

# A* Algorithm
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(maze, start, goal):
    heap = [(0, start)]
    visited = set()

    while heap:
        current_cost, current = heapq.heappop(heap)
        if current == goal:
            return True
        if current not in visited:
            visited.add(current)
            neighbors = [(current[0] + 1, current[1]), (current[0] - 1, current[1]), (current[0], current[1] + 1), (current[0], current[1] - 1)]
            neighbors = [(i, j) for i, j in neighbors if 0 <= i < len(maze) and 0 <= j < len(maze[0]) and maze[i][j] != '#']
            for neighbor in neighbors:
                cost = current_cost + heuristic(neighbor, goal)
                heapq.heappush(heap, (cost, neighbor))

    return False

# Visualization setup
def visualize(maze, start, goal, algorithm):
    pygame.init()
    size = len(maze) * 30
    screen = pygame.display.set_mode((size, size))
    pygame.display.set_caption(f'Maze Visualization - {algorithm}')
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((255, 255, 255))
        draw_maze(screen, maze)
        pygame.display.flip()
        clock.tick(60)

# Main function
def main():
    size = 10
    density = 0.3

    maze, start, goal = generate_maze(size, density)
    visualize(maze, start, goal, "Original Maze")

    if dfs(maze, start, goal):
        visualize(maze, start, goal, "DFS")
    else:
        print("DFS could not find a path.")

    if bfs(maze, start, goal):
        visualize(maze, start, goal, "BFS")
    else:
        print("BFS could not find a path.")

    if astar(maze, start, goal):
        visualize(maze, start, goal, "A*")
    else:
        print("A* could not find a path.")

if __name__ == "__main__":
    main()
