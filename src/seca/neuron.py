"""Simplified LIF neuron with explicit millisecond refractory time."""
from dataclasses import dataclass
from math import isfinite


@dataclass
class LIFNeuron:
    potential: float = -70.0
    resting: float = -70.0
    threshold: float = -55.0
    tau_ms: float = 20.0
    refractory_ms: float = 2.0
    refractory_remaining_ms: float = 0.0

    def __post_init__(self):
        self._validate_state()

    def _validate_state(self):
        values = (self.potential, self.resting, self.threshold, self.tau_ms,
                  self.refractory_ms, self.refractory_remaining_ms)
        if not all(isfinite(value) for value in values):
            raise ValueError("neuron state and parameters must be finite")
        if self.tau_ms <= 0 or self.refractory_ms < 0 or self.refractory_remaining_ms < 0:
            raise ValueError("invalid time constant or refractory duration")

    def step(self, current: float, dt_ms: float = 1.0) -> bool:
        """Advance Euler over the active part of a possibly refractory step.

        Spikes are detected at the step boundary. Invalid inputs and
        nonfinite integration results leave the state unchanged.
        """
        self._validate_state()
        if not isfinite(current) or not isfinite(dt_ms) or not 0 < dt_ms <= self.tau_ms:
            raise ValueError("require finite current and 0 < dt_ms <= tau_ms")
        remaining = max(0.0, self.refractory_remaining_ms - dt_ms)
        active_dt = max(0.0, dt_ms - self.refractory_remaining_ms)
        if active_dt == 0:
            self.refractory_remaining_ms = remaining
            return False
        candidate = self.potential + active_dt / self.tau_ms * (
            self.resting - self.potential + current
        )
        if not isfinite(candidate):
            raise OverflowError("nonfinite integration result")
        fired = candidate >= self.threshold
        self.potential = self.resting if fired else candidate
        self.refractory_remaining_ms = self.refractory_ms if fired else remaining
        return fired
