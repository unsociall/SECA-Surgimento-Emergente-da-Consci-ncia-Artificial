"""Offline 2D overdamped central-force cell model; no biological calibration."""
from math import hypot, isfinite

def step(positions, dt=0.01, radius=0.5, repulsion=1.0, attraction=0.1, reach=1.5):
    """Return updated positions and number of coincident pairs (no force)."""
    if not all(isfinite(x) and x > 0 for x in (dt, radius, reach)) or not all(isfinite(x) and x >= 0 for x in (repulsion, attraction)) or reach < 2*radius:
        raise ValueError("invalid parameters")
    pts = [tuple(p) for p in positions]
    if any(len(p) != 2 or not all(isfinite(v) for v in p) for p in pts):
        raise ValueError("positions must be finite 2D points")
    forces = [[0., 0.] for _ in pts]
    coincident = 0
    for i in range(len(pts)):
        for j in range(i+1, len(pts)):
            dx, dy = pts[j][0]-pts[i][0], pts[j][1]-pts[i][1]
            d = hypot(dx, dy)
            if d == 0:
                coincident += 1
                continue
            overlap = 2*radius-d
            magnitude = -repulsion*overlap if overlap > 0 else attraction*(d-2*radius) if d < reach else 0.
            fx, fy = magnitude*dx/d, magnitude*dy/d
            forces[i][0] += fx
            forces[i][1] += fy
            forces[j][0] -= fx
            forces[j][1] -= fy
    result = [(x+dt*f[0], y+dt*f[1]) for (x,y),f in zip(pts,forces)]
    if any(not all(isfinite(v) for v in p) for p in result):
        raise OverflowError("nonfinite integration result")
    return result, coincident
