import json
import subprocess
from pathlib import Path


def run_slither(target_path: Path, output_path: Path) -> None:
    command = [
        "slither",
        str(target_path),
        "--json",
        str(output_path),
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    if not output_path.exists():
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError("Slither did not generate the JSON output file.")


def load_slither_results(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"{path} not found")

    return json.loads(path.read_text())
