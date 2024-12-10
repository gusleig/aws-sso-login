import subprocess
import json
import os
from pathlib import Path
from dotenv import load_dotenv


def load_configuration():
    """Load configuration from .env file"""
    # Get the directory where the script is located
    script_dir = Path(__file__).parent.absolute()
    env_path = script_dir / '.env'

    if not env_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {env_path}")

    # Load .env file
    load_dotenv(env_path)

    # Get required configuration
    config = {
        'profile': os.getenv('AWS_PROFILE'),
        'env_file': os.path.expandvars(os.path.expanduser(os.getenv('AWS_ENV_FILE', '~/aws-env')))
    }

    # Validate configuration
    if not config['profile']:
        raise ValueError("AWS_PROFILE not set in .env file")

    return config


def run_aws_sso_login(profile):
    """Run AWS SSO login command and return True if successful"""
    try:
        subprocess.run(['aws', 'sso', 'login', '--profile', profile], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error logging in: {e}")
        return False


def get_credentials(profile):
    """Get credentials using the configured profile"""
    try:
        result = subprocess.run(
            ['aws', 'configure', 'export-credentials', '--profile', profile],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error getting credentials: {e}")
        return None


def save_to_env_file(credentials, env_file_path):
    """Save credentials to a file that can be sourced by shell"""
    if not credentials:
        return False

    # Create directory if it doesn't exist
    env_file = Path(env_file_path)
    env_file.parent.mkdir(parents=True, exist_ok=True)

    with open(env_file, 'w') as f:
        f.write(f"export AWS_ACCESS_KEY_ID={credentials['AccessKeyId']}\n")
        f.write(f"export AWS_SECRET_ACCESS_KEY={credentials['SecretAccessKey']}\n")
        f.write(f"export AWS_SESSION_TOKEN={credentials['SessionToken']}\n")
        f.write(f"export AWS_REGION=us-east-1\n")  # You might want to make this configurable in .env too

    # Make sure the file has appropriate permissions
    env_file.chmod(0o600)

    print(f"\nCredentials saved to {env_file}")
    return True


def main():
    try:
        config = load_configuration()
        if run_aws_sso_login(config['profile']):
            credentials = get_credentials(config['profile'])
            save_to_env_file(credentials, config['env_file'])
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0


if __name__ == "__main__":
    exit(main())