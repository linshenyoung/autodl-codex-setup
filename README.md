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

### Copy-paste installation prompt

Alternatively, copy this prompt into Codex to install the Skill automatically:

```text
Install the autodl-codex-setup Skill from https://github.com/linshenyoung/autodl-codex-setup into my user-level Codex Skills directory.

Please:
1. Inspect the repository structure before copying anything.
2. Install the directory that contains SKILL.md and agents/openai.yaml as ~/.codex/skills/autodl-codex-setup.
3. Prefer the available Skill installer when supported; otherwise clone or download the repository and copy the correct directory.
4. Do not overwrite an existing installation without checking whether it is the same Skill and asking before replacing local changes.
5. Validate the installed SKILL.md and report the exact installation path and validation result.
6. Do not copy auth.json, tokens, passwords, private keys, device codes, or any unrelated repository files into the Skill directory.
```

Then ask Codex to configure a host, for example:

```text
Use autodl-codex-setup to configure this AutoDL host:
Host autodl-example
  HostName <your-autodl-host>
  Port <ssh-port>
  User <ssh-user>
```

## Copy-paste prompt for Codex

After installing the Skill, copy the prompt below into Codex. Replace the values inside `<...>` first. GitHub's code blocks include a copy button.

```text
Use the autodl-codex-setup Skill to configure Codex on this remote AutoDL server.

SSH details:
Host <ssh-alias>
  HostName <your-autodl-host>
  Port <ssh-port>
  User <ssh-user>

Local HTTP proxy port: <local-proxy-port>
Preferred unique remote proxy port: <remote-proxy-port>

Please complete the workflow end to end:
1. Inspect the local proxy, existing SSH host block, and the remote server's OS, Node.js, npm, Codex CLI, Codex config, VS Code settings, and login status.
2. Add or update only this host's SSH RemoteForward so the remote proxy port maps to the local proxy port. Preserve unrelated settings and avoid port conflicts.
3. Configure the remote Codex and VS Code proxy settings using the remote proxy port.
4. Install Node.js and the official Codex CLI only if they are missing or unusable.
5. Run `codex login --device-auth`. Show me the device URL and one-time code, then wait for me to finish browser confirmation before continuing.
6. Verify `codex login status`, Codex version, SSH connectivity, and the end-to-end proxy path.

Do not print or commit auth.json, tokens, passwords, private keys, device codes after use, or real infrastructure details. Do not claim completion until every verification step has passed. Report changed files, remote paths, ports, and any remaining manual action without exposing secrets.
```

### Example values

Use values from your own server only; the following are intentionally non-real placeholders:

```text
SSH alias: autodl-example
HostName: <your-autodl-host>
SSH port: <ssh-port>
User: <ssh-user>
Local proxy port: <local-proxy-port>
Remote proxy port: <remote-proxy-port>
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
