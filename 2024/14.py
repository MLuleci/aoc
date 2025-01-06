import re
import pygame
import math

WIDTH = 101
HEIGHT = 103
SIZE = 5

def step(x, y, vx, vy):
    return (x + vx) % WIDTH, (y + vy) % HEIGHT, vx, vy

def step_all(robots):
    return [ step(*i) for i in robots ]

def safety(robots):
    positions = [ (x, y) for x, y, *_ in robots ]
    q1 = sum([ x < WIDTH // 2 and y < HEIGHT // 2 for x, y in positions ])
    q2 = sum([ x < WIDTH // 2 and y > HEIGHT // 2 for x, y in positions ])
    q3 = sum([ x > WIDTH // 2 and y < HEIGHT // 2 for x, y in positions ])
    q4 = sum([ x > WIDTH // 2 and y > HEIGHT // 2 for x, y in positions ])
    return q1 * q2 * q3 * q4

def step_n(robots, n):
    for _ in range(n):
        robots = step_all(robots)
    return robots

def silver(robots):
    robots = step_n(robots, 100)
    print(safety(robots))

def variance(x):
    s = sum(x)
    m = s / len(x)
    return 1 / len(x) * sum([ (i - m) * (i - m) for i in x ])

with open("14.txt") as f:
    robots = [ [ int(j) for j in re.split(r"[^-\d]+", i)[1:-1] ] for i in f.readlines() ]
    silver(robots)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH * SIZE, HEIGHT * SIZE))
    clock = pygame.time.Clock()

    second = 0
    min_variance = math.inf
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        robots = step_all(robots)
        x = [ x for x, *_ in robots ]
        y = [ y for _, y, *_ in robots ]
        total_variance = variance(x) + variance(y)
        if total_variance < min_variance:
            min_variance = total_variance

            screen.fill("black")
            for x, y, *_ in robots:
                pygame.draw.rect(screen, "green", pygame.Rect(x * SIZE, y * SIZE, SIZE, SIZE))
            pygame.display.flip()

            print(second, end="\r")
        second += 1

        clock.tick(60)
    pygame.quit()
    print(7344) # my answer