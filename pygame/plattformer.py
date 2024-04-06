import pygame
import random

# Farger
WHITE = (255, 255, 255)  # Definerer fargen hvit
BLACK = (0, 0, 0)  # Definerer fargen svart
RED = (255, 0, 0)  # Definerer fargen rød

# Skjermstørrelse
SCREEN_WIDTH = 800  # Bredde på spillvinduet
SCREEN_HEIGHT = 600  # Høyde på spillvinduet

# Spillerattributter
PLAYER_WIDTH = 50  # Bredde på spilleren
PLAYER_HEIGHT = 50  # Høyde på spilleren
PLAYER_SPEED = 5  # Hastighet til spilleren
PLAYER_JUMP_POWER = 12  # Styrken til spillerhoppet

# Plattformattributter
PLATFORM_WIDTH = 100  # Bredde på plattformen
PLATFORM_HEIGHT = 20  # Høyde på plattformen

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))  # Oppretter en overflate for spilleren
        self.image.fill(RED)  # Fyller overflaten med rød farge
        self.rect = self.image.get_rect()  # Henter rektangulær attributt for spilleren
        self.vel_y = 0  # Vertikal hastighet til spilleren
        self.on_ground = False  # Variabel for å sjekke om spilleren er på bakken

    def update(self, platforms):
        keys = pygame.key.get_pressed()  # Henter tastetrykkene
        if keys[pygame.K_LEFT]:  # Sjekker om venstre-piltasten er trykket
            self.rect.x -= PLAYER_SPEED  # Flytter spilleren mot venstre
        if keys[pygame.K_RIGHT]:  # Sjekker om høyre-piltasten er trykket
            self.rect.x += PLAYER_SPEED  # Flytter spilleren mot høyre
        if keys[pygame.K_SPACE] and self.on_ground:  # Sjekker om mellomromstasten er trykket og spilleren er på bakken
            self.vel_y = -PLAYER_JUMP_POWER  # Setter vertikal hastighet til spillerhoppet
            self.on_ground = False  # Spilleren er ikke lenger på bakken

        self.vel_y += 0.5  # Legger til gravitasjon på vertikal hastighet
        if self.vel_y > 8:  # Begrenser fallhastigheten til spilleren
            self.vel_y = 8
        self.rect.y += self.vel_y  # Oppdaterer spillerens vertikale posisjon

        self.on_ground = False  # Setter at spilleren ikke er på bakken
        for platform in platforms:  # Går gjennom alle plattformene
            if self.rect.colliderect(platform.rect):  # Sjekker om det er kollisjon med en plattform
                if self.vel_y > 0:  # Sjekker om spilleren faller nedover
                    self.rect.bottom = platform.rect.top  # Plasserer spilleren på toppen av plattformen
                    self.vel_y = 0  # Nullstiller vertikal hastighet
                    self.on_ground = True  # Spilleren er på bakken
                elif self.vel_y < 0:  # Sjekker om spilleren hopper oppover
                    self.rect.top = platform.rect.bottom  # Plasserer spilleren under plattformen
                    self.vel_y = 0  # Nullstiller vertikal hastighet

        # Sjekk om spilleren har falt ut av skjermen
        if self.rect.top > SCREEN_HEIGHT: 
            self.kill()  # Fjerner spilleren fra gruppen
            self.rect.topleft = (0, 0)  # Plasserer spilleren helt oppe i venstre hjørne
            all_sprites.add(self)  # Legger til spilleren på nytt

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))  # Oppretter en overflate for plattformen
        self.image.fill(WHITE)  # Fyller overflaten med hvit farge
        self.rect = self.image.get_rect()  # Henter rektangulær attributt for plattformen
        self.rect.x = x  # Setter x-posisjonen til plattformen
        self.rect.y = y  # Setter y-posisjonen til plattformen

# Initialisering av pygame
pygame.init()  # Starter pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Oppretter spillvinduet
pygame.display.set_caption("Plattformspill")  # Setter tittelen på spillvinduet

# Gruppe for alle sprites
all_sprites = pygame.sprite.Group()  # Oppretter gruppen for alle sprites
platforms = pygame.sprite.Group()  # Oppretter gruppen for plattformene

# Legg til plattformer
for i in range(10):  # Oppretter 10 plattformer
    platform = Platform(random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH),  # Tilfeldig x-posisjon
                        random.randint(100, SCREEN_HEIGHT - PLATFORM_HEIGHT))  # Tilfeldig y-posisjon
    all_sprites.add(platform)  # Legger til plattformen i alle sprites
    platforms.add(platform)  # Legger til plattformen i plattform-gruppen

# Legg til spilleren
player = Player()  # Oppretter en spiller
all_sprites.add(player)  # Legger til spilleren i alle sprites

# Spilloppdatering
running = True  # Variabel for å kontrollere om spillet kjører eller ikke
clock = pygame.time.Clock()  # Lager et Clock-objekt for å styre oppdateringshastigheten
while running:
    for event in pygame.event.get():  # Henter hendelser fra køen
        if event.type == pygame.QUIT:  # Sjekker om spilleren har lukket spillvinduet
            running = False  # Setter running til False for å avslutte spillet

    # Oppdatering av spilleren
    player.update(platforms)

    # Tegn alt på skjermen
    screen.fill(BLACK)  # Fyller skjermen med svart farge
    all_sprites.draw(screen)  # Tegner alle sprites på skjermen
    pygame.display.flip()  # Oppdaterer skjermen

    # Begrens oppdateringshastigheten
    clock.tick(60)  # Begrenser oppdateringshastigheten til 60 bilder per sekund

pygame.quit()  # Avslutter pygame
