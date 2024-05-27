import math
from pygame.math import Vector2
from model.solver import VerletSolver
from model.verlet_object import VerletObject

# Square root of 2, used on square diagoanal length
ROOT_2 = 1.414213562373

# Creates a box mesh
def addBox(
    solver: VerletSolver,
    center: Vector2,
    numX: int,
    numY: int,
    objectRadius: float = 15,
    spacing: float = 0.0,
    isCloth: bool = False,
) -> None:
    step = objectRadius * 2.0
    # Box size
    sizeX = numX * step
    sizeY = numY * step

    # Box top-left position
    startX = center.x - sizeX * 0.5 + objectRadius
    startY = center.y - sizeY * 0.5 + objectRadius

    # Save number of objects before adding new ones
    n = len(solver.objects)

    # Create all objects
    for i in range(numX):
        x = startX + step * i
        for j in range(numY):
            obj = VerletObject(Vector2(x, startY + step * j), objectRadius - spacing)
            solver.addObject(obj)

    # Add links
    for i in range(numX - 1):
        for j in range(numY - 1):
            # Get current and neighbors' indexes
            idx0 = (i + 0) * numY + (j + 0)
            idx1 = (i + 0) * numY + (j + 1)
            idx2 = (i + 1) * numY + (j + 0)
            idx3 = (i + 1) * numY + (j + 1)

            # Add three links
            solver.addLink(n + idx0, n + idx1, step)
            solver.addLink(n + idx0, n + idx2, step)

            # Diagonal links needs bigger target distance
            if not isCloth:
                solver.addLink(n + idx0, n + idx3, step * ROOT_2)
                solver.addLink(n + idx2, n + idx1, step * ROOT_2)

    # Add remaining links on last row and last column
    for i in range(numX - 1):
        idx0 = (i + 0) * numY + (numY - 1)
        idx1 = (i + 1) * numY + (numY - 1)
        solver.addLink(n + idx0, n + idx1, step)

    for j in range(numY - 1):
        idx0 = (numX - 1) * numY + (j + 0)
        idx1 = (numX - 1) * numY + (j + 1)
        solver.addLink(n + idx0, n + idx1, step)

# Creates a rope mesh
def addRope(
    solver: VerletSolver,
    start: Vector2,
    end: Vector2,
    numObjects: int = 10,
    spacing: float = 0.0,
    isStartStatic: bool = False,
    isEndStatic: bool = False,
) -> None:
    if start == end:
        print("[utils.addRope]: Start and end positions are the same. Exiting")
        return
    
    # Save number of objects before adding new ones
    n = len(solver.objects)
    
    # Object radius
    radius = (end - start).magnitude() / (numObjects * 2)

    # Add objects
    step = 1 / numObjects
    for i in range(numObjects):
        t = step * i
        isStatic = (isStartStatic and i == 0) or (isEndStatic and i == numObjects - 1)
        solver.addObject(VerletObject(start + (end - start) * t, radius - spacing, isStatic))

    # Add links
    for i in range(numObjects - 1):
        solver.addLink(n + i, n + i + 1, radius * 2)

def addTriangle(
    solver: VerletSolver,
    p0: Vector2,
    p1: Vector2,
    p2: Vector2,
    objectRadius: float = 15,
) -> None:
    # Save number of objects before adding new ones
    n = len(solver.objects)
    
    # Add objects
    solver.addObject(VerletObject(p0, objectRadius))
    solver.addObject(VerletObject(p1, objectRadius))
    solver.addObject(VerletObject(p2, objectRadius))

    # Add links
    solver.addLink(n + 0, n + 1)
    solver.addLink(n + 1, n + 2)
    solver.addLink(n + 2, n + 0)

def addCircle(
    solver: VerletSolver,
    center: Vector2,
    radius: float,
    resolution: int = 4,
    objectRadius: float = 15,
) -> None:
    if resolution < 3:
        print("[utils.addCircle]: Need resolution >= 3")
        return

    # Save number of objects before adding new ones
    n = len(solver.objects)

    # Number of objects
    numObjects = 2 ** resolution

    # Add objects
    step = 1 / numObjects * math.pi * 2.0
    for i in range(numObjects):
        ang = i * step
        x = center.x + math.cos(ang) * radius
        y = center.y + math.sin(ang) * radius

        solver.addObject(VerletObject(Vector2(x, y), objectRadius))

    # Add outline links
    nn = len(solver.objects)
    for i in range(numObjects):
        solver.addLink(n + i, (n + i + 1) % nn)

    # Add inner links for stability
    offsetPower = int(2 ** (resolution - 2))
    for i in range(numObjects):
        idx = n + i
        solver.addLink(idx, (idx + offsetPower - 1) % nn)
        solver.addLink(idx, (idx + offsetPower + 1) % nn)
        solver.addLink(idx, (idx - offsetPower + 1) % nn)
        solver.addLink(idx, (idx - offsetPower - 1) % nn)