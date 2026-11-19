from concurrent.futures import ThreadPoolExecutor
from time import perf_counter

import requests

URL = "http://127.0.0.1:5000/deployment-check"
EXPECTED_TEXT = "Deployment Check"
TOTAL_REQUESTS = 10

def request_once(_):
    started = perf_counter()

    try:
        with requests.get(
            URL,
            timeout=5,
            allow_redirects=False
        ) as response:
            ok = (
                response.status_code == 200 and EXPECTED_TEXT in response.text
            )
    except requests.RequestException:
        ok = False

    return ok, (perf_counter() - started)* 1000

def run_batch(workers):
    started = perf_counter()

    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(
            pool.map(request_once, range(TOTAL_REQUESTS))
        )

    batch_seconds = perf_counter() - started
    successful = sum(ok for ok, _ in results)
    mean_ms = sum(ms for _, ms in results) / len(results)

    print(f"\nClient workers: {workers}")
    print(f"Successful: {successful}/{TOTAL_REQUESTS}")
    print(f"Failed: {TOTAL_REQUESTS - successful}")
    print(f"Mean attempt time (ms): {mean_ms:.1f}")
    print(f"Batch time (s): {batch_seconds:.3f}")

if __name__ == "__main__":
    print("Target:", URL)

    for workers in (1, 5):
        run_batch(workers)