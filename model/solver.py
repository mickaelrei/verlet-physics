import pygame
from pygame.math import Vector2
from model.verlet_object import VerletObject
from model.verlet_link import VerletLink

class VerletSolver:
    def __init__(self) -> None:
        self.objects: list[VerletObject] = []
        self.links: list[VerletLink] = []

        self.gravity = Vector2(0, 50)

    def addObject(self, object: VerletObject) -> None:
        self.objects.append(object)

    def addLink(
        self,
        object0idx: int,
        object1idx: int,
        targetDist: float | None = None,
    ) -> None:
        # If same/invalid indexes, cancel
        if object0idx == object1idx:
            print("[VerletSolver.addLink]: Same index")
            return
        if object0idx < 0 or object0idx >= len(self.objects):
            print("[VerletSolver.addLink]: invalid index")
            return
        if object1idx < 0 or object1idx >= len(self.objects):
            print("[VerletSolver.addLink]: invalid index")
            return

        object0 = self.objects[object0idx]
        object1 = self.objects[object1idx]
        if targetDist == None:
            # Use current distance as target
            targetDist = (object0.pos - object1.pos).magnitude()

        # Add new link
        self.links.append(VerletLink(
            object0,
            object1,
            targetDist,
        ))

    def update(self, dt: float) -> None:
        subSteps = 8
        subDt = dt / subSteps
        for i in range(subSteps):
            self.applyGravity()
            self.applyConstraints()
            self.solveCollisions()
            self.updatePositions(subDt)

    def draw(self, surface: pygame.Surface, debug: bool = False) -> None:
        for object in self.objects:
            object.draw(surface, debug)

        if debug:
            for link in self.links:
                link.draw(surface, debug)

    def applyGravity(self) -> None:
        for object in self.objects:
            object.accelerate(self.gravity)

    def applyConstraints(self) -> None:
        constraintPosition = Vector2(300, 300)
        constraintRadius = 300

        for object in self.objects:
            toObj = object.pos - constraintPosition
            dist = toObj.magnitude()
            if dist > constraintRadius - object.radius:
                norm = toObj / dist
                object.pos = constraintPosition + norm * (constraintRadius - object.radius)

    def solveCollisions(self) -> None:
        # TODO: This is O(n²), very inefficient. Use threads to divide work
        size = len(self.objects)
        for i in range(size):
            object0 = self.objects[i]
            for j in range(size):
                if i == j: continue

                object1 = self.objects[j]
                if object0.isStatic and object1.isStatic:
                    # Both static, do not handle collision
                    continue

                # Get vector between both objects
                collAxis = object0.pos - object1.pos

                # Check for distance
                minDist = object0.radius + object1.radius
                dist = collAxis.magnitude()
                if dist < minDist and dist > 0:
                    norm = collAxis / dist
                    delta = minDist - dist

                    # Check for static objects
                    # Both objects initially will displace by 50%
                    object0disp = 0.5
                    object1disp = 0.5
                    if object0.isStatic:
                        # First is static, move only second
                        object0disp = 0.0
                        object1disp = 1.0
                    elif object1.isStatic:
                        # Second is static, move only first
                        object1disp = 0.0
                        object0disp = 1.0

                    object0.pos += object0disp * norm * delta
                    object1.pos -= object1disp * norm * delta

    def updatePositions(self, dt: float) -> None:
        for object in self.objects:
            object.update(dt)

        for link in self.links:
            link.update(dt)
