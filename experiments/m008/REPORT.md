# M008 — Equivariant pairwise forces and explicit coincidence detection
Date: 2026-11-06.

## Goal
Reduce artificial preferred directions in the M007-style coincident-cell regularization without silently claiming a general solution. A rotationally equivariant, deterministic vector force based solely on identical coincident positions cannot select a nonzero direction without extra symmetry-breaking information.

## Method
For noncoincident cells, apply central pairwise forces depending only on distance: linear soft overlap repulsion, bounded short-range attraction, zero beyond the cutoff. Pairwise forces sum to zero. At exactly coincident positions, do not invent an arbitrary direction; report an unresolved pair count and apply zero force to that pair. The simulator therefore does **not** resolve exact overlaps automatically. External perturbations or additional physical state would be required.

## Execution
Local command: `cd experiments/m008 && python -m unittest -v`
Observed: 8 tests passed (Python unittest, 2026-11-06). Initially two tests failed due to a force-sign error and exact float equality; the sign was corrected and numerical comparisons changed to tolerances before the passing run. CI not verified.

## Properties tested
Overlap repulsion, action-reaction, translation and 90-degree rotation covariance, explicit coincidence flag, centroid conservation, invalid parameters and distant pairs.

## Scientific limits
Toy overdamped 2-D mechanics, no calibrated units, no adhesion molecules, no developmental cell fate, no empirical validation. The zero-force coincidence policy is a known limitation, not a biological solution. Rotation covariance checked for a 90-degree rotation only; broader randomized tests remain needed.

## Reference
Maître et al., *Mechanics of human embryo compaction*, Nature (2024): https://www.nature.com/articles/s41586-024-07351-x. This paper motivates the importance of cell mechanics, but does not validate these chosen equations or parameters.

## Next
Test convergence and finite-step stability over random seeds, add collision resolution using explicitly modeled polarity or stochastic perturbations with controlled seeds, and calibrate against published data where accessible.
