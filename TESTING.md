# Quick Testing Guide for matcha-sip

Here are several ways to quickly test matcha-sip.py without manually entering inputs each time.

## Method 1: Bash Script (Recommended)
```bash
./test-matcha.sh
```
Edit `test-matcha.sh` to change the test inputs.

## Method 2: Python Test Script
```bash
python3 test-quick.py
```
Edit the `TEST_INPUTS` dictionary in `test-quick.py` to change values.

## Method 3: One-liner with Echo
```bash
echo -e "spencercsheehan1\nlearn-cantonese-app,awesome-security-GRC,grc-audit-tool\n2020-01-01\n2025-06-01\n~/repos/local_env_spencer" | python3 matcha-sip.py
```

## Method 4: Here Document (Direct in Terminal)
```bash
python3 matcha-sip.py << EOF
spencercsheehan1
learn-cantonese-app
2020-01-01
2025-06-01
~/repos/local_env_spencer
EOF
```

## Method 5: Input from File
Create a file `inputs.txt`:
```
spencercsheehan1
learn-cantonese-app,awesome-security-GRC
2020-01-01
2025-06-01
~/repos/local_env_spencer
```

Then run:
```bash
python3 matcha-sip.py < inputs.txt
```

## Method 6: Alias for Quick Testing
Add to your `~/.zshrc` or `~/.bashrc`:
```bash
alias test-matcha='echo -e "spencercsheehan1\nlearn-cantonese-app\n2020-01-01\n2025-06-01\n~/repos/local_env_spencer" | python3 matcha-sip.py'
```

Then just run:
```bash
test-matcha
```

## Tips:
- For testing a single repo quickly, use Method 3 or 4
- For testing multiple scenarios, use Method 1 or 2
- For repeated testing with same inputs, use Method 6 (alias) 