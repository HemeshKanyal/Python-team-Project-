import pygame
from random import randrange as rnd

WIDTH, HEIGHT = 1200, 800
fps = 60

paddle_w = 300
paddle_h = 35
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)

ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1

block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

img = pygame.image.load('1.jpg').convert()

def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy

def show_start_screen():
    while True:
        sc.fill(pygame.Color('black'))
        font = pygame.font.SysFont('Arial', 80)
        text = font.render("WELCOME TO THE GAME!", True, pygame.Color('white'))
        sc.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 200))

        button_font = pygame.font.SysFont('Arial', 50)
        play_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 80)
        pygame.draw.rect(sc, pygame.Color('blue'), play_button)
        play_text = button_font.render("PLAY", True, pygame.Color('white'))
        sc.blit(play_text, (play_button.x + play_button.width // 2 - play_text.get_width() // 2, play_button.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return  # Start the game when "Play" is clicked

        pygame.display.flip()
        clock.tick(30)

def show_end_screen(message):
    while True:
        sc.fill(pygame.Color('black'))
        font = pygame.font.SysFont('Arial', 60)
        text = font.render(message, True, pygame.Color('white'))
        sc.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))

        button_font = pygame.font.SysFont('Arial', 40)
        replay_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 60)
        quit_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 100, 300, 60)

        pygame.draw.rect(sc, pygame.Color('green'), replay_button)
        pygame.draw.rect(sc, pygame.Color('red'), quit_button)

        replay_text = button_font.render("REPLAY", True, pygame.Color('black'))
        quit_text = button_font.render("QUIT", True, pygame.Color('black'))

        sc.blit(replay_text, (replay_button.x + replay_button.width // 2 - replay_text.get_width() // 2, replay_button.y + 10))
        sc.blit(quit_text, (quit_button.x + quit_button.width // 2 - quit_text.get_width() // 2, quit_button.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.collidepoint(event.pos):
                    return True
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        pygame.display.flip()
        clock.tick(30)

show_start_screen()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    sc.blit(img, (0, 0))

    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
    pygame.draw.rect(sc, pygame.Color('darkorange'), paddle)
    pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)

    ball.x += ball_speed * dx
    ball.y += ball_speed * dy

    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx
    if ball.centery < ball_radius:
        dy = -dy
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)

    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)

        hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
        pygame.draw.rect(sc, hit_color, hit_rect)
        fps += 2

    if ball.bottom > HEIGHT:
        if show_end_screen("GAME OVER!"):
            paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)
            ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
            dx, dy = 1, -1
            block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
            color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]
            fps = 60
        else:
            exit()
    elif not len(block_list):
        if show_end_screen("YOU WIN!!"):
            paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)
            ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
            dx, dy = 1, -1
            block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
            color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]
            fps = 60
        else:
            exit()

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed

    pygame.display.flip()
    clock.tick(fps)
