import pygame
from pygame.math import Vector2

# Color for non static objects
NON_STATIC_COLOR = (255, 40, 40)

# Color for static objects
STATIC_COLOR = (40, 110, 255)

class VerletObject:
    def __init__(self, pos: Vector2, radius: float, isStatic: bool=False) -> None:
        self.pos = pos.copy()
        self.radius = radius
        self.isStatic = isStatic

        self.lastPos = self.pos.copy()
        self.acceleration = Vector2(0.0)

    def accelerate(self, acc: Vector2) -> None:
        self.acceleration += acc

    def update(self, dt: float) -> None:
        if self.isStatic: return

        # Get velocity from both positions
        velocity = self.pos - self.lastPos

        # Save current position
        self.lastPos = self.pos

        # Verlet integration
        self.pos = self.pos + velocity + self.acceleration * dt * dt

        # Reset acceleration
        self.acceleration = Vector2(0.0)

    def draw(self, surface: pygame.Surface, debug: bool = False) -> None:
        color = STATIC_COLOR if self.isStatic else NON_STATIC_COLOR
        pygame.draw.circle(surface, color, self.pos, self.radius)