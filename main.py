import pygame
import operator
import random
import math

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 64)

done = False
status = ""


COLOR_BACKGROUND = (0, 0, 80)
COLOR_ASTEROID = (0, 100, 0)
COLOR_BULLET = (100, 0, 0)
COLOR_STARSHIP = (100, 100, 100)
COLOR_FONT = (200, 200, 0)


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
    def __init__(self, pos, radius, speed, angle):
        self.pos = pos
        self.dir = [speed*math.cos(angle), speed*math.sin(angle)]
        self.radius = radius

    def draw(self, surface):
        pos = [int(c) for c in self.pos]
        pygame.draw.circle(surface, self.color, pos, self.radius, 2)

    def animate(self):
        self.pos = list(map(operator.add, self.pos, self.dir))


class Asteroid(Object):
    color = COLOR_ASTEROID

    def __init__(self, pos, radius=50, speed=5.0):
        angle = 2 * math.pi * random.random()
        super().__init__(pos, radius, speed, angle)

    def split(self):
        if self.radius >= 30:
            speed = random.random() * 5
            radius = self.radius - 10
            return [Asteroid(self.pos, radius, speed) for _ in range(2)]
        else:
            return None


class Bullet(Object):
    color = COLOR_BULLET

    def __init__(self, pos, angle, radius=10, speed=9.0):
        super().__init__(pos, radius, speed, angle)

    def collides_with(self, other_obj):
        distance = math.sqrt(
            (self.pos[0]-other_obj.pos[0])**2 +
            (self.pos[1]-other_obj.pos[1])**2
        )
        return distance < self.radius + other_obj.radius


class Starship(Object):
    color = COLOR_STARSHIP

    def __init__(self, pos):
        super().__init__(pos, 20, 0.0, 0)
        radius = self.radius
        self.surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.lines(
            self.surface, self.color, True, [(20, 0), (10, 20), (30, 20)], 2
        )
        pygame.draw.circle(
            self.surface, self.color, (radius, radius), radius, 2
        )
        self.angle = -90.0
        self.acc = 1.0

    def draw(self, surface):
        sur = pygame.transform.rotozoom(self.surface, -self.angle-90.0, 1.0)
        pos = [int(c-sur.get_width()/2) for c in self.pos]
        surface.blit(sur, pos)

    def rotate(self, clockwise=True):
        direction = 1 if clockwise else -1
        self.angle += 4.0 * direction

    def move(self):
        self.dir[0] += math.cos(self.angle / 180.0 * math.pi) * self.acc
        self.dir[1] += math.sin(self.angle / 180.0 * math.pi) * self.acc

screen = Screen()
starship = Starship([400, 400])

asteroids = []
bullets = []

for _ in range(6):
    angle = 2 * math.pi * random.random()
    pos = [400+300*math.sin(angle), 400+300*math.cos(angle)]
    asteroids.append(Asteroid(pos))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            angle = starship.angle / 180.0 * math.pi
            bullets.append(Bullet(starship.pos, angle))

    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        starship.rotate(True)
    elif pygame.key.get_pressed()[pygame.K_LEFT]:
        starship.rotate(False)
    if pygame.key.get_pressed()[pygame.K_UP]:
        starship.move()

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

    if not asteroids:
        status = "You won!"

    for asteroid in asteroids:
        asteroid.animate()
        screen.contain_object(asteroid)
        screen.draw_object(asteroid)

    for bullet in bullets:
        bullet.animate()
        screen.contain_object(bullet)
        screen.draw_object(bullet)

    starship.animate()
    screen.contain_object(starship)
    screen.draw_object(starship)

    if status:
        text = font.render(status, 1, COLOR_FONT)
        rect = text.get_rect()
        rect.center = (400, 400)
        screen.background.blit(text, rect)

    pygame.display.flip()
    clock.tick(30)
