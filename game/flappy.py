import pygame as pg
import sys
import random


WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.25
FLAP_POWER = -6
PIPE_WIDTH = 50
PIPE_GAP = 150

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

def load_image(path, scale=None):
    try:
        img = pg.image.load(path).convert_alpha()
        if scale:
            img = pg.transform.scale(img, scale)
        return img
    except pg.error as e:
        print(f"Unable to load image at {path}: {e}")
        sys.exit()


class Bird:
    def __init__(self):
        self.image = load_image("bird.png", (40, 40))
        self.rect = self.image.get_rect(center=(100, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

    def flap(self):
        self.velocity = FLAP_POWER

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Pipe:
    def __init__(self, x):
        self.pipe_top = load_image("pipe_top.jpg", (PIPE_WIDTH, HEIGHT // 2))
        self.pipe_bottom = load_image("pipe_bottom.jpg", (PIPE_WIDTH, HEIGHT // 2))
        self.x = x
        self.height = random.randint(100, HEIGHT - 200)
        self.top_rect = self.pipe_top.get_rect(midbottom=(self.x, self.height))
        self.bottom_rect = self.pipe_bottom.get_rect(midtop=(self.x, self.height + PIPE_GAP))

    def update(self):
        self.x -= 3
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, screen):
        screen.blit(self.pipe_top, self.top_rect)
        screen.blit(self.pipe_bottom, self.bottom_rect)

    def off_screen(self):
        return self.x + PIPE_WIDTH < 0


class FlappyBirdGame:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Flappy Bird")
        self.clock = pg.time.Clock()
        self.running = True
        self.bird = Bird()
        self.pipes = []
        self.spawn_pipe()
        self.score = 0
        self.font = pg.font.SysFont("Arial", 30)
        self.background = load_image("background.jpg", (WIDTH, HEIGHT))

    def spawn_pipe(self):
        self.pipes.append(Pipe(WIDTH))

    def check_collision(self):
        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe.top_rect) or self.bird.rect.colliderect(pipe.bottom_rect):
                self.running = False

        if self.bird.rect.top <= 0 or self.bird.rect.bottom >= HEIGHT:
            self.running = False

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

    def display_game_over(self):
        self.screen.fill(BLACK)
        font_big = pg.font.SysFont("Arial", 50, bold=True)
        font_small = pg.font.SysFont("Arial", 30)

        game_over_text = font_big.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        self.screen.blit(game_over_text, game_over_rect)

        final_score_text = font_small.render(f"Your Score: {self.score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(final_score_text, final_score_rect)

        restart_text = font_small.render("Press R to Restart or Q to Quit", True, GRAY)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))
        self.screen.blit(restart_text, restart_rect)

        pg.display.flip()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        return True
                    if event.key == pg.K_q:
                        pg.quit()
                        sys.exit()

    def show_start_screen(self):
        font_big = pg.font.SysFont("Arial", 50, bold=True)
        font_small = pg.font.SysFont("Arial", 30)

        self.screen.fill(WHITE)
        title_text = font_big.render("Flappy Bird", True, BLACK)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        self.screen.blit(title_text, title_rect)

        play_button_text = font_small.render("Play", True, WHITE)
        play_button_rect = pg.Rect((WIDTH // 2 - 50, HEIGHT // 2 - 25), (100, 50))
        pg.draw.rect(self.screen, RED, play_button_rect)
        self.screen.blit(play_button_text, play_button_text.get_rect(center=play_button_rect.center))

        pg.display.flip()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if play_button_rect.collidepoint(event.pos):
                        return

    def run(self):
        self.show_start_screen()
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    self.bird.flap()

            self.bird.update()
            for pipe in self.pipes:
                pipe.update()

            self.pipes = [pipe for pipe in self.pipes if not pipe.off_screen()]

            if len(self.pipes) == 0 or self.pipes[-1].x < WIDTH - 200:
                self.spawn_pipe()

            self.check_collision()

            for pipe in self.pipes:
                if pipe.x + PIPE_WIDTH < self.bird.rect.x and not getattr(pipe, 'scored', False):
                    self.score += 1
                    pipe.scored = True

            self.screen.blit(self.background, (0, 0))
            self.bird.draw(self.screen)
            for pipe in self.pipes:
                pipe.draw(self.screen)
            self.draw_score()

            pg.display.flip()
            self.clock.tick(FPS)

        if not self.running:
            if self.display_game_over():
                self.__init__()
                self.run()

if __name__ == "__main__":
    FlappyBirdGame().run()
