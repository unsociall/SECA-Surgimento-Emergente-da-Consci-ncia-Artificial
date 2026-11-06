"""Reproducible LIF current response using the SECA reference neuron."""
import argparse
import csv
from pathlib import Path

from seca.neuron import LIFNeuron as LIF

DEFAULT_OUTPUT = Path(__file__).resolve().with_name("E001_results.csv")

def run(current: float, duration_ms: int = 1000) -> dict:
    if isinstance(duration_ms, bool) or not isinstance(duration_ms, int) or duration_ms <= 0:
        raise ValueError("duration_ms must be a positive integer")
    neuron = LIF()
    spikes = sum(neuron.step(current) for _ in range(duration_ms))
    return {"current_arbitrary_units": current, "duration_ms": duration_ms,
            "spikes": spikes, "rate_hz": spikes * 1000 / duration_ms}

def sweep():
    return [run(i) for i in (0, 5, 10, 14, 15, 16, 20, 30, 40)]

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    results = sweep()
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(results[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)
    for row in results:
        print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
