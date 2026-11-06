"""Run SECA suites in separate processes, including standalone experiments."""
import os
from pathlib import Path
import subprocess
import sys


def main():
    root = Path(__file__).resolve().parents[1]
    suites = {root / "tests"}
    suites.update(path.parent for path in (root / "experiments").rglob("test*.py"))
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(filter(None, (str(root / "src"), env.get("PYTHONPATH"))))
    failed = []
    for suite in sorted(suites):
        label = str(suite.relative_to(root))
        print(f"\nRunning suite: {label}", flush=True)
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", ".", "-p", "test*.py", "-v"],
            cwd=suite, env=env, check=False,
        )
        if result.returncode:
            failed.append(label)
    if failed:
        print("Failed suites: " + ", ".join(failed), file=sys.stderr)
        return 1
    print(f"\nAll {len(suites)} suites passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
