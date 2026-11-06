"""Reproducible LIF current-response experiment. No biological validation claimed."""
import csv
from dataclasses import dataclass

@dataclass
class LIF:
    voltage: float = -70.0
    rest: float = -70.0
    threshold: float = -55.0
    tau_ms: float = 20.0
    refractory: int = 0

    def step(self, current: float, dt_ms: float = 1.0) -> bool:
        if not (0 < dt_ms <= self.tau_ms):
            raise ValueError("invalid dt")
        if self.refractory:
            self.refractory -= 1
            return False
        self.voltage += dt_ms / self.tau_ms * (self.rest - self.voltage + current)
        if self.voltage >= self.threshold:
            self.voltage = self.rest
            self.refractory = 2
            return True
        return False

def run(current: float, duration_ms: int = 1000) -> dict:
    neuron = LIF()
    spikes = sum(neuron.step(current) for _ in range(duration_ms))
    return {"current_arbitrary_units": current, "duration_ms": duration_ms,
            "spikes": spikes, "rate_hz": spikes * 1000 / duration_ms}

def sweep():
    return [run(i) for i in (0, 5, 10, 14, 15, 16, 20, 30, 40)]

if __name__ == "__main__":
    results = sweep()
    with open("results_lif.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)
    for row in results:
        print(row)
