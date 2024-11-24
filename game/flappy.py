import pygame as pg
import sys
import random

# Game Settings
WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.25
FLAP_POWER = -6
PIPE_WIDTH = 50
PIPE_GAP = 150

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


class Bird:
    def __init__(self):
        # Triangle points for the bird (relative to the bird's center)
        self.size = 20
        self.rect = pg.Rect(100, HEIGHT // 2, self.size, self.size)
        self.points = [
            (self.rect.x, self.rect.y + self.size),  # Bottom-left corner
            (self.rect.x + self.size, self.rect.y + self.size // 2),  # Tip
            (self.rect.x, self.rect.y)  # Top-left corner
        ]
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        # Update triangle points with the bird's current position
        self.points = [
            (self.rect.x, self.rect.y + self.size),  # Bottom-left corner
            (self.rect.x + self.size, self.rect.y + self.size // 2),  # Tip
            (self.rect.x, self.rect.y)  # Top-left corner
        ]

    def flap(self):
        self.velocity = FLAP_POWER

    def draw(self, screen):
        # Draw a filled triangle representing the bird
        pg.draw.polygon(screen, WHITE, self.points)


class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, HEIGHT - 200)
        self.top_rect = pg.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pg.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP)

    def update(self):
        self.x -= 3  # Move pipes to the left
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, screen):
        pg.draw.rect(screen, GREEN, self.top_rect)
        pg.draw.rect(screen, GREEN, self.bottom_rect)

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

    def spawn_pipe(self):
        self.pipes.append(Pipe(WIDTH))

    def check_collision(self):
        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe.top_rect) or self.bird.rect.colliderect(pipe.bottom_rect):
                self.running = False  # End the game on collision

        if self.bird.rect.top <= 0 or self.bird.rect.bottom >= HEIGHT:
            self.running = False  # End the game if the bird hits the screen edges

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

    def run(self):
        while self.running:
            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    self.bird.flap()

            # Update game objects
            self.bird.update()
            for pipe in self.pipes:
                pipe.update()

            # Remove pipes that have left the screen
            self.pipes = [pipe for pipe in self.pipes if not pipe.off_screen()]

            # Spawn a new pipe if necessary
            if len(self.pipes) == 0 or self.pipes[-1].x < WIDTH - 200:
                self.spawn_pipe()

            # Check for collisions
            self.check_collision()

            # Update score
            for pipe in self.pipes:
                if pipe.x + PIPE_WIDTH < self.bird.rect.x and not getattr(pipe, 'scored', False):
                    self.score += 1
                    pipe.scored = True  # Mark pipe as scored

            # Draw everything
            self.screen.fill(BLUE)
            self.bird.draw(self.screen)
            for pipe in self.pipes:
                pipe.draw(self.screen)
            self.draw_score()

            # Update display and tick clock
            pg.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    FlappyBirdGame().run()