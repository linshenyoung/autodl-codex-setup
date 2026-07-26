<p align="center">
  <strong>AutoDL Codex Setup</strong>
</p>

<p align="center">
  <a href="README.zh-CN.md">简体中文</a> · <a href="README.md">English</a>
</p>

Configure [OpenAI Codex](https://developers.openai.com/codex/) on an AutoDL or similar remote Ubuntu server through Windows SSH and VS Code Remote-SSH.

## What it covers

- Host-scoped `RemoteForward` for a local HTTP proxy
- Remote Codex proxy configuration in `~/.codex/config.toml`
- VS Code Remote-SSH proxy settings
- Node.js and global Codex CLI installation when missing
- `codex login --device-auth` and safe status verification
- Port-conflict checks and end-to-end proxy validation

## Quick example

Replace the placeholders with your own server values. Do not commit real hostnames, ports, usernames, credentials, or device codes.

```ssh
Host autodl-example
  HostName <your-autodl-host>
  Port <ssh-port>
  User <ssh-user>
  RemoteForward <remote-proxy-port> 127.0.0.1:<local-proxy-port>
```

The server-side Codex proxy endpoint is `http://127.0.0.1:<remote-proxy-port>`; the local proxy remains on `127.0.0.1:<local-proxy-port>`.

## Install the Skill

Clone this repository and copy the Skill directory into your Codex Skills directory:

```powershell
Copy-Item .\autodl-codex-setup "$HOME\.codex\skills\autodl-codex-setup" -Recurse
```

Then ask Codex to configure a host, for example:

```text
Use autodl-codex-setup to configure this AutoDL host:
Host autodl-example
  HostName <your-autodl-host>
  Port <ssh-port>
  User <ssh-user>
```

## Safety notes

- Give each host a unique remote forwarding port.
- Preserve unrelated SSH, TOML, and JSON settings.
- Never commit `auth.json`, tokens, passwords, private keys, or device codes.
- A successful HTTP proxy test does not prove Codex authentication; verify with `codex login status`.
- Public GitHub visibility does not grant permission to use code; see the license before reuse.

## Repository layout

```text
autodl-codex-setup/
├── SKILL.md
└── agents/
    └── openai.yaml
```

## License

Released under the [MIT License](LICENSE).

## Security

Please see [SECURITY.md](SECURITY.md) for secret-handling guidance and vulnerability reports.
