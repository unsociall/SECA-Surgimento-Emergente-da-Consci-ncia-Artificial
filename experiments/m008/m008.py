"""Pairwise soft-core cell mechanics; toy 2-D model, not biological validation."""
from math import hypot, isfinite

def forces(points, radii, stiffness=1.0, attraction=0.1, attraction_range=0.4):
    if not all(isfinite(x) and isfinite(y) for x,y in points):
        raise ValueError('nonfinite position')
    if len(points)!=len(radii) or any(not isfinite(r) or r<=0 for r in radii):
        raise ValueError('invalid radii')
    if any(not isfinite(v) or v<0 for v in (stiffness,attraction,attraction_range)):
        raise ValueError('invalid parameter')
    out=[[0.,0.] for _ in points]
    unresolved=0
    for i in range(len(points)):
        for j in range(i+1,len(points)):
            dx=points[j][0]-points[i][0]; dy=points[j][1]-points[i][1]
            dist=hypot(dx,dy)
            target=radii[i]+radii[j]
            if dist==0:
                unresolved+=1
                continue  # cannot choose a nonzero direction equivariantly from coincident positions alone
            if dist<target:
                magnitude=-stiffness*(target-dist)
            elif dist<target+attraction_range:
                magnitude=attraction*(dist-target)*(target+attraction_range-dist)/max(attraction_range,1e-12)
            else:
                continue
            fx=magnitude*dx/dist;fy=magnitude*dy/dist
            out[i][0]+=fx;out[i][1]+=fy
            out[j][0]-=fx;out[j][1]-=fy
    return out,unresolved

def step(points,radii,dt=0.01,**kwargs):
    if not isfinite(dt) or dt<=0: raise ValueError('invalid timestep')
    f,n=forces(points,radii,**kwargs)
    return [(x+dt*fx,y+dt*fy) for (x,y),(fx,fy) in zip(points,f)],n
