# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Stage driver for sprint 1.2.0 – calls `nox -s vibed` correctly."""

import subprocess
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python 1.2.0.py <semver>")
        sys.exit(1)
    semver = sys.argv[1]
    # Bubble all output so the parent process handles logging/tee
    cmd = ["nox", "-s", "vibed", "--", semver]
    print(f"▶ Running: {' '.join(cmd)}")
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as exc:
        print(f"❌ nox vibed failed with code {exc.returncode}")
        sys.exit(exc.returncode)


if __name__ == "__main__":
    main()
