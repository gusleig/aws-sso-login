import subprocess
import json
import os
from pathlib import Path


def run_aws_sso_login():
    """Run AWS SSO login command and return True if successful"""
    try:
        subprocess.run(['aws', 'sso', 'login', '--profile', 'pepsi'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error logging in: {e}")
        return False


def get_credentials():
    """Get credentials using the configured profile"""
    try:
        result = subprocess.run(
            ['aws', 'configure', 'export-credentials', '--profile', 'pepsi'],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error getting credentials: {e}")
        return None


def save_to_env_file():
    """Save credentials to a file that can be sourced by shell"""
    credentials = get_credentials()
    if not credentials:
        return False

    env_file = Path.home() / '.aws-env'
    with open(env_file, 'w') as f:
        f.write(f"export AWS_ACCESS_KEY_ID={credentials['AccessKeyId']}\n")
        f.write(f"export AWS_SECRET_ACCESS_KEY={credentials['SecretAccessKey']}\n")
        f.write(f"export AWS_SESSION_TOKEN={credentials['SessionToken']}\n")
        f.write(f"export AWS_REGION=us-east-1\n")  # Based on your config

    print(f"\nCredentials saved to {env_file}")
    print("\nTo use these credentials, run:")
    print(f"source {env_file}")
    return True


def main():
    if run_aws_sso_login():
        save_to_env_file()


if __name__ == "__main__":
    main()