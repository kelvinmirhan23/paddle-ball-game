import pygame  # Import the pygame library 
import random  # Import random module to randomly initialize ball position and direction

# Initialize pygame
pygame.init()

# Game Constants (Set up screen width, height, and object sizes)
WIDTH, HEIGHT = 800, 600  # Screen dimensions
BALL_RADIUS = 20  # Radius of the ball
BALL_SPEED_X = 5  # Initial horizontal speed of the ball
BALL_SPEED_Y = 5  # Initial vertical speed of the ball
PADDLE_WIDTH = 100  # Width of the paddle
PADDLE_HEIGHT = 15  # Height of the paddle
PADDLE_SPEED = 10  # Speed at which the paddle moves left and right

# Defining Colors using RGB values
WHITE = (255, 255, 255)  # Background color
BLACK = (0, 0, 0)  # Text color
RED = (255, 0, 0)  # Ball color
BLUE = (0, 0, 255)  # Paddle color
GREEN = (0, 255, 0)  # Start/Restart text color

# To set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the ame window with defined width and height
pygame.display.set_caption("Paddle Bouncing Ball Game")  # Set the window title

# Initialize Ball properties
ball_x = random.randint(BALL_RADIUS, WIDTH - BALL_RADIUS)  # Randomly position ball within screen width
ball_y = HEIGHT // 2  # Start the ball at the middle of the screen vertically
ball_dx = BALL_SPEED_X  # Set horizontal movement direction
ball_dy = BALL_SPEED_Y  # Set vertical movement direction

# Initialize Paddle properties
paddle_x = (WIDTH - PADDLE_WIDTH) // 2  # Start paddle in the middle of the screen horizontally
paddle_y = HEIGHT - 50  # Position paddle near the bottom of the screen

# Score variables
score = 0  # Initialize player's score
high_score = 0  # Track the highest score achieved

# Game state flags
game_active = False  # Track if the game is currently running
game_over = False  # Track if the game has ended

# Load font for rendering text
font = pygame.font.Font(None, 36)  # Use default font, size 36

# Function to draw the start screen
def draw_start_screen():
    screen.fill(WHITE)  # Clear screen with white background
    title_text = font.render("Paddle Bouncing Ball Game", True, BLACK)  # Render game title text
    start_text = font.render("Press SPACE to Start", True, GREEN)  # Render start instruction text
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))  # Center title text
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))  # Center start text
    pygame.display.flip()  # Update screen

# Function to draw the game over screen
def draw_game_over_screen():
    screen.fill(WHITE)  # Clear screen with white background
    game_over_text = font.render("GAME OVER", True, RED)  # Render "Game Over" text in red
    restart_text = font.render("Press SPACE to Restart", True, GREEN)  # Render restart instruction
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))  # Center "Game Over" text
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))  # Center restart text
    pygame.display.flip()  # Update screen

# Game loop (Main loop that keeps the game running)
running = True  # Flag to keep the game loop running
clock = pygame.time.Clock()  # Creating a clock object to control frame rate

while running:
    # First iteration we entire this if block of if-else 
    if not game_active:  # Check if the game is in the start or game over screen
        if game_over:
            draw_game_over_screen()  # Display game over screen if the game ended
        else:
            draw_start_screen()  # Otherwise display the start screen
        
        # Event loop to check for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If user clicks the close button, exit the game
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # If space is pressed, start/restart game
                game_active = True  # Start the game
                game_over = False  # Reset game over state
    # On the next loop iteration, assuming player presses SPACE, game_active is set to True and we enter this else block
    else:
        screen.fill(WHITE)  # Clear screen to avoid ghosting effects
        
        # Event Handling (Check if player wants to quit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Paddle Movement (Controlled by Left and Right arrow keys)
        keys = pygame.key.get_pressed()  # Get pressed keys
        if keys[pygame.K_LEFT] and paddle_x > 0:  # Move left if not at left boundary
            paddle_x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:  # Move right if not at right boundary
            paddle_x += PADDLE_SPEED
        
        # Ball Movement (Ball moves according to its velocity)
        ball_x += ball_dx  # Update ball's x-coordinate
        ball_y += ball_dy  # Update ball's y-coordinate
        
        # Collision with Left/Right Walls (Reverse X direction when hitting the sides)
        if ball_x - BALL_RADIUS <= 0 or ball_x + BALL_RADIUS >= WIDTH:
            ball_dx *= -1  # Reverse direction
        
        # Collision with Top Wall (Reverse Y direction when hitting the top)
        if ball_y - BALL_RADIUS <= 0:
            ball_dy *= -1  # Reverse direction
        
        # Collision with Paddle (If ball touches paddle, bounce it up)
        if (paddle_y <= ball_y + BALL_RADIUS <= paddle_y + PADDLE_HEIGHT) and (paddle_x <= ball_x <= paddle_x + PADDLE_WIDTH):
            ball_dy *= -1  # Reverse direction on Y-axis
            ball_y = paddle_y - BALL_RADIUS - 1  # Prevent multiple bounces by moving ball slightly up
            score += 1  # Increase score on successful paddle hit
            if score > high_score:  # Update high score if needed
                high_score = score
        
        # Game Over Condition (Ball misses the paddle and falls below screen)
        if ball_y + BALL_RADIUS >= HEIGHT:
            game_active = False  # Stop the game
            game_over = True  # Trigger game over state
            score = 0  # Reset score
            # Reset ball position and direction
            ball_x = random.randint(BALL_RADIUS, WIDTH - BALL_RADIUS)
            ball_y = HEIGHT // 2
            ball_dx = BALL_SPEED_X * random.choice([-1, 1])  # Randomize initial direction
            ball_dy = BALL_SPEED_Y
        
        # Draw the Ball and Paddle on the screen
        pygame.draw.circle(screen, RED, (ball_x, ball_y), BALL_RADIUS)  # Draw ball
        pygame.draw.rect(screen, BLUE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))  # Draw paddle
        
        # Draw Score Display
        score_text = font.render(f"Score: {score}  High Score: {high_score}", True, BLACK)  # Render score text
        screen.blit(score_text, (10, 10))  # Display score in top-left corner
        
        # Update Display to show new frame
        pygame.display.flip()
        
        # # Control game speed (60 FPS)
        clock.tick(60)

# Quit pygame when the loop ends
pygame.quit()


