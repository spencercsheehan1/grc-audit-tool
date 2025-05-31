import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the token
token = os.getenv("GITHUB_TOKEN")

print("=== GitHub Token Debug ===")
print(f"Token loaded: {'Yes' if token else 'No'}")
if token:
    print(f"Token length: {len(token)}")
    print(f"Token starts with: {token[:7]}...")
    print(f"Token ends with: ...{token[-4:]}")
else:
    print("Token is None or empty!")
    print("\nChecking .env file:")
    if os.path.exists('.env'):
        print(".env file exists")
        with open('.env', 'r') as f:
            content = f.read()
            if 'GITHUB_TOKEN' in content:
                print("GITHUB_TOKEN found in .env file")
            else:
                print("GITHUB_TOKEN NOT found in .env file")
    else:
        print(".env file NOT found in current directory")

print(f"\nCurrent directory: {os.getcwd()}")
print("\nEnvironment variables containing 'GITHUB':")
for key, value in os.environ.items():
    if 'GITHUB' in key:
        print(f"{key}={value[:10]}...") if len(value) > 10 else print(f"{key}={value}") 