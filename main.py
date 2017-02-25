import pygame
import operator
import random
import math

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 64)
screen = pygame.display.set_mode((800, 800))

IMG_EARTH = pygame.image.load('earth.png').convert()
IMG_ASTEROID_BIG = pygame.image.load('asteroid-big.png').convert_alpha()
IMG_ASTEROID_MEDIUM = pygame.image.load('asteroid-medium.png').convert_alpha()
IMG_ASTEROID_SMALL = pygame.image.load('asteroid-small.png').convert_alpha()
IMG_BULLET = pygame.image.load('bullet.png').convert_alpha()
IMG_STARSHIP = pygame.image.load('starship.png').convert_alpha()

done = False
status = ""


class Screen:
    def __init__(self, screen_surface):
        self.background = screen_surface
        self.size = screen_surface.get_size()

    def draw(self):
        self.background.blit(IMG_EARTH, (0, 0))

    def draw_object(self, obj):
        obj.draw(self.background)

    def contain_object(self, obj):
        pos = obj.pos
        orig_pos = pos[:]
        if pos[0] > self.size[0]:
            pos[0] = pos[0] - self.size[0]
        if pos[1] > self.size[1]:
            pos[1] = pos[1] - self.size[1]
        if pos[0] < 0:
            pos[0] = pos[0] + self.size[0]
        if pos[1] < 1:
            pos[1] = pos[1] + self.size[1]
        return pos != orig_pos


class Object:
    def __init__(self, pos, radius, speed, angle):
        self.pos = pos
        self.dir = [speed*math.cos(angle), speed*math.sin(angle)]
        self.radius = radius

    def draw(self, surface):
        pos = [int(c-self.radius) for c in self.pos]
        surface.blit(self.image, pos)

    def animate(self):
        self.pos = list(map(operator.add, self.pos, self.dir))

    def collides_with(self, other_obj):
        distance = math.sqrt(
            (self.pos[0]-other_obj.pos[0])**2 +
            (self.pos[1]-other_obj.pos[1])**2
        )
        return distance < self.radius + other_obj.radius


class Asteroid(Object):
    def __init__(self, pos, image=IMG_ASTEROID_BIG, radius=50, speed=5.0):
        self.image = image
        angle = 2 * math.pi * random.random()
        super().__init__(pos, radius, speed, angle)

    def split(self):
        if self.radius > 30:
            speed = random.random() * 5
            radius = self.radius - 10
            if radius == 40:
                image = IMG_ASTEROID_MEDIUM
            else:
                image = IMG_ASTEROID_SMALL
            return [Asteroid(self.pos, image, radius, speed) for _ in range(2)]
        else:
            return None


class Bullet(Object):
    image = IMG_BULLET

    def __init__(self, pos, angle, radius=10, speed=9.0):
        super().__init__(pos, radius, speed, angle)


class Starship(Object):

    def __init__(self, pos):
        super().__init__(pos, 20, 0.0, 0)
        self.angle = -90.0
        self.acc = 1.0

    def draw(self, surface):
        sur = pygame.transform.rotozoom(IMG_STARSHIP, -self.angle-90.0, 1.0)
        pos = [int(c-sur.get_width()/2) for c in self.pos]
        surface.blit(sur, pos)

    def rotate(self, clockwise=True):
        direction = 1 if clockwise else -1
        self.angle += 4.0 * direction

    def move(self):
        self.dir[0] += math.cos(self.angle / 180.0 * math.pi) * self.acc
        self.dir[1] += math.sin(self.angle / 180.0 * math.pi) * self.acc


screen = Screen(screen)
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
            if starship:
                angle = starship.angle / 180.0 * math.pi
                bullets.append(Bullet(starship.pos, angle))

    screen.draw()

    if asteroids or starship:
        for asteroid in asteroids:
            for bullet in bullets:
                if bullet.collides_with(asteroid):
                    new_asteroids = asteroid.split()
                    if new_asteroids:
                        asteroids.extend(new_asteroids)
                    asteroids.remove(asteroid)
                    bullets.remove(bullet)
                    if not asteroids:
                        status = "You won!"
                    break

            if starship and asteroid.collides_with(starship):
                starship = None
                status = "You lost!"

    for asteroid in asteroids:
        asteroid.animate()
        screen.contain_object(asteroid)
        screen.draw_object(asteroid)

    for bullet in bullets:
        bullet.animate()
        if screen.contain_object(bullet):
            bullets.remove(bullet)
            continue
        screen.draw_object(bullet)

    if starship:
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            starship.rotate(True)
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            starship.rotate(False)
        if pygame.key.get_pressed()[pygame.K_UP]:
            starship.move()

        starship.animate()
        screen.contain_object(starship)
        screen.draw_object(starship)

    if status:
        text = font.render(status, 1, (200, 200, 0))
        rect = text.get_rect()
        rect.center = (400, 400)
        screen.background.blit(text, rect)

    pygame.display.flip()
    clock.tick(30)
