"""Neurônio LIF simplificado, não um modelo neural humano completo."""
from dataclasses import dataclass

@dataclass
class LIFNeuron:
    potential: float = -70.0
    resting: float = -70.0
    threshold: float = -55.0
    tau_ms: float = 20.0
    refractory_steps: int = 0

    def step(self, current: float, dt_ms: float = 1.0) -> bool:
        if dt_ms <= 0 or self.tau_ms <= 0 or dt_ms > self.tau_ms:
            raise ValueError("Require 0 < dt_ms <= tau_ms")
        if self.refractory_steps > 0:
            self.refractory_steps -= 1
            return False
        self.potential += dt_ms / self.tau_ms * (self.resting - self.potential + current)
        if self.potential >= self.threshold:
            self.potential = self.resting
            self.refractory_steps = 2
            return True
        return False
