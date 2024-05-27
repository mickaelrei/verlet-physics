import pygame
from pygame.math import Vector2
from model.verlet_object import VerletObject

class VerletLink:
    def __init__(self, object0: VerletObject, object1: VerletObject, targetDist: float) -> None:
        self.object0 = object0
        self.object1 = object1
        self.targetDist = targetDist

    def accelerate(self, acc: Vector2) -> None:
        self.object0.acceleration += acc
        self.object1.acceleration += acc

    def update(self, dt: float) -> None:
        if self.object0.isStatic and self.object1.isStatic:
            # Both objects are static, so the link is useless
            return

        # Get from one object to another
        axis = self.object0.pos - self.object1.pos
        dist = axis.magnitude()
        dir = axis / dist

        # Differente between current and desired distance
        deltaDist = self.targetDist - dist

        # Check for static objects
        object0disp = 0.5
        object1disp = 0.5
        if self.object0.isStatic:
            # First is static, move only second
            object0disp = 0.0
            object1disp = 1.0
        elif self.object1.isStatic:
            # Second is static, move only first
            object1disp = 0.0
            object0disp = 1.0

        # Update object positions
        self.object0.pos += dir * deltaDist * object0disp
        self.object1.pos -= dir * deltaDist * object1disp

    def draw(self, surface: pygame.Surface, debug: bool = False) -> None:
        pygame.draw.line(surface, (0, 255, 0), self.object0.pos, self.object1.pos, 1)