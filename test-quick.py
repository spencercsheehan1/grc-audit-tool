#!/usr/bin/env python3
"""
Quick test script for matcha-sip.py
Modify the TEST_INPUTS dictionary to change test values
"""

import subprocess

# Modify these values for your test
TEST_INPUTS = {
    "owner": "spencercsheehan1",
    "repos": "learn-cantonese-app,awesome-security-GRC,grc-audit-tool",
    "start_date": "2020-01-01",
    "end_date": "2025-06-01",
    "output_dir": "/Users/spencersheehan/repos/local_env_spencer"
}

# Build the input string
input_string = "\n".join([
    TEST_INPUTS["owner"],
    TEST_INPUTS["repos"],
    TEST_INPUTS["start_date"],
    TEST_INPUTS["end_date"],
    TEST_INPUTS["output_dir"]
])

print("Running matcha-sip.py with test inputs:")
print("-" * 50)
for key, value in TEST_INPUTS.items():
    print(f"{key}: {value}")
print("-" * 50)

# Run the script with piped input
process = subprocess.run(
    ["python3", "matcha-sip.py"],
    input=input_string,
    text=True,
    capture_output=False
)

print("\nTest completed with exit code:", process.returncode) 