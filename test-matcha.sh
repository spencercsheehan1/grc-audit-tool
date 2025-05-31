#!/bin/bash

# Test script for matcha-sip.py
# Usage: ./test-matcha.sh

echo "Running matcha-sip.py with test inputs..."

# Feed all inputs to the script
python3 matcha-sip.py << EOF
spencercsheehan1
learn-cantonese-app,awesome-security-GRC,grc-audit-tool
2020-01-01
2025-06-01
/Users/spencersheehan/repos/local_env_spencer
EOF

echo "Test completed!" 