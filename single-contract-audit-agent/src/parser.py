try:
    from src.models import Finding, Location
except ModuleNotFoundError:
    from models import Finding, Location


def get_detector_results(slither_data: dict) -> list[dict]:
    return slither_data.get("results", {}).get("detectors", [])


def extract_location(detector: dict) -> dict:
    elements = detector.get("elements", [])

    function_location = find_location_for_element_type(elements, "function")
    if function_location:
        return function_location

    for element in elements:
        location = extract_location_from_element(element)
        if location:
            return location

    return empty_location()


def find_location_for_element_type(elements: list[dict], element_type: str) -> dict | None:
    for element in elements:
        if element.get("type") == element_type:
            return extract_location_from_element(element)

    return None


def extract_location_from_element(element: dict) -> dict | None:
    source_mapping = element.get("source_mapping", {})
    lines = source_mapping.get("lines", [])
    filename = source_mapping.get("filename_relative")

    if not filename or not lines:
        return None

    type_specific_fields = element.get("type_specific_fields", {})
    parent = type_specific_fields.get("parent", {})
    element_type = element.get("type")

    contract_parent = find_parent_by_type(parent, "contract")
    function_parent = find_parent_by_type(parent, "function")

    contract_name = contract_parent.get("name") if contract_parent else None
    if element_type == "contract":
        contract_name = element.get("name")

    function_name = None
    if element_type in {"function", "modifier"}:
        function_name = type_specific_fields.get("signature") or element.get("name")
    elif function_parent:
        function_name = function_parent.get("type_specific_fields", {}).get("signature")
        function_name = function_name or function_parent.get("name")

    return {
        "contract": contract_name,
        "function": function_name,
        "filename": filename,
        "start_line": min(lines),
        "end_line": max(lines),
    }


def find_parent_by_type(parent: dict, parent_type: str) -> dict | None:
    current = parent

    while current:
        if current.get("type") == parent_type:
            return current

        current = current.get("type_specific_fields", {}).get("parent", {})

    return None


def empty_location() -> dict:
    return {
        "contract": None,
        "function": None,
        "filename": None,
        "start_line": None,
        "end_line": None,
    }


def extract_findings(slither_data: dict) -> list[Finding]:
    detectors = get_detector_results(slither_data)

    findings = []

    for i, detector in enumerate(detectors, start=1):
        location = extract_location(detector)
        description = detector.get("description") or ""
        check = detector.get("check")
        severity = detector.get("impact")

        finding = Finding(
            id=f"S-{i:03d}",
            tool="slither",
            check=detector.get("check"),
            title=build_title(check, description),
            severity=severity,
            confidence=detector.get("confidence"),
            contract=location["contract"],
            function=location["function"],
            location=Location(
                file=location["filename"],
                start_line=location["start_line"],
                end_line=location["end_line"],
            ),
            description=description,
            recommendation=build_recommendation(check),
        )

        findings.append(finding)

    return findings


def build_title(check: str | None, description: str) -> str:
    if description:
        first_line = description.strip().splitlines()[0]
        return first_line.removesuffix(":").strip()

    return check or "Untitled finding"


def build_recommendation(check: str | None) -> str:
    recommendations = {
        "reentrancy-eth": "Apply checks-effects-interactions, update state before external calls, and consider using a reentrancy guard.",
        "reentrancy-no-eth": "Apply checks-effects-interactions, update state before token transfers, and consider using a reentrancy guard.",
        "unchecked-transfer": "Check the return value of token transfers or use a safe transfer helper such as OpenZeppelin SafeERC20.",
        "low-level-calls": "Prefer typed interfaces where possible and keep low-level calls isolated, checked, and documented.",
        "missing-zero-check": "Validate address parameters against address(0) before storing or using them.",
        "solc-version": "Pin the Solidity compiler to a reviewed patch version and verify known compiler bugs for that version.",
        "events-maths": "Emit an event when updating security-sensitive configuration or accounting state.",
    }

    return recommendations.get(
        check,
        "Review the finding manually, confirm whether it is exploitable in context, and document the chosen fix.",
    )


def sort_findings_by_impact(findings: list[Finding]) -> list[Finding]:
    impact_order = {
        "Critical": 0,
        "High": 0,
        "Medium": 1,
        "Low": 2,
        "Informational": 3,
        "Optimization": 4,
    }

    return sorted(
        findings,
        key=lambda finding: impact_order.get(finding.severity, 999),
    )
