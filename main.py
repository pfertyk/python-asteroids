import pygame
import operator
import random
import math

pygame.init()
clock = pygame.time.Clock()

done = False


COLOR_BACKGROUND = (0, 0, 80)
COLOR_ASTEROID = (0, 100, 0)
COLOR_BULLET = (100, 0, 0)
COLOR_STARSHIP = (100, 100, 100)


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


class Object:
    def __init__(self, pos, radius, speed):
        angle = 2 * math.pi * random.random()
        self.pos = pos
        self.dir = [speed*math.sin(angle), speed*math.cos(angle)]
        self.radius = radius

    def draw(self, surface):
        pos = [int(c) for c in self.pos]
        pygame.draw.circle(surface, self.color, pos, self.radius, 2)

    def animate(self):
        self.pos = list(map(operator.add, self.pos, self.dir))


class Asteroid(Object):
    color = COLOR_ASTEROID

    def __init__(self, pos, radius=50, speed=5.0):
        super().__init__(pos, radius, speed)

    def split(self):
        if self.radius >= 30:
            speed = random.random() * 5
            radius = self.radius - 10
            return [Asteroid(self.pos, radius, speed) for _ in range(2)]
        else:
            return None


class Bullet(Object):
    color = COLOR_BULLET

    def __init__(self, pos, radius=10, speed=9.0):
        super().__init__(pos, radius, speed)

    def collides_with(self, other_obj):
        distance = math.sqrt(
            (self.pos[0]-other_obj.pos[0])**2 +
            (self.pos[1]-other_obj.pos[1])**2
        )
        return distance < self.radius + other_obj.radius


class Starship(Object):
    color = COLOR_STARSHIP

    def __init__(self, pos):
        super().__init__(pos, 20, 0.0)
        radius = self.radius
        self.surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.lines(
            self.surface, self.color, True, [(20, 0), (10, 20), (30, 20)], 2
        )
        pygame.draw.circle(
            self.surface, self.color, (radius, radius), radius, 2
        )

    def draw(self, surface):
        pos = [int(c-self.radius) for c in self.pos]
        surface.blit(self.surface, pos)

screen = Screen()
starship = Starship([400, 400])

asteroids = []
bullets = []

for _ in range(6):
    angle = 2 * math.pi * random.random()
    pos = [400+300*math.sin(angle), 400+300*math.cos(angle)]
    asteroids.append(Asteroid(pos))

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
                new_asteroids = asteroid.split()
                if new_asteroids:
                    asteroids.extend(new_asteroids)
                asteroids.remove(asteroid)
                bullets.remove(bullet)
                break

    for asteroid in asteroids:
        asteroid.animate()
        screen.contain_object(asteroid)
        screen.draw_object(asteroid)

    for bullet in bullets:
        bullet.animate()
        screen.contain_object(bullet)
        screen.draw_object(bullet)

    screen.draw_object(starship)

    pygame.display.flip()
    clock.tick(30)
