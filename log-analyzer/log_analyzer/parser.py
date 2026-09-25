from dataclasses import dataclass
from typing import List


@dataclass
class LogEntry:
    method: str
    endpoint: str
    status: int
    latency_ms: float


def parse_line(line: str) -> LogEntry:
    """
    Parse a log line in the format:

    2026-09-25T10:00:00 GET /api/users 200 42.5
    """
    parts = line.strip().split()

    if len(parts) != 5:
        raise ValueError(f"Invalid log line: {line}")

    _, method, endpoint, status, latency = parts

    return LogEntry(
        method=method,
        endpoint=endpoint,
        status=int(status),
        latency_ms=float(latency),
    )


def read_log_file(path: str) -> List[LogEntry]:
    """Read and parse all valid log entries from a file."""
    entries: List[LogEntry] = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            try:
                entries.append(parse_line(line))
            except ValueError:
                continue

    return entries


def percentile(values: List[float], p: float) -> float:
    """Calculate a percentile using linear interpolation."""
    if not values:
        raise ValueError("Cannot calculate percentile of empty list.")

    if not 0 <= p <= 100:
        raise ValueError("Percentile must be between 0 and 100.")

    sorted_values = sorted(values)

    position = (len(sorted_values) - 1) * (p / 100)
    lower = int(position)
    upper = min(lower + 1, len(sorted_values) - 1)

    fraction = position - lower

    return (
        sorted_values[lower]
        + (sorted_values[upper] - sorted_values[lower]) * fraction
    )