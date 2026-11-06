"""Deterministic regularization for coincident point cells (toy model)."""
import math

def pair_forces(positions, radius=0.5, stiffness=1.0):
    if not (math.isfinite(radius) and radius > 0 and math.isfinite(stiffness) and stiffness >= 0):
        raise ValueError('invalid parameters')
    if any(len(p) != 2 or not all(math.isfinite(v) for v in p) for p in positions):
        raise ValueError('invalid positions')
    forces = [[0.0, 0.0] for _ in positions]
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            dx = positions[j][0] - positions[i][0]
            dy = positions[j][1] - positions[i][1]
            d = math.hypot(dx, dy)
            if d >= 2 * radius:
                continue
            if d == 0:
                # Index-defined direction: reproducible but not permutation invariant.
                ux, uy = 1.0, 0.0
            else:
                ux, uy = dx / d, dy / d
            f = stiffness * (2 * radius - d)
            forces[i][0] -= f * ux
            forces[i][1] -= f * uy
            forces[j][0] += f * ux
            forces[j][1] += f * uy
    return [tuple(p) for p in forces]

def step(positions, dt, radius=0.5, stiffness=1.0):
    if not (math.isfinite(dt) and dt > 0):
        raise ValueError('invalid timestep')
    forces = pair_forces(positions, radius, stiffness)
    return [(p[0] + dt*f[0], p[1] + dt*f[1]) for p,f in zip(positions, forces)]
