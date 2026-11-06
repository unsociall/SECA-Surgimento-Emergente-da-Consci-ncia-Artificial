"""Temporal refinement check for the archived idealized cell mechanics model."""
from cell_mechanics import Disc, step
from math import hypot

INITIAL = [Disc(0.0, 0.0), Disc(0.7, 0.0), Disc(2.0, 0.3)]

def evolve(dt: float, duration: float = 1.0):
    n = round(duration / dt)
    if abs(n * dt - duration) > 1e-10:
        raise ValueError('duration must be divisible by timestep')
    cells = INITIAL
    for _ in range(n):
        cells = step(cells, dt=dt)
    return cells

def distance(a, b):
    return max(hypot(x.x-y.x, x.y-y.y) for x, y in zip(a,b))

if __name__ == '__main__':
    reference = evolve(0.001)
    for dt in (0.1, 0.05, 0.025, 0.0125):
        print(f'dt={dt:.4f} max_position_error={distance(evolve(dt),reference):.9f}')
