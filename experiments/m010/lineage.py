"""Deterministic abstract cell lineage; not an embryo model."""
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Cell:
    identifier: int
    parent: int | None
    generation: int
    x: float
    y: float

class Lineage:
    def __init__(self):
        self.cells = {0: Cell(0, None, 0, 0.0, 0.0)}
        self.next_id = 1

    def divide(self, identifier: int, separation: float = 1.0, angle: float = 0.0):
        if identifier not in self.cells:
            raise KeyError(identifier)
        if not math.isfinite(separation) or separation <= 0 or not math.isfinite(angle):
            raise ValueError('separation must be positive and parameters finite')
        mother = self.cells.pop(identifier)
        dx = 0.5 * separation * math.cos(angle)
        dy = 0.5 * separation * math.sin(angle)
        children = (Cell(self.next_id, identifier, mother.generation + 1, mother.x - dx, mother.y - dy),
                    Cell(self.next_id + 1, identifier, mother.generation + 1, mother.x + dx, mother.y + dy))
        self.next_id += 2
        self.cells.update((child.identifier, child) for child in children)
        return children

    def centroid(self):
        return (sum(c.x for c in self.cells.values()) / len(self.cells),
                sum(c.y for c in self.cells.values()) / len(self.cells))
