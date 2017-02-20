import pygame
import operator

pygame.init()
clock = pygame.time.Clock()

done = False


COLOR_BACKGROUND = (0, 0, 80)
COLOR_CIRCLE = (0, 100, 0)


class Cosmos:
    def __init__(self, size=(800, 800)):
        self.size = size
        self.screen = pygame.display.set_mode(size)

    def draw(self):
        self.screen.fill(COLOR_BACKGROUND)

    def contain(self, asteroid):
        pos = asteroid.pos
        if pos[0] > self.size[0]:
            pos[0] = pos[0] - self.size[0]
        if pos[1] > self.size[1]:
            pos[1] = pos[1] - self.size[1]
        if pos[0] < 0:
            pos[0] = pos[0] + self.size[0]
        if pos[1] < 1:
            pos[1] = pos[1] + self.size[1]
        asteroid.pos = pos


class Asteroid:
    def __init__(self):
        self.pos = [300.0, 400.0]
        self.dir = [5.0, 0.0]

    def draw(self, surface):
        pos = [int(c) for c in self.pos]
        pygame.draw.circle(surface, COLOR_CIRCLE, pos, 50, 2)

    def animate(self):
        self.pos = list(map(operator.add, self.pos, self.dir))


cosmos = Cosmos()
asteroid = Asteroid()


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            done = True

    cosmos.draw()

    asteroid.animate()
    cosmos.contain(asteroid)
    asteroid.draw(cosmos.screen)

    pygame.display.flip()
    clock.tick(30)
