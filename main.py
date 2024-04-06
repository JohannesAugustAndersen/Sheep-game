# Tar utgangspunkt i en annen kode derfor heter "Hindring" klassen min "Platform og "Menneske" 
# klassen "Player". Dette er fordi det blir for mye styr å endre :)

# Jeg har heller ingen "SpillObjekt" klasse, men isteden en "pygame.sprite.Sprite" klasse
# Disse to gjør egentlig det samme, men "pygame.sprite.Sprite" klassen gjør bare enda mer
# og er innebygget i pygame biblioteket

# Splitter parameteren "fart" opp i vfart, hfart, nfart og ofart

# BLE IKKE FERDIG MED KODEN

import pygame
import random

# Farger
WHITE = (255, 255, 255)  # Definerer fargen hvit
BLACK = (0, 0, 0)  # Definerer fargen svart
RED = (255, 0, 0)  # Definerer fargen rød
BLUE = (0, 0, 255)  # Definerer fargen blå
GREEN = (0, 255, 0)  # Definerer fargen grønn
IDK = (255, 0, 255)  # Definerer fargen lilla

# Skjermstørrelse
SCREEN_WIDTH = 800  # Bredde på spillvinduet
SCREEN_HEIGHT = 600  # Høyde på spillvinduet

# Spillerattributter
PLAYER_WIDTH = 50  # Bredde på spilleren
PLAYER_HEIGHT = 50  # Høyde på spilleren
PLAYER_SPEED = 5  # Hastighet til spilleren

# Plattformattributter
PLATFORM_WIDTH = 10  # Bredde på plattformen
PLATFORM_HEIGHT = 100  # Høyde på plattformen

# Sauattributter
SAU_WIDTH = 40
SAU_HEIGHT = 40

# Spøkelseattributter
SPOKELSE_WIDTH = 40
SPOKELSE_HEIGHT = 40
SPOKELSE_SPEED = 10

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))  # Oppretter en overflate for plattformen
        self.image.fill(WHITE)  # Fyller overflaten med hvit farge
        self.rect = self.image.get_rect()  # Henter rektangulær attributt for plattformen
        self.rect.x = x  # Setter x-posisjonen til plattformen
        self.rect.y = y  # Setter y-posisjonen til plattformen

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))  # Oppretter en overflate for spilleren
        self.image.fill(RED)  # Fyller overflaten med rød farge
        self.vfart = PLAYER_SPEED
        self.hfart = PLAYER_SPEED
        self.nfart = PLAYER_SPEED
        self.ofart = PLAYER_SPEED
        self.rect = self.image.get_rect()  # Henter rektangulær attributt for spilleren
        self.rect.x = x
        self.rect.y = y
        self.bærerSau = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()  # Henter tastetrykkene
        if keys[pygame.K_LEFT]:  # Sjekker om venstre-piltasten er trykket
            self.rect.x -= self.vfart  # Flytter spilleren mot venstre
        if keys[pygame.K_RIGHT]:  # Sjekker om høyre-piltasten er trykket
            self.rect.x += self.hfart  # Flytter spilleren mot høyre
        if keys[pygame.K_DOWN]:  # Sjekker om ned-piltasten er trykket
            self.rect.y += self.nfart  # FLytter spilleren ned
        if keys[pygame.K_UP]:  # Sjekker om opp-piltasten er trykket
            self.rect.y -= self.ofart  # Flytter spilleren opp
        
        self.hfart = PLAYER_SPEED
        self.vfart = PLAYER_SPEED
        self.ofart = PLAYER_SPEED
        self.nfart = PLAYER_SPEED
        
        for platform in platforms:  # Går gjennom alle plattformene
            if self.rect.colliderect(platform.rect):  # Sjekker om det er kollisjon med en plattform
                self.hfart = 0
                self.vfart = 0
                
        # Sjekk om spilleren går ut av skjermen
        if self.rect.top < 0 :
            self.ofart = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.hfart = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.nfart = 0
        elif self.rect.left < 0 :
            self.vfart = 0

class Safezone(pygame.sprite.Sprite):
    def __init__(self, bredde, høyde, x, y):
        super().__init__()
        self.image = pygame.Surface((bredde, høyde))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Sau(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((SAU_WIDTH, SAU_HEIGHT))
        self.image.fill(IDK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Spokelse(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((SPOKELSE_WIDTH, SPOKELSE_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])

    def update(self):
        self.rect.x += self.direction_x * SPOKELSE_SPEED
        self.rect.y += self.direction_y * SPOKELSE_SPEED

        if self.rect.y <= 0 or self.rect.y >= SCREEN_HEIGHT:
            self.direction_y *= -1

    def collide(self, sprite):
        if pygame.sprite.collide_rect(self, sprite):
            self.direction_x *= -1
        

# Initialisering av pygame
pygame.init()  # Starter pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Oppretter spillvinduet
pygame.display.set_caption("Plattformspill")  # Setter tittelen på spillvinduet

# Gruppe for alle sprites
all_sprites = pygame.sprite.Group()  # Oppretter gruppen for alle sprites
platforms = pygame.sprite.Group()  # Oppretter gruppen for plattformene
sauer = pygame.sprite.Group()
spokelser = pygame.sprite.Group()


safezone_venstre = Safezone(80, 600, 0, 0)
all_sprites.add(safezone_venstre)

safezone_høyre = Safezone(720, 600, 720, 0)
all_sprites.add(safezone_høyre)

# Legg til spilleren
player = Player(15, 300)  # Oppretter en spiller
all_sprites.add(player)  # Legger til spilleren i alle sprites

# Legg til plattformer
for i in range(3):  # Oppretter 3 plattformer
    platform = Platform(random.randint(100, 700),  # Tilfeldig x-posisjon
                        random.randint(100, 600))  # Tilfeldig y-posisjon
    all_sprites.add(platform)  # Legger til plattformen i alle sprites
    platforms.add(platform)  # Legger til plattformen i plattform-gruppen

# Legg til sauer
for i in range(3):  # Oppretter 3 sauer
    sau = Sau(740, random.randint(0, 500))  # Tilfeldig y-posisjon
    all_sprites.add(sau)  # Legger til sauen i alle sprites
    sauer.add(sau)  # Legger til sauen i sau-gruppen

# Legg til spøkelset
for i in range(1):  # Oppretter 3 sauer
    spokelse = Spokelse()
    all_sprites.add(spokelse)  # Legger til spøkelset i alle sprites
    spokelser.add(spokelse)  # Legger til spøkelset i spokelse-gruppen




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
