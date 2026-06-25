import json
from pathlib import Path


data = json.loads(Path("slither-output.json").read_text())

detectors = data["results"]["detectors"]

first = detectors[0]

print("Top-level keys in first detector:")
print(first.keys())

print("\nFirst detector raw content:")
print(json.dumps(first, indent=2)[:5000])