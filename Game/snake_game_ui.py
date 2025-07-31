import pygame
import random
import sys

# Initialize
pygame.init()
pygame.mixer.init()  # Initialize the sound system

# Load Sound Effects
eat_sound = pygame.mixer.Sound("hiss-86052.mp3")
gameover_sound = pygame.mixer.Sound("game-fail-90322.mp3")

# Screen Settings
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Fonts
FONT = pygame.font.SysFont("consolas", 28, bold=True)
BIG_FONT = pygame.font.SysFont("consolas", 48, bold=True)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game ")

clock = pygame.time.Clock()
FPS = 8

# Helper function to draw text
def draw_text(surface, text, font, color, x, y):
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, (x, y))

# Draw grid (optional for style)
def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, DARK_GREEN, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, DARK_GREEN, (0, y), (WIDTH, y))

# Snake Game
def game_loop():
    # Snake setup
    snake = [[100, 100]]
    direction = [CELL_SIZE, 0]
    score = 0

    # Food setup
    food = [
        random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
        random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    ]

    running = True
    while running:
        screen.fill(BLACK)
        draw_grid()

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Controls
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction[1] == 0:
                    direction = [0, -CELL_SIZE]
                elif event.key == pygame.K_DOWN and direction[1] == 0:
                    direction = [0, CELL_SIZE]
                elif event.key == pygame.K_LEFT and direction[0] == 0:
                    direction = [-CELL_SIZE, 0]
                elif event.key == pygame.K_RIGHT and direction[0] == 0:
                    direction = [CELL_SIZE, 0]

        # Move snake
        new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
        snake.insert(0, new_head)

        # Eat food
        if snake[0] == food:
            eat_sound.play()  # 🔊 Play eat sound
            score += 1
            food = [
                random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            ]
        else:
            snake.pop()

        # Collision: Walls
        if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
            snake[0][1] < 0 or snake[0][1] >= HEIGHT):
            return show_game_over(score)

        # Collision: Self
        if snake[0] in snake[1:]:
            return show_game_over(score)

        # Draw snake
        for block in snake:
            pygame.draw.rect(screen, GREEN, (block[0], block[1], CELL_SIZE, CELL_SIZE))

        # Draw food
        pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

        # Draw Score
        draw_text(screen, f"Score: {score}", FONT, WHITE, 10, 10)

        pygame.display.update()
        clock.tick(FPS)

# Game Over Screen
def show_game_over(score):
    gameover_sound.play()  # 🔊 Play game over sound
    screen.fill(BLACK)
    draw_text(screen, "Game Over", BIG_FONT, RED, WIDTH//2 - 140, HEIGHT//2 - 80)
    draw_text(screen, f"Your Score: {score}", FONT, WHITE, WIDTH//2 - 100, HEIGHT//2 - 20)
    draw_text(screen, "Press R to Restart or Q to Quit", FONT, GREEN, WIDTH//2 - 190, HEIGHT//2 + 40)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Start Game
game_loop()