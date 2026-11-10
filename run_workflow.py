import subprocess
import sys
steps = [
    (
        "Unit tests",
        [
            sys.executable,
            "-m",
            "unittest",
            "-v",
            "test_release_checks"
        ]
    ),
    (
        "Configuration",
        ["docker", "compose", "config", "--quiet"]
    ),
    (
        "Build",
        ["docker", "compose", "build"]
    ),
    (
        "Local deployment",
        ["docker", "compose", "up", "-d", "--no-build"]
    )
]

for label, command in steps:
    print(f"Starting: {label}", flush=True)
    result = subprocess.run(command)

    if result.returncode != 0:
        print(f"Starting: {label} failed.", flush=True)
        raise SystemExit(result.returncode)

print("Commands completed. Check the container, page, and logs.")