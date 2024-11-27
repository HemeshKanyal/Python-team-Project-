import pygame
import random

pygame.init()

WIDTH, HEIGHT = 10, 20  
TILE_SIZE = 30          
SCREEN_WIDTH, SCREEN_HEIGHT = WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

shapes = [
    [(0, 1), (1, 1), (2, 1), (3, 1)],  
    [(0, 0), (1, 0), (1, 1), (2, 1)],  
    [(1, 0), (0, 1), (1, 1), (2, 1)],  
    [(0, 0), (1, 0), (0, 1), (1, 1)],  
]


score = 0


def draw_grid():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            color = (0, 0, 0) if grid[y][x] == 0 else (100, 100, 100)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)


def draw_score():
    font = pygame.font.SysFont("Arial", 24)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def display_game_over():
    screen.fill((0, 0, 0))  
    font_big = pygame.font.SysFont("Arial", 50, bold=True)
    font_small = pygame.font.SysFont("Arial", 30)

    game_over_text = font_big.render("GAME OVER", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(game_over_text, game_over_rect)

    final_score_text = font_small.render(f"Your Score: {score}", True, (255, 255, 255))
    final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(final_score_text, final_score_rect)

    restart_text = font_small.render("Press R to Restart or Q to Quit", True, (200, 200, 200))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5))
    screen.blit(restart_text, restart_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

def create_tetromino():
    shape = random.choice(shapes)
    return [[x + WIDTH // 2, y] for x, y in shape]

def is_valid_position(tetromino):
    for x, y in tetromino:
        if x < 0 or x >= WIDTH or y >= HEIGHT:
            return False
        if y >= 0 and grid[y][x] != 0:
            return False
    return True

def place_tetromino(tetromino):
    for x, y in tetromino:
        if y >= 0:
            grid[y][x] = 1


def clear_rows():
    global grid, score
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    cleared_rows = HEIGHT - len(new_grid)
    grid = [[0] * WIDTH for _ in range(cleared_rows)] + new_grid
    score += cleared_rows * 10 


def rotate_tetromino(tetromino):
    center = tetromino[0] 
    rotated = [[center[0] - y + center[1], center[1] + x - center[0]] for x, y in tetromino]
    return rotated

while True:
    grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    tetromino = create_tetromino()
    fall_time = 0
    score = 0
    running = True

    while running:
        screen.fill((0, 0, 0))
        draw_grid()
        draw_score()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
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
                elif event.key == pygame.K_UP:  
                    new_tetromino = rotate_tetromino(tetromino)
                    if is_valid_position(new_tetromino):
                        tetromino = new_tetromino

        fall_time += clock.get_time()
        if fall_time > 500: 
            fall_time = 0
            new_tetromino = [[x, y + 1] for x, y in tetromino]
            if is_valid_position(new_tetromino):
                tetromino = new_tetromino
            else:
                place_tetromino(tetromino)
                clear_rows()
                tetromino = create_tetromino()
                if not is_valid_position(tetromino):
                    running = False


        for x, y in tetromino:
            if y >= 0:
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, (0, 255, 0), rect)

        pygame.display.flip()
        clock.tick(FPS)

    if not display_game_over():
        break