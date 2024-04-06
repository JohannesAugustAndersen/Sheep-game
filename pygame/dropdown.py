import pygame
import random

# Farger
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Skjermstørrelse
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Spillerattributter
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_SPEED = 5
PLAYER_JUMP_POWER = 12

# Myntattributter
COIN_RADIUS = 15

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.vel_y = 0
        self.on_ground = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -PLAYER_JUMP_POWER
            self.on_ground = False

        self.vel_y += 0.5
        if self.vel_y > 8:
            self.vel_y = 8
        self.rect.y += self.vel_y
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((COIN_RADIUS * 2, COIN_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (COIN_RADIUS, COIN_RADIUS), COIN_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - COIN_RADIUS * 2)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - COIN_RADIUS * 2)

# Initialisering av pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Plattformspill")

# Gruppe for alle sprites
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Gruppe for mynter
coins = pygame.sprite.Group()
for _ in range(10):
    coin = Coin()
    all_sprites.add(coin)
    coins.add(coin)

# Spilloppdatering
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Kollisjon mellom spiller og mynter
    hits = pygame.sprite.spritecollide(player, coins, True)
    for hit in hits:
        coin = Coin()
        all_sprites.add(coin)
        coins.add(coin)

    # Oppdatering av sprites
    all_sprites.update()

    # Tegn alt på skjermen
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Begrens oppdateringshastigheten
    clock.tick(60)

pygame.quit()
