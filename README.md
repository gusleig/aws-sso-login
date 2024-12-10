# Amazon AWS credentials refresher

This script will help you to refresh your AWS credentials when using AWS SSO.

## How to use

To use this:

Save the Python script as `aws_sso_login.py`
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
4. Automatically source them into your current shell

The credentials will be available as environment variables right away, and you won't need to copy/paste anything.
