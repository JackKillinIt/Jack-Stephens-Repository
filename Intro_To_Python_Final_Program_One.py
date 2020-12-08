import math
import pygame

# Creating colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Size of break-out bricks
brick_width = 23
brick_height = 15

class Brick(pygame.sprite.Sprite):
    def __init__(self, color, x, y):

        # Call the Sprite constructor
        super().__init__()

        # Create the image of the brick
        self.image = pygame.Surface([brick_width, brick_height])

        # Color the brick
        self.image.fill(color)

        # Fetch the rectangle object with the same dimensions as the brick
        self.rect = self.image.get_rect()

        # Move the top left of the brick to x, y. This is where the brick will appear
        self.rect.x = x
        self.rect.y = y

class Ball(pygame.sprite.Sprite):

    # Speed of ball in pixels per cycle
    speed = 5.0

    # Floating point representation of where the ball is
    x = 0.0
    y = 180.0

    # Direction of ball (in degrees)
    direction = 200

    width = 10
    height = 10

    # Constructor. Pass in the color of the brick, and it's x and y position.
    def __init__(self):

        # Call the Sprite constructor again
        super().__init__()

        # Create the sprite of the ball
        self.image = pygame.Surface([self.width, self.height])

        # Color the ball
        self.image.fill(white)

        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()

        # Get attributes for the height / width of the screen
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

    def bounce(self, diff):

        self.direction = (180 - self.direction) % 360
        self.direction -= diff

    def update(self):

        # Sine and Cosine work in degrees, so we convert them to radians
        direction_radians = math.radians(self.direction)

        # Change the ball's position according to its speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        # Move the ball to its new position
        self.rect.x = self.x
        self.rect.y = self.y

        # If the ball hits the top of the screen:
        if self.y <= 0:
            self.bounce(0)
            self.y = 1

        # If the ball hits the left of the screen:
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1

        # If the ball hits the right side of the screen:
        if self.x > self.screenwidth - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.screenwidth - self.width - 1

        # If the player misses the ball and it hits the bottom of the screen:
        if self.y > 600:
            return True
        else:
            return False

class Player(pygame.sprite.Sprite):

    def __init__(self):

        # Call the Sprite Constructor again
        super().__init__()

        self.width = 75
        self.height = 15
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((white))

        # Set the ball's starting location to the top-left corner of the screen
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        self.rect.x = 0
        self.rect.y = self.screenheight - self.height

    def update(self):

        # Fetch where the mouse is to update the player's position
        pos = pygame.mouse.get_pos()

        # Set the left side of the player bar to the mouse position
        self.rect.x = pos[0]

        # Make sure player paddle doesn't go off the screen
        if self.rect.x > self.screenwidth - self.width:
            self.rect.x = self.screenwidth - self.width

# Initiate Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode([800, 600])

# Set the title of the window
pygame.display.set_caption('Breakout: The Classic Brick Breaker Game!')

# Make the mouse disappear when hovering the window
pygame.mouse.set_visible(0)

# Set the font
font = pygame.font.Font(None, 36)

# Create a surface to be drawn on
background = pygame.Surface(screen.get_size())

# Create a list of all the sprites
bricks = pygame.sprite.Group()
balls = pygame.sprite.Group()
allsprites = pygame.sprite.Group()

# Create the player paddle object
player = Player()
allsprites.add(player)

# Create the ball
ball = Ball()
allsprites.add(ball)
balls.add(ball)

# The top of the brick (y)
top = 80

# Number of bricks
brickcount = 32

# Creating the bricks

# Five rows of bricks
for row in range(5):

    # 32 columns of bricks
    for column in range(0, brickcount):

        # Create a brick
        brick = Brick(red, column * (brick_width + 2) + 1, top)
        bricks.add(brick)
        allsprites.add(brick)

    # Move the top of the next row down
    top += brick_height + 2

# Crick to limit speed
clock = pygame.time.Clock()

# Has the game ended?
game_over = False

# Exit the program?
close_program = False

# Main program loop
while not close_program:

    # Limit to 60 fps
    clock.tick(60)

    # Clear the screen
    screen.fill(black)

    # Process the events in the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_program = True

    # Update the ball and player position as long as the game is still going on
    if not game_over:
        player.update()
        game_over = ball.update()

    # If the game is donw, print game over
    if game_over:
        text = font.render("Game Over", True, white)
        textpos = text.get_rect(centerx = background.get_width()/2)
        textpos.top = 300
        screen.blit(text, textpos)
        close_program = True

    # See if the ball hits the player's paddle
    if pygame.sprite.spritecollide(player, balls, False):

        # 'Diff' allows you to bounce the ball left or right depending on what part of the paddle the player hits the ball with
        diff = (player.rect.x + player.width/2) - (ball.rect.x + ball.width / 2)

        # Set the ball's position in case the ball hits the edge of the paddle
        ball.rect.y = screen.get_height() - player.rect.height - ball.rect.height - 1
        ball.bounce(diff)

    # Check for collisions between the ball and the bricks
    deadbricks = pygame.sprite.spritecollide(ball, bricks, True)

    # If the player hits a brick, bounce the ball
    if len(deadbricks) > 0:
        ball.bounce(0)

        # Game ends when all the bricks have been destroyed
        if len(bricks) == 0:
            text = font.render("You Win! Great Job!", True, white)
            textpos = text.get_rect(centerx = background.get_width()/2)
            textpos.top = 300
            screen.blit(text, textpos)
            close_program = True

    # Draw everything
    allsprites.draw(screen)

    # Flip the screen and show what has been drawn
    pygame.display.flip()

pygame.quit()
