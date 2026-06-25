from dataclasses import asdict, dataclass


@dataclass
class Location:
    file: str | None
    start_line: int | None
    end_line: int | None

    def format(self) -> str:
        if self.file is None or self.start_line is None or self.end_line is None:
            return "N/A"

        return f"{self.file}#{self.start_line}-{self.end_line}"


@dataclass
class Triage:
    verdict: str
    reason: str
    is_duplicate: bool = False
    duplicate_of: str | None = None


@dataclass
class Finding:
    id: str
    tool: str
    check: str | None
    title: str
    severity: str | None
    confidence: str | None
    contract: str | None
    function: str | None
    location: Location
    description: str
    recommendation: str
    status: str = "Open"
    triage: Triage | None = None

    @property
    def impact(self) -> str | None:
        return self.severity

    def to_dict(self) -> dict:
        output = asdict(self)
        output["impact"] = self.impact
        output["filename"] = self.location.file
        output["start_line"] = self.location.start_line
        output["end_line"] = self.location.end_line
        return output
