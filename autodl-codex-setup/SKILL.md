---
name: autodl-codex-setup
description: Use when configuring OpenAI Codex on an AutoDL or similar remote Linux server through Windows SSH/VS Code Remote-SSH, especially when the server needs a local HTTP proxy, Node.js/Codex installation, device-code login, or end-to-end verification.
---

# AutoDL Codex Setup

Configure a remote Ubuntu server so Codex can run through an SSH reverse proxy tunnel and be used from VS Code Remote-SSH. Treat each host as independent: re-check its state instead of assuming another container has the same software, port, or login.

## Required inputs

Collect or infer:

- SSH alias, `HostName`, SSH `Port`, and `User`.
- Local HTTP proxy listen port; default to `7897` only after checking that `127.0.0.1:<port>` is listening.
- A unique remote listen port for this host, such as `17897`, `17898`, or `17899`. It may differ from the local proxy port.

Never put ChatGPT tokens, `auth.json`, passwords, or device codes in the skill, Git, logs, or command output beyond what the user must enter interactively.

## Workflow

### 1. Inspect before changing

On Windows PowerShell, verify the local proxy and inspect `C:\Users\<user>\.ssh\config`. Read the target host block and preserve unrelated entries. On the server, check:

```bash
cat /etc/os-release
command -v node; command -v npm; command -v codex
codex --version 2>/dev/null || true
codex login status 2>/dev/null || true
```

Also check whether `~/.codex/config.toml` and `~/.vscode-server/data/Machine/settings.json` already exist. Do not overwrite non-proxy settings blindly.

### 2. Add a host-scoped SSH reverse tunnel

Add this to the target host block in the local SSH config:

```ssh
Host <alias>
  HostName <hostname>
  Port <ssh-port>
  User <user>
  RemoteForward <remote-proxy-port> 127.0.0.1:<local-proxy-port>
```

The direction is important: the server-side Codex uses `127.0.0.1:<remote-proxy-port>`, which reaches the local proxy at `127.0.0.1:<local-proxy-port>`. Keep `RemoteForward` inside this host block; never make it global.

Validate with:

```powershell
ssh -o BatchMode=yes -o ExitOnForwardFailure=yes <alias> "echo SSH_OK"
```

If the forward fails, inspect existing SSH sessions and choose another remote port. Do not silently remove another host's tunnel.

### 3. Configure Codex and VS Code on the server

Set the proxy endpoint to the remote listen port, preserving other settings:

```toml
[proxy]
http_proxy = "http://127.0.0.1:<remote-proxy-port>"
https_proxy = "http://127.0.0.1:<remote-proxy-port>"
```

In `/root/.vscode-server/data/Machine/settings.json`, preserve existing JSON and set:

```json
{
  "http.proxy": "http://127.0.0.1:<remote-proxy-port>",
  "http.proxySupport": "on",
  "http.proxyStrictSSL": false
}
```

If the remote VS Code directory does not exist, create only the required parent directory after confirming the target server and user.

### 4. Install missing runtime components

Codex CLI requires a current Node.js runtime. Prefer Node.js 22 from a trusted official distribution source on Ubuntu 22.04; do not use the Ubuntu 22.04 default Node.js 12 package. Route downloads through the active tunnel:

```bash
export http_proxy=http://127.0.0.1:<remote-proxy-port>
export https_proxy=http://127.0.0.1:<remote-proxy-port>
curl -fsSL --proxy "$http_proxy" https://deb.nodesource.com/setup_22.x -o /tmp/nodesource_setup_22.sh
bash /tmp/nodesource_setup_22.sh
apt-get install -y nodejs
npm install --global @openai/codex
```

Skip installation when `node --version`, `npm --version`, and `codex --version` already satisfy the requirement. Do not install a second copy into a different Conda environment without checking login-shell `PATH`.

### 5. Authenticate interactively

Start the device flow in a TTY:

```bash
codex login --device-auth
```

Show the generated URL and one-time device code to the user, ask them to complete the browser confirmation, then run:

```bash
codex login status
```

Report only the status (`Logged in using ChatGPT` or the error). Never print `~/.codex/auth.json`.

### 6. Verify end to end

Verify all of the following separately:

```bash
node --version
npm --version
codex --version
codex login status
curl -I --max-time 10 -x http://127.0.0.1:<remote-proxy-port> https://api.openai.com
```

The HTTP response proves the proxy path, not that an API request was authorized. Reconnect VS Code Remote-SSH after changing remote settings.

## Common failures

| Symptom | Action |
|---|---|
| `Host key verification failed` | Use `StrictHostKeyChecking=accept-new` only for a newly confirmed host, then retry. |
| `remote port forwarding failed` | Check for a live SSH session or occupied remote port; select a unique remote port and update both server config files. |
| `curl: (7) connection refused` on the remote proxy | Confirm the SSH connection actually includes `RemoteForward`; do not use `ClearAllForwardings=yes` while testing the tunnel. |
| `codex: command not found` | Check the login-shell `PATH`; verify the global npm bin directory and install only once. |
| Login succeeds but Codex cannot connect | Verify the server proxy uses the remote port, while SSH maps that port to the local proxy port. |
| Existing config contains unrelated settings | Edit only the proxy keys and preserve the rest. |

## Completion criteria

Complete only when the target host has: a working plain SSH connection, a host-scoped reverse tunnel, valid Codex/VS Code proxy settings, `codex --version`, and a verified `codex login status`. If any condition is unverified, report it explicitly instead of claiming completion.
