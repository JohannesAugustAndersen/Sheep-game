import pygame
import random

# Definerer noen konstanter
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_RADIUS = 10
PADDLE_SPEED = 5
BALL_SPEED = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definerer Paddle klassen
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([PADDLE_WIDTH, PADDLE_HEIGHT])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move_up(self):
        self.rect.y -= PADDLE_SPEED
        if self.rect.y < 0:
            self.rect.y = 0

    def move_down(self):
        self.rect.y += PADDLE_SPEED
        if self.rect.y > SCREEN_HEIGHT - PADDLE_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - PADDLE_HEIGHT

# Definerer Ball klassen
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([BALL_RADIUS * 2, BALL_RADIUS * 2])
        self.image.fill(WHITE)
        pygame.draw.circle(self.image, BLACK, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])

    def update(self):
        self.rect.x += self.direction_x * BALL_SPEED
        self.rect.y += self.direction_y * BALL_SPEED

        if self.rect.y <= 0 or self.rect.y >= SCREEN_HEIGHT - BALL_RADIUS * 2:
            self.direction_y *= -1

    def collide(self, sprite):
        if pygame.sprite.collide_rect(self, sprite):
            self.direction_x *= -1

# Initialiserer Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# Oppretter spiller og ball objekter
player1 = Paddle(20, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
player2 = Paddle(SCREEN_WIDTH - 20 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball()

# Oppretter en gruppe for spillobjekter
all_sprites = pygame.sprite.Group()
all_sprites.add(player1, player2, ball)

# Spillets hovedløkke
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player1.move_up()
    if keys[pygame.K_s]:
        player1.move_down()
    if keys[pygame.K_UP]:
        player2.move_up()
    if keys[pygame.K_DOWN]:
        player2.move_down()

    # Oppdaterer ballens bevegelse
    ball.update()

    # Sjekker kollisjon med paddles
    ball.collide(player1)
    ball.collide(player2)

    # Tegner alt på skjermen
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Oppdaterer skjermen
    pygame.display.flip()

    # Setter oppdateringshastighet
    clock.tick(60)

# Avslutter Pygame
pygame.quit()
