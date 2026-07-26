# Security Policy

## Protect secrets

This Skill works with SSH, HTTP proxies, and Codex authentication. Never commit or paste into issues:

- `~/.codex/auth.json`
- API keys, access tokens, passwords, or private keys
- Real server addresses and ports when they identify private infrastructure
- One-time device-login codes

Use placeholders in public examples and redact logs before sharing them.

## Reporting a vulnerability

Please use GitHub's private vulnerability reporting for this repository when available. If it is unavailable, open a minimal issue without including secrets or exploit details, and request a private contact channel from the maintainers.
