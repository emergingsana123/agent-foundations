1. Top 10 endpoints

Count how many times each endpoint was requested.

Example:

Top endpoints:

/api/users: 15234
/api/products: 12431
/api/orders: 10293
...

This tells you which APIs are being used most.

2. Error rate

Determine what percentage of requests failed.

For example:

Total requests: 100000
Errors: 12450

Error rate: 12.45%

You need to define an error as an HTTP status code >= 400.

So:

200 → success
201 → success
400 → error
404 → error
500 → error

Formula:

error rate = (number of errors / total requests) × 100

3. Latency percentiles

Take all request latencies and calculate:

p50
p95
p99

For example:

Latency:

p50: 31.42 ms
p95: 82.17 ms
p99: 119.83 ms

This is particularly important because average latency isn't enough.

Imagine:

99 requests → 10 ms
1 request   → 5000 ms

Average:

~60 ms

But that hides the fact that one user waited 5 seconds.

p99 helps expose the slow tail.