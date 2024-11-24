import pygame
import random

# Initialize the game
pygame.init()

# Screen settings
WIDTH, HEIGHT = 10, 20  # Grid size
TILE_SIZE = 30          # Size of each tile
SCREEN_WIDTH, SCREEN_HEIGHT = WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE
FPS = 60

# Set up display and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

# Create grid
grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

# Define Tetromino shapes
shapes = [
    [(0, 1), (1, 1), (2, 1), (3, 1)],  # Line
    [(0, 0), (1, 0), (1, 1), (2, 1)],  # Z-shape
    [(1, 0), (2, 0), (0, 1), (1, 1)],  # T-shape
    [(0, 0), (1, 0), (0, 1), (1, 1)],  # Square
]

# Function to draw the grid
def draw_grid():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            color = (0, 0, 0) if grid[y][x] == 0 else (100, 100, 100)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

# Spawn a new tetromino
def create_tetromino():
    shape = random.choice(shapes)
    return [[x + WIDTH // 2, y] for x, y in shape]

# Check if the position is valid
def is_valid_position(tetromino):
    for x, y in tetromino:
        if x < 0 or x >= WIDTH or y >= HEIGHT:
            return False
        if y >= 0 and grid[y][x] != 0:
            return False
    return True

# Place the tetromino on the grid
def place_tetromino(tetromino):
    for x, y in tetromino:
        if y >= 0:
            grid[y][x] = 1

# Clear completed rows
def clear_rows():
    global grid
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    cleared_rows = HEIGHT - len(new_grid)
    grid = [[0] * WIDTH for _ in range(cleared_rows)] + new_grid

# Game loop
tetromino = create_tetromino()
fall_time = 0

running = True
while running:
    screen.fill((0, 0, 0))
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                new_tetromino = [[x - 1, y] for x, y in tetromino]
                if is_valid_position(new_tetromino):
                    tetromino = new_tetromino
            elif event.key == pygame.K_RIGHT:
                new_tetromino = [[x + 1, y] for x, y in tetromino]
                if is_valid_position(new_tetromino):
                    tetromino = new_tetromino
            elif event.key == pygame.K_DOWN:
                new_tetromino = [[x, y + 1] for x, y in tetromino]
                if is_valid_position(new_tetromino):
                    tetromino = new_tetromino

    # Handle falling
    fall_time += clock.get_time()
    if fall_time > 500:  # Fall every 500ms
        fall_time = 0
        new_tetromino = [[x, y + 1] for x, y in tetromino]
        if is_valid_position(new_tetromino):
            tetromino = new_tetromino
        else:
            place_tetromino(tetromino)
            clear_rows()
            tetromino = create_tetromino()
            if not is_valid_position(tetromino):
                print("Game Over!")
                running = False

    # Draw current tetromino
    for x, y in tetromino:
        if y >= 0:
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (0, 255, 0), rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()