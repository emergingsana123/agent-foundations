import argparse
from collections import Counter
from typing import List

from .parser import LogEntry, percentile, read_log_file


def calculate_error_rate(entries: List[LogEntry]) -> float:
    """Return percentage of requests with HTTP status >= 400."""
    if not entries:
        return 0.0

    errors = sum(entry.status >= 400 for entry in entries)
    return errors / len(entries) * 100


def print_report(entries: List[LogEntry], top_n: int = 10) -> None:
    """Print the log analysis report."""
    if not entries:
        print("No valid log entries found.")
        return

    endpoint_counts = Counter(entry.endpoint for entry in entries)
    latencies = [entry.latency_ms for entry in entries]

    print(f"Total requests: {len(entries)}")

    print("\nTop endpoints:")
    for endpoint, count in endpoint_counts.most_common(top_n):
        print(f"{endpoint}: {count}")

    error_rate = calculate_error_rate(entries)

    print(f"\nError rate: {error_rate:.2f}%")

    print("\nLatency:")
    print(f"p50: {percentile(latencies, 50):.2f} ms")
    print(f"p95: {percentile(latencies, 95):.2f} ms")
    print(f"p99: {percentile(latencies, 99):.2f} ms")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze web server/application logs."
    )

    parser.add_argument(
        "log_file",
        help="Path to the log file",
    )

    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of top endpoints to display (default: 10)",
    )

    args = parser.parse_args()

    entries = read_log_file(args.log_file)

    print_report(entries, args.top)


if __name__ == "__main__":
    main()