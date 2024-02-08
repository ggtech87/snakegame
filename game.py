import pygame
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 20
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define Snake class
class Snake:
    def __init__(self, x, y, color):
        self.body = [(x, y)]
        self.direction = 'RIGHT'
        self.color = color

    def move(self):
        head = self.body[0]
        x, y = head

        if self.direction == 'UP':
            y -= CELL_SIZE
        elif self.direction == 'DOWN':
            y += CELL_SIZE
        elif self.direction == 'LEFT':
            x -= CELL_SIZE
        elif self.direction == 'RIGHT':
            x += CELL_SIZE

        self.body.insert(0, (x, y))

    def change_direction(self, direction):
        if direction == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        elif direction == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        elif direction == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        elif direction == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, self.color, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

# Define CPU Snake class
class CPUSnake(Snake):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)

    def move_randomly(self):
        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        random_direction = random.choice(directions)
        self.change_direction(random_direction)
        self.move()

# Function to handle collisions
def check_collisions(snake, cpu_snakes):
    # Check collisions with walls
    head = snake.body[0]
    if head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT:
        return True

    # Check collisions with CPU snakes
    for cpu_snake in cpu_snakes:
        if head in cpu_snake.body:
            return True

    return False
# Main function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Game')

    clock = pygame.time.Clock()

    # Game variables
    running = True
    game_over = False

    while running:
        screen.fill(WHITE)

        player_snake = Snake(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, GREEN)
        cpu_snakes_info = [(random.randint(0, SCREEN_WIDTH // CELL_SIZE - 1) * CELL_SIZE,
                            random.randint(0, SCREEN_HEIGHT // CELL_SIZE - 1) * CELL_SIZE,
                            RED) for _ in range(3)]
        cpu_snakes = [CPUSnake(*info) for info in cpu_snakes_info]

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player_snake.change_direction('UP')
                    elif event.key == pygame.K_DOWN:
                        player_snake.change_direction('DOWN')
                    elif event.key == pygame.K_LEFT:
                        player_snake.change_direction('LEFT')
                    elif event.key == pygame.K_RIGHT:
                        player_snake.change_direction('RIGHT')

            # Move player snake
            player_snake.move()

            # Move CPU snakes
            for cpu_snake in cpu_snakes:
                cpu_snake.move_randomly()

            # Check collisions
            if check_collisions(player_snake, cpu_snakes):
                game_over = True

            # Draw player snake
            player_snake.draw(screen)

            # Draw CPU snakes
            for cpu_snake in cpu_snakes:
                cpu_snake.draw(screen)

            # Update display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(10)

        # Show "Game Over" message
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("Game Over. Press Enter to restart.", True, (0, 0, 0))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, text_rect)
        pygame.display.flip()

        # Wait for Enter key press to restart the game
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
                        game_over = False

    pygame.quit()

if __name__ == "__main__":
    main()
