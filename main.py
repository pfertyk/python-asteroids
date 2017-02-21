import pygame
import operator
import random
import math

pygame.init()
clock = pygame.time.Clock()

done = False


COLOR_BACKGROUND = (0, 0, 80)
COLOR_CIRCLE = (0, 100, 0)
COLOR_BULLET = (100, 0, 0)


class Screen:
    def __init__(self, size=(800, 800)):
        self.size = size
        self.background = pygame.display.set_mode(size)

    def draw(self):
        self.background.fill(COLOR_BACKGROUND)

    def draw_object(self, obj):
        obj.draw(self.background)

    def contain_object(self, obj):
        pos = obj.pos
        if pos[0] > self.size[0]:
            pos[0] = pos[0] - self.size[0]
        if pos[1] > self.size[1]:
            pos[1] = pos[1] - self.size[1]
        if pos[0] < 0:
            pos[0] = pos[0] + self.size[0]
        if pos[1] < 1:
            pos[1] = pos[1] + self.size[1]
        obj.pos = pos


class Asteroid:
    def __init__(self, pos=None):
        if not pos:
            pos = [400.0, 400.0]

        angle = 2 * math.pi * random.random()
        self.pos = pos
        self.dir = [5.0*math.sin(angle), 5.0*math.cos(angle)]
        self.radius = 50

    def draw(self, surface):
        pos = [int(c) for c in self.pos]
        pygame.draw.circle(surface, COLOR_CIRCLE, pos, self.radius, 2)

    def animate(self):
        self.pos = list(map(operator.add, self.pos, self.dir))


class Bullet:
    def __init__(self, pos=None):
        if not pos:
            pos = [300.0, 400.0]

        angle = 2 * math.pi * random.random()
        self.pos = pos
        self.dir = [9.0*math.sin(angle), 9.0*math.cos(angle)]
        self.radius = 10

    def draw(self, surface):
        pos = [int(c) for c in self.pos]
        pygame.draw.circle(surface, COLOR_BULLET, pos, self.radius, 2)

    def animate(self):
        self.pos = list(map(operator.add, self.pos, self.dir))

    def collides_with(self, other_obj):
        distance = math.sqrt(
            (self.pos[0]-other_obj.pos[0])**2 +
            (self.pos[1]-other_obj.pos[1])**2
        )
        return distance < self.radius + other_obj.radius

screen = Screen()

asteroids = []
for _ in range(6):
    angle = 2 * math.pi * random.random()
    pos = [400+300*math.sin(angle), 400+300*math.cos(angle)]
    asteroids.append(Asteroid(pos))

bullets = []
for _ in range(6):
    angle = 2 * math.pi * random.random()
    pos = [400+300*math.sin(angle), 400+300*math.cos(angle)]
    bullets.append(Bullet(pos))


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            done = True

    screen.draw()

    for bullet in bullets:
        for asteroid in asteroids:
            if bullet.collides_with(asteroid):
                asteroids.remove(asteroid)

    for asteroid in asteroids:
        asteroid.animate()
        screen.contain_object(asteroid)
        screen.draw_object(asteroid)

    for bullet in bullets:
        bullet.animate()
        screen.contain_object(bullet)
        screen.draw_object(bullet)

    pygame.display.flip()
    clock.tick(30)
