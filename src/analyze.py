import json
from pathlib import Path


slither_path = Path("slither-output.json")

if not slither_path.exists():
    print("Error: slither-output.json not found")
    exit(1)

data = json.loads(slither_path.read_text())

detectors = data["results"]["detectors"]

print("Mini Slither Report")
print("===================")
print()

for i, detector in enumerate(detectors, start=1):
    check = detector.get("check")
    impact = detector.get("impact")
    confidence = detector.get("confidence")
    description = detector.get("description")

    print(f"Finding #{i}")
    print(f"Check: {check}")
    print(f"Impact: {impact}")
    print(f"Confidence: {confidence}")
    print()
    print(description)
    print("-" * 80)