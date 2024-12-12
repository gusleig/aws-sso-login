# Amazon AWS credentials refresher

This script will help you to refresh your AWS credentials when using AWS SSO.

## How to use

To use this:

Save the shell script as `aws_sso_login.sh` and make it executable:

```bash
chmod +x aws_sso_login.sh
```

Add an alias to your ~/.bashrc or ~/.zshrc:

```bash
alias aws-login='/path/to/aws_sso_login.sh'
```

Then you can simply type:
```bash
aws-login
```
This will:

1. Run the SSO login process (opening your browser if needed)
2. Get the temporary credentials 
3. Save them to a file ~/.aws-env
4. Create scripts to refresh the credentials and export them as environment variables

## Using the scripts

To set this up:

Add this line to your ~/.bashrc or ~/.zshrc:
```bash
source ~/.aws-functions
```

Reload your shell or run:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

Then you can use it like this:
```bash
# First time setup
./aws_sso_login.sh

# Later, when you need the credentials
aws-load-creds

# Check your current credentials
aws-check-creds

# Clear credentials when done
aws-clear-creds

``` 

The credentials will be available as environment variables right away, and you won't need to copy/paste anything.
