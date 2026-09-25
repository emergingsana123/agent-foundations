import random
from datetime import datetime, timedelta
from pathlib import Path


ENDPOINTS = [
    "/",
    "/api/users",
    "/api/products",
    "/api/orders",
    "/api/login",
    "/api/search",
    "/api/cart",
    "/api/health",
    "/api/profile",
    "/api/recommendations",
]

STATUS_CODES = [200, 200, 200, 200, 201, 400, 404, 500]


def generate_log_line(timestamp: datetime) -> str:
    method = random.choice(["GET", "GET", "GET", "POST"])
    endpoint = random.choice(ENDPOINTS)
    status = random.choice(STATUS_CODES)

    latency = random.lognormvariate(3.5, 0.5)

    return (
        f"{timestamp.isoformat()} "
        f"{method} "
        f"{endpoint} "
        f"{status} "
        f"{latency:.2f}\n"
    )


def generate_logs(output: Path, count: int = 100_000) -> None:
    timestamp = datetime(2026, 9, 25, 10, 0, 0)

    with output.open("w", encoding="utf-8") as file:
        for _ in range(count):
            file.write(generate_log_line(timestamp))
            timestamp += timedelta(milliseconds=random.randint(1, 1000))


if __name__ == "__main__":
    output_path = Path("data/app.log")

    random.seed(42)

    generate_logs(output_path)

    print(f"Generated 100,000 logs at {output_path}")