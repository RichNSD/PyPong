import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 20
PADDLE_SPEED = 6
BALL_SPEED_X, BALL_SPEED_Y = 7, 7
WHITE, BLACK = (255, 255, 255), (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Paddles and ball
paddle_left = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_right = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# Ball velocity with random initial direction
ball_velocity = [random.choice([BALL_SPEED_X, -BALL_SPEED_X]), random.choice([BALL_SPEED_Y, -BALL_SPEED_Y])]
score_left, score_right = 0, 0

font = pygame.font.Font(None, 74)
clock = pygame.time.Clock()

def reset_ball(direction):
    ball.center = (WIDTH//2, HEIGHT//2)
    return [direction * BALL_SPEED_X, random.choice([BALL_SPEED_Y, -BALL_SPEED_Y])]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle key presses for paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle_left.top > 0:
        paddle_left.y -= PADDLE_SPEED
    if keys[pygame.K_s] and paddle_left.bottom < HEIGHT:
        paddle_left.y += PADDLE_SPEED
    if keys[pygame.K_UP] and paddle_right.top > 0:
        paddle_right.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and paddle_right.bottom < HEIGHT:
        paddle_right.y += PADDLE_SPEED

    # Update ball position
    ball.x += ball_velocity[0]
    ball.y += ball_velocity[1]

    # Collision with top and bottom walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_velocity[1] = -ball_velocity[1]

    # Collision with paddles
    for paddle in [paddle_left, paddle_right]:
        if ball.colliderect(paddle):
            if (paddle == paddle_left and ball_velocity[0] < 0) or (paddle == paddle_right and ball_velocity[0] > 0):
                # Calculate hit position effect
                hit_pos = (ball.centery - paddle.centery) / (PADDLE_HEIGHT / 2)
                ball_velocity[1] = hit_pos * BALL_SPEED_Y
                ball_velocity[0] = -ball_velocity[0]

    # Scoring
    if ball.left <= 0:
        score_right += 1
        ball_velocity = reset_ball(1)  # Move towards right
    if ball.right >= WIDTH:
        score_left += 1
        ball_velocity = reset_ball(-1)  # Move towards left

    # Check for winner
    if score_left >= 10 or score_right >= 10:
        winner_text = "Left Player Wins!" if score_left >=10 else "Right Player Wins!"
        text = font.render(winner_text, True, WHITE)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle_left)
    pygame.draw.rect(screen, WHITE, paddle_right)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    # Draw scores
    screen.blit(font.render(str(score_left), True, WHITE), (WIDTH//4, 20))
    screen.blit(font.render(str(score_right), True, WHITE), (3*WIDTH//4 - 50, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()