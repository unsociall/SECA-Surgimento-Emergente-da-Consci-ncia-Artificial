"""Idealized 2D symmetric pair-force cell model. Not biologically calibrated."""
from dataclasses import dataclass
from math import hypot, isfinite

@dataclass(frozen=True)
class Cell2D:
    x: float
    y: float
    radius: float = 0.5

def step(cells: list[Cell2D], dt: float = 0.05, repulsion: float = 1.0,
         attraction: float = 0.1, reach: float = 0.5) -> list[Cell2D]:
    if not all(isfinite(v) for v in (dt, repulsion, attraction, reach)):
        raise ValueError("nonfinite parameter")
    if dt <= 0 or repulsion < 0 or attraction < 0 or reach < 0:
        raise ValueError("invalid parameters")
    if any(c.radius <= 0 or not all(isfinite(v) for v in (c.x, c.y, c.radius)) for c in cells):
        raise ValueError("invalid cell")
    fx = [0.0] * len(cells)
    fy = [0.0] * len(cells)
    for i in range(len(cells)):
        for j in range(i + 1, len(cells)):
            dx, dy = cells[j].x - cells[i].x, cells[j].y - cells[i].y
            d = hypot(dx, dy)
            ux, uy = (1.0, 0.0) if d == 0 else (dx / d, dy / d)
            contact = cells[i].radius + cells[j].radius
            if d < contact:
                force = -repulsion * (contact - d)
            elif d < contact + reach:
                force = attraction * (d - contact) * (contact + reach - d) / max(reach, 1e-12)
            else:
                force = 0.0
            fx[i] += force * ux
            fy[i] += force * uy
            fx[j] -= force * ux
            fy[j] -= force * uy
    return [Cell2D(c.x + dt * fx[i], c.y + dt * fy[i], c.radius)
            for i, c in enumerate(cells)]

def center(cells: list[Cell2D]) -> tuple[float, float]:
    if not cells:
        raise ValueError("empty cells")
    return (sum(c.x for c in cells) / len(cells),
            sum(c.y for c in cells) / len(cells))
