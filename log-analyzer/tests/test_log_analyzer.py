from pathlib import Path

import pytest

from log_analyzer.cli import calculate_error_rate
from log_analyzer.parser import LogEntry, parse_line, percentile, read_log_file


def test_parse_line():
    line = "2026-09-25T10:00:00 GET /api/users 200 42.5"

    entry = parse_line(line)

    assert entry.method == "GET"
    assert entry.endpoint == "/api/users"
    assert entry.status == 200
    assert entry.latency_ms == 42.5


def test_parse_invalid_line():
    with pytest.raises(ValueError):
        parse_line("invalid log line")


def test_percentile():
    values = [10, 20, 30, 40, 50]

    assert percentile(values, 50) == 30
    assert percentile(values, 100) == 50
    assert percentile(values, 0) == 10


def test_error_rate():
    entries = [
        LogEntry("GET", "/", 200, 10),
        LogEntry("GET", "/", 200, 20),
        LogEntry("GET", "/", 500, 30),
        LogEntry("GET", "/", 404, 40),
    ]

    assert calculate_error_rate(entries) == 50.0


def test_read_log_file(tmp_path: Path):
    log_file = tmp_path / "test.log"

    log_file.write_text(
        "2026-09-25T10:00:00 GET /api/users 200 10\n"
        "2026-09-25T10:00:01 GET /api/orders 500 20\n"
    )

    entries = read_log_file(str(log_file))

    assert len(entries) == 2
    assert entries[0].endpoint == "/api/users"
    assert entries[1].status == 500


def test_empty_percentile():
    with pytest.raises(ValueError):
        percentile([], 50)