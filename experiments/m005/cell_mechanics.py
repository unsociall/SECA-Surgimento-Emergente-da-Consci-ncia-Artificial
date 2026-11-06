"""Idealized 2D pairwise soft-disc mechanics; not calibrated to embryos."""
from dataclasses import dataclass
from math import hypot, isfinite

@dataclass(frozen=True)
class Disc:
    x: float
    y: float
    radius: float = 0.5

def step(cells: list[Disc], dt: float = 0.05, adhesion: float = 0.2,
         repulsion: float = 2.0, contact_range: float = 0.25) -> list[Disc]:
    if not all(isfinite(v) and v >= 0 for v in (dt, adhesion, repulsion, contact_range)):
        raise ValueError('parameters must be finite and nonnegative')
    if dt > 0.1:
        raise ValueError('dt too large for reference configuration')
    if any(not (isfinite(c.x) and isfinite(c.y) and isfinite(c.radius) and c.radius > 0) for c in cells):
        raise ValueError('invalid cell geometry')
    fx, fy = [0.0] * len(cells), [0.0] * len(cells)
    for i, a in enumerate(cells):
        for j in range(i + 1, len(cells)):
            b = cells[j]
            dx, dy = b.x - a.x, b.y - a.y
            d = hypot(dx, dy)
            ux, uy = (1.0, 0.0) if d == 0 else (dx / d, dy / d)
            rest = a.radius + b.radius
            if d < rest:
                magnitude = -repulsion * (rest - d)
            elif d < rest + contact_range:
                magnitude = adhesion * (d - rest) * (rest + contact_range - d) / max(contact_range, 1e-12)
            else:
                magnitude = 0.0
            fx[i] += magnitude * ux; fy[i] += magnitude * uy
            fx[j] -= magnitude * ux; fy[j] -= magnitude * uy
    return [Disc(c.x + dt * fx[i], c.y + dt * fy[i], c.radius) for i, c in enumerate(cells)]
