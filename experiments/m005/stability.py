"""Step refinement and invariant diagnostics for idealized 2D cell mechanics."""
from math import hypot, isfinite
from cell_mechanics import Disc, step

def simulate(initial, total_time, dt):
    if not isfinite(total_time) or total_time < 0 or not isfinite(dt) or dt <= 0 or dt > .1:
        raise ValueError('invalid time parameters')
    n = round(total_time / dt)
    if abs(n * dt - total_time) > 1e-10 * max(1, total_time):
        raise ValueError('time must be divisible by dt')
    cells = list(initial)
    for _ in range(n):
        cells = step(cells, dt=dt)
    return cells

def centroid(cells):
    if not cells:
        raise ValueError('empty population')
    return (sum(c.x for c in cells) / len(cells), sum(c.y for c in cells) / len(cells))

def max_position_error(a, b):
    if len(a) != len(b):
        raise ValueError('mismatched populations')
    return max((hypot(x.x-y.x, x.y-y.y) for x, y in zip(a, b)), default=0.)

def refinement(initial, total_time=.5, steps=(.1,.05,.025,.0125)):
    if len(steps) < 3 or any(not isfinite(s) or s <= 0 for s in steps):
        raise ValueError('invalid refinement steps')
    results = [simulate(initial, total_time, dt) for dt in steps]
    return [max_position_error(results[i], results[i+1]) for i in range(len(results)-1)]
