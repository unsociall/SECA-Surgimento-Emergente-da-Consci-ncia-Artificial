"""Offline pairwise overdamped mechanics; not a biological model."""
from math import hypot, isfinite

def step(points, dt=.01, radius=.5, repulsion=1., attraction=.1, reach=1.5):
    if not (0 < dt <= 1 and radius > 0 and repulsion >= 0 and attraction >= 0 and reach >= 2*radius):
        raise ValueError("invalid parameters")
    if any(len(p)!=2 or not all(isfinite(v) for v in p) for p in points):
        raise ValueError("nonfinite or malformed coordinates")
    forces=[[0.,0.] for _ in points]
    for i in range(len(points)):
        for j in range(i+1,len(points)):
            dx=points[j][0]-points[i][0];dy=points[j][1]-points[i][1]
            d=hypot(dx,dy)
            ux,uy=(dx/d,dy/d) if d else (1.,0.)
            if d<2*radius: f=-repulsion*(2*radius-d)
            elif d<reach: f=attraction*(d-2*radius)
            else: continue
            fx,fy=f*ux,f*uy
            forces[i][0]+=fx;forces[i][1]+=fy
            forces[j][0]-=fx;forces[j][1]-=fy
    return [(p[0]+dt*f[0],p[1]+dt*f[1]) for p,f in zip(points,forces)]

def simulate(points, steps, **kwargs):
    if not isinstance(steps,int) or steps<0: raise ValueError("invalid steps")
    points=[tuple(p) for p in points]
    for _ in range(steps): points=step(points,**kwargs)
    return points

def centroid(points):
    if not points: raise ValueError("empty")
    return (sum(x for x,y in points)/len(points),sum(y for x,y in points)/len(points))
