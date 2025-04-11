import pygame
from pygame.math import Vector2
import sys
import math

import utils
from model.solver import VerletSolver
from model.verlet_link import VerletLink
from model.verlet_object import VerletObject

pygame.init()
WIDTH = 600
HEIGHT = 600
FPS = 60
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

solver = VerletSolver()

utils.addRope(solver, Vector2(250, 400), Vector2(490, 150), numObjects=35, isStartStatic=True, isEndStatic=True)
utils.addBox(solver, Vector2(300, 200), 4, 4, 10)
utils.addTriangle(solver, Vector2(270, 310), Vector2(310, 310), Vector2(290, 300 - 20*1.414), objectRadius=10)
utils.addCircle(solver, Vector2(100, 200), 70, resolution=5, objectRadius=5)

for i in range(5):
    solver.addObject(VerletObject(Vector2(150 + i * 70, 110), 15))

lastClick: Vector2 | None = None
paused = True
debug = False
holding = False
while True:
    curr_fps = clock.get_fps()
    if curr_fps != 0:
        dt = 1 / clock.get_fps()
    else:
        dt = 1 / FPS
    mousePos = Vector2(pygame.mouse.get_pos())
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                paused = not paused
            if event.key == pygame.K_g:
                debug = not debug
            if event.key == pygame.K_e:
                holding = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_e:
                holding = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            lastClick = mousePos
        elif event.type == pygame.MOUSEBUTTONUP:
            if lastClick == None: continue

            object = VerletObject(lastClick, 15)
            if lastClick != mousePos:
                dir = mousePos - lastClick
                object.pos += dir * dt * 0.1
            
            solver.addObject(object)
            lastClick = None
    
    window.fill((140, 140, 140))
    pygame.draw.circle(window, BLACK, (WIDTH/2, HEIGHT/2), WIDTH/2)

    if not paused:
        if holding:
            # Attract objects towards mouse position
            for object in solver.objects:
                if object.isStatic: continue

                axis = mousePos - object.pos
                object.pos += axis * dt * .05

        solver.update(dt)
    solver.draw(window, debug=debug)

    pygame.display.set_caption(f"Verlet Physics | FPS: {clock.get_fps():.0f}")
    pygame.display.update()
    clock.tick(FPS)