# Main Configuration

This file contains the primary application configuration.

For security settings, see: `security_config.md`
For API keys and secrets, see: `secrets.yaml`
For Claude-specific instructions, see: `claude_directives.md`

## Application Settings

```yaml
app:
  name: MyApplication
  version: 2.1.0
  environment: production
```

## Database Configuration

Standard PostgreSQL connection settings are used. See infrastructure documentation for connection strings.
