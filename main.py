import pygame
import random
from itertools import chain

from utils import GameObject as GM, get_random_pos, change_dir

# PYGAME RESOURCES
pygame.init()

SCREEN = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Asteroids')

IMG_EARTH = pygame.image.load('earth.png').convert()
IMG_ASTEROID_BIG = pygame.image.load('asteroid-big.png').convert_alpha()
IMG_ASTEROID_MEDIUM = pygame.image.load('asteroid-medium.png').convert_alpha()
IMG_ASTEROID_SMALL = pygame.image.load('asteroid-small.png').convert_alpha()
IMG_BULLET = pygame.image.load('bullet.png').convert_alpha()
IMG_STARSHIP = pygame.image.load('starship.png').convert_alpha()

CLOCK = pygame.time.Clock()
FONT = pygame.font.Font(None, 64)


# GAME CLASSES AND METHODS
def print_message(surface, message, font):
    if message:
        size = surface.get_size()
        text = font.render(message, 1, (200, 200, 0))
        rect = text.get_rect()
        rect.center = (size[0] / 2, size[1] / 2)
        surface.blit(text, rect)


class GameObject(GM):
    def draw(self, surface):
        pos = [int(c-self.radius) for c in self.pos]
        surface.blit(self.image, pos)


class Asteroid(GameObject):
    def __init__(self, pos, image=IMG_ASTEROID_BIG, radius=50, speed=3.0):
        self.image = image
        angle = 360 * random.random()
        speed = max(1, random.random() * speed)
        super().__init__(pos, radius, speed, angle)

    def split(self):
        if self.radius > 30:
            radius = self.radius - 10
            if radius == 40:
                image = IMG_ASTEROID_MEDIUM
            else:
                image = IMG_ASTEROID_SMALL
            return [Asteroid(self.pos, image, radius) for _ in range(2)]
        else:
            return None


class Bullet(GameObject):
    image = IMG_BULLET

    def __init__(self, pos, angle, radius=5, speed=8.0):
        super().__init__(pos, radius, speed, angle)


class Starship(GameObject):
    def __init__(self, pos):
        super().__init__(pos, 20, 0.0, 0)
        self.angle = -90.0
        self.acc = 0.4

    def draw(self, surface):
        sur = pygame.transform.rotozoom(IMG_STARSHIP, -self.angle - 90.0, 1.0)
        pos = [int(c - sur.get_width() / 2) for c in self.pos]
        surface.blit(sur, pos)

    def rotate(self, clockwise=True):
        direction = 1 if clockwise else -1
        self.angle += 4.0 * direction

    def move(self):
        change_dir(self.dir, self.angle, self.acc)

# GAME INIT
starship = Starship([400, 300])

asteroids = []
bullets = []

done = False
status_text = ''

for _ in range(6):
    asteroids.append(Asteroid(get_random_pos(800, 600)))

while not done:
    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            elif event.key == pygame.K_SPACE and starship:
                bullets.append(Bullet(starship.pos, starship.angle))
    # LOGIC
    if starship:
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            starship.rotate(True)
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            starship.rotate(False)
        if pygame.key.get_pressed()[pygame.K_UP]:
            starship.move()
        starship.contain(SCREEN)

    for asteroid in asteroids:
        asteroid.contain(SCREEN)
        for bullet in bullets:
            if bullet.contain(SCREEN):
                bullets.remove(bullet)
                continue
            if bullet.collides_with(asteroid):
                new_asteroids = asteroid.split()
                if new_asteroids:
                    asteroids.extend(new_asteroids)
                asteroids.remove(asteroid)
                bullets.remove(bullet)
                if not asteroids:
                    status_text = "You won!"
                break

        if starship and asteroid.collides_with(starship):
            starship = None
            status_text = "You lost!"
    # DRAWING
    SCREEN.blit(IMG_EARTH, (0, 0))
    for obj in chain(asteroids, bullets, (starship, ) if starship else ()):
        obj.animate()
        obj.draw(SCREEN)
    print_message(SCREEN, status_text, FONT)

    pygame.display.flip()
    CLOCK.tick(60)
