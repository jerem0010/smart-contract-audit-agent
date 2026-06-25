import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 src/main.py <solidity-project-path>")
        sys.exit(1)

    target_path = Path(sys.argv[1])

    if not target_path.exists():
        print(f"Error: target path not found: {target_path}")
        sys.exit(1)

    print("Project-level audit agent scaffold")
    print(f"Target: {target_path}")
    print("Implementation pending.")


if __name__ == "__main__":
    main()
