# AutoDL Codex Setup

<p align="center">
  <a href="README.zh-CN.md">简体中文</a> · <a href="README.md">English</a>
</p>

Configure [OpenAI Codex](https://developers.openai.com/codex/) on AutoDL and similar remote Linux servers through Windows SSH and VS Code Remote-SSH.

This repository contains a reusable Codex Skill. It is designed for public use and intentionally contains no personal hostnames, credentials, tokens, device codes, or private infrastructure details.

## What it handles

- Unique SSH aliases when the local config contains duplicate hostname blocks
- Host-scoped SSH `RemoteForward` from the remote server to a local HTTP proxy
- Codex proxy settings in `~/.codex/config.toml`
- VS Code Remote-SSH proxy settings without clobbering unrelated JSON keys
- Node.js and the Codex CLI installation when missing
- Layered SSH, proxy, endpoint, authentication, timeout, and cleanup checks
- Safe interactive `codex login --device-auth` handoff
- Explicit opt-in handling for an existing local `auth.json` fallback

## Install

### Option A: ask Codex to install it

Copy this prompt into your Codex client:

```text
Install the public autodl-codex-setup Skill from https://github.com/linshenyoung/autodl-codex-setup.

Please:
1. Inspect the repository and locate the directory containing SKILL.md and agents/openai.yaml.
2. Install that directory as ~/.codex/skills/autodl-codex-setup.
3. If an installation already exists, compare it first and do not overwrite local changes without asking.
4. Validate the installed SKILL.md and report the installation path and result.
5. Do not copy auth.json, tokens, passwords, private keys, device codes, or unrelated files into the Skill directory.
```

### Option B: install manually

From a clone of this repository, copy the inner Skill directory:

```powershell
Copy-Item .\autodl-codex-setup "$HOME\.codex\skills\autodl-codex-setup" -Recurse
```

The installed directory should contain `SKILL.md`, `agents/openai.yaml`, and `scripts/regression_check.py`.

## Configure a server with Codex

Replace every placeholder before sending this prompt:

```text
Use the autodl-codex-setup Skill to configure Codex on this remote AutoDL server.

SSH details:
Host <unique-ssh-alias>
  HostName <your-autodl-host>
  Port <ssh-port>
  User <ssh-user>

Local HTTP proxy port: <local-proxy-port>
Preferred unique remote proxy port: <remote-proxy-port>

Complete the workflow in separate, observable phases:
1. Inspect the local proxy and SSH config, including duplicate hostname blocks. Prefer a unique alias and preserve unrelated entries.
2. Add only a host-scoped RemoteForward from the remote proxy port to the local proxy port. Verify SSH with ExitOnForwardFailure=yes.
3. Inspect the remote OS, disk, processes, Node.js, npm, Codex CLI, Codex config, VS Code settings, and login status.
4. Configure only the Codex and VS Code proxy keys, preserving unrelated settings.
5. Install Node.js and @openai/codex only when required, using bounded phases.
6. Validate the proxy path with safe GET/HEAD checks. Do not POST to a device-auth endpoint as a network probe.
7. Start codex login --device-auth only through a user-controlled interactive terminal. Do not print or persist the device code in automation logs.
8. Verify codex login status, versions, SSH forwarding, proxy configuration, and cleanup of processes created by this run.

If login returns HTTP 403, report it as a Codex CLI request rejection; do not automatically conclude that SSH or the proxy is broken. Suggest a clean shell, WSL, another network, or an updated CLI as follow-up tests.

Do not read, print, commit, or upload auth.json, tokens, passwords, private keys, device codes, or private infrastructure details. Do not copy an existing auth.json unless I explicitly authorize copying my existing Codex login to this confirmed target host.
```

## SSH forwarding model

The remote Codex process uses the remote loopback port. SSH carries that traffic back to the local proxy:

```text
remote Codex -> 127.0.0.1:<remote-proxy-port>
           SSH RemoteForward
local proxy  <- 127.0.0.1:<local-proxy-port>
```

Example with placeholders only:

```ssh
Host <unique-ssh-alias>
  HostName <your-autodl-host>
  Port <ssh-port>
  User <ssh-user>
  RemoteForward <remote-proxy-port> 127.0.0.1:<local-proxy-port>
```

Do not reuse a hostname block when the SSH config already contains multiple blocks for that hostname. A unique alias avoids OpenSSH first-match surprises.

## Validation and safety

The Skill includes a static regression check that does not contact any server or read credentials:

```powershell
python .\autodl-codex-setup\scripts\regression_check.py
```

Important boundaries:

- HTTP 421 or an auth endpoint returning 405 proves reachability, not authorization.
- A device-auth POST may create a real one-time code; never use it as a probe.
- A timed-out SSH command may leave processes behind; inspect exact PIDs and ports before retrying.
- Never kill generic `sshd`, `node`, `codex`, `grep`, or training processes.
- Copy an existing `auth.json` only after explicit user authorization, only when the remote file does not already exist, and verify only `codex login status` afterward.

## Repository layout

```text
autodl-codex-setup/
├── README.md
├── README.zh-CN.md
├── SECURITY.md
└── autodl-codex-setup/
    ├── SKILL.md
    ├── agents/openai.yaml
    └── scripts/regression_check.py
```

## License

MIT. See [LICENSE](LICENSE).

For secret-handling guidance and responsible vulnerability reports, see [SECURITY.md](SECURITY.md).
