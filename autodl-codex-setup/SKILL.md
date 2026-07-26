---
name: autodl-codex-setup
description: Use when configuring OpenAI Codex on an AutoDL or similar remote Linux server through Windows SSH/VS Code Remote-SSH, especially when the server needs a local HTTP proxy, Node.js/Codex installation, device-code login, endpoint diagnosis, or cleanup after a timed-out SSH command.
---

# AutoDL Codex Setup

Configure a remote Linux server so Codex can use a local HTTP proxy through a host-scoped SSH reverse tunnel and VS Code Remote-SSH. Treat every host as independent and every authentication artifact as sensitive.

## Required inputs and privacy rules

Collect or infer:

- A unique SSH alias, `HostName`, SSH `Port`, and `User`.
- The local HTTP proxy listen port; use `7897` only after checking that `127.0.0.1:<port>` is listening.
- A unique remote listen port for this host. It may differ from the local proxy port.

Never put ChatGPT tokens, `auth.json`, passwords, private keys, device codes, real private hostnames, or private infrastructure ports in the Skill, Git, logs, examples, or normal command output. A device code may be shown only as a short-lived interactive handoff when the user explicitly started the login; never persist or replay it.

## 1. Inspect before changing

On Windows, inspect the local proxy and the SSH config before writing. Search for duplicate `Host <hostname>` blocks: OpenSSH uses the first obtained value for each parameter, so reusing a hostname block with multiple ports is unsafe. Prefer a new unique alias such as `autodl-example-36927`, not another `Host <hostname>` block.

The user SSH config is outside most workspaces. If access is denied, request a narrowly scoped elevated operation. Before writing:

1. Confirm the alias does not already exist.
2. Do not rewrite the whole file or silently replace an existing alias.
3. Append only the new host block, preserving all other entries.
4. After writing, validate with:

```powershell
ssh -o BatchMode=yes -o ExitOnForwardFailure=yes <alias> "echo SSH_OK"
```

On the server, inspect state independently:

```bash
cat /etc/os-release
command -v node; command -v npm; command -v codex
node --version 2>/dev/null || true
npm --version 2>/dev/null || true
codex --version 2>/dev/null || true
codex login status 2>/dev/null || true
test -e ~/.codex/config.toml && echo CODEX_CONFIG_EXISTS || true
test -e ~/.vscode-server/data/Machine/settings.json && echo VS_CODE_SETTINGS_EXISTS || true
test -e ~/.codex/auth.json && echo AUTH_EXISTS || true
df -h / /
```

Never read or print the contents of `~/.codex/auth.json`.

## 2. Add a host-scoped reverse tunnel

Add this only inside the unique alias block in the local SSH config:

```ssh
Host <alias>
  HostName <hostname>
  Port <ssh-port>
  User <user>
  RemoteForward <remote-proxy-port> 127.0.0.1:<local-proxy-port>
```

The server-side Codex endpoint is `127.0.0.1:<remote-proxy-port>` and the local proxy endpoint is `127.0.0.1:<local-proxy-port>`. Keep `RemoteForward` host-scoped; never make it global.

Use `-o ExitOnForwardFailure=yes` for every forward validation. If the forward fails, inspect live SSH sessions and the remote port before choosing another port. Do not kill an unknown user task.

## 3. Execute remote commands safely from PowerShell

PowerShell does not use backslash to escape double quotes. Do not write nested commands such as `\\"...\\"` and send them through Windows OpenSSH into Bash.

Prefer short, static commands with the entire remote command in a PowerShell single-quoted string, avoiding internal single quotes:

```powershell
$remoteCommand = 'set -eu; command -v codex; codex --version'
ssh -o BatchMode=yes -o ConnectTimeout=15 <alias> $remoteCommand
```

For long configuration or installation stages, use a temporary uploaded script, base64 over stdin, or a clearly bounded remote script. Run one phase at a time: inspect, edit, install, login, verify. After a failure, inspect state before retrying; do not concatenate a large recovery command.

Do not place a regex containing `|` inside unverified nested quoting. Prefer separate fixed-string checks such as `grep -F http.proxy settings.json`, or parse JSON with a short uploaded script. Give every remote check a timeout.

## 4. Configure Codex and VS Code without clobbering settings

Preserve unrelated TOML and JSON keys. Set only the proxy values:

```toml
[proxy]
http_proxy = "http://127.0.0.1:<remote-proxy-port>"
https_proxy = "http://127.0.0.1:<remote-proxy-port>"
```

In `~/.vscode-server/data/Machine/settings.json`, set:

```json
{
  "http.proxy": "http://127.0.0.1:<remote-proxy-port>",
  "http.proxySupport": "on",
  "http.proxyStrictSSL": false
}
```

If either file exists, inspect and merge only the proxy keys. Create the parent directory only after confirming the target host and user.

## 5. Install missing runtime components

Check Node.js, npm, Codex, login-shell `PATH`, disk space, and active package processes first. Prefer Node.js 22 from a trusted official distribution source on Ubuntu; do not install the outdated Ubuntu default Node.js package merely because it is available.

When installation is needed, route downloads through the active remote forward and use bounded, separately observable stages:

```bash
export http_proxy=http://127.0.0.1:<remote-proxy-port>
export https_proxy=http://127.0.0.1:<remote-proxy-port>
curl --fail --silent --show-error --max-time 30 --proxy "$http_proxy" \
  https://deb.nodesource.com/setup_22.x -o /tmp/nodesource_setup_22.sh
bash /tmp/nodesource_setup_22.sh
apt-get install -y nodejs
npm install --global @openai/codex
node --version; npm --version; codex --version
```

Do not start a second install while the first package process is still running. If a tool timeout occurs, inspect `ps`, disk, package state, and the process command line before retrying.

## 6. Diagnose the proxy and authentication in layers

Run these checks in order:

1. SSH connects with the unique alias and `ExitOnForwardFailure=yes`.
2. A safe `HEAD` or `GET` through the remote proxy reaches a public API endpoint. `HTTP 421` can prove the path reached the service/proxy; it does not prove authorization.
3. A safe `GET` or `HEAD` to the device-auth endpoint may return `405`; that can prove endpoint reachability. Do not use `POST` as a network probe. A POST may create a real one-time device code and has side effects.
4. If `codex login --device-auth` returns `403`, report that the Codex CLI request was rejected with HTTP 403. Do not conclude that SSH or the proxy is definitely broken. Possible causes include request-header/User-Agent handling, CLI/auth-service compatibility, or an authentication-edge policy; treat these as hypotheses, not confirmed root causes.
5. Suggest a clean shell, WSL, a different network/egress node, or an updated CLI as controlled follow-up tests.

Never print, persist, or use an endpoint probe to generate a device code. Do not display device codes in automated logs. If a real login needs a code, hand it to the user only through an interactive TTY flow.

## 7. Handle interactive login and timeout residue

`ssh -tt ... codex login --device-auth` is interactive and may outlive a non-interactive tool timeout. Prefer a real user-controlled terminal. If the agent starts the TTY:

- Set a bounded timeout and record the exact local SSH PID it created.
- Do not interpret a tool timeout as login failure.
- After timeout, use a separate direct SSH check to inspect `ps`, the relevant remote port, and matching process command lines.
- Only terminate PIDs created by this run and verified by command line; never kill a generic `sshd`, `node`, `codex`, `grep`, or user training process.
- Before retrying the forward, confirm the remote port is released.
- When testing a replacement forwarding session, use `ClearAllForwardings=yes` only for that narrowly scoped test if stale forwarding state may be inherited; do not add it to the persistent host block unless the user explicitly requests that behavior.

After the user completes browser confirmation, verify only:

```bash
codex login status
```

Report the status, never the credential file or its contents.

## 8. auth.json fallback is opt-in only

If device authentication fails and a local Codex login file exists, do not copy it by default. Explain that copying it gives the target server access to the user's existing ChatGPT authorization and ask for explicit confirmation using clear wording such as: “I authorize copying my existing Codex login to this confirmed target host.”

Only after explicit authorization:

1. Confirm the target host and user again.
2. Check whether the remote `~/.codex/auth.json` already exists; do not overwrite unknown login state.
3. Copy the file through an approved sensitive-file transfer path.
4. Run `chmod 600 ~/.codex/auth.json` remotely.
5. Verify only `codex login status`.

Never place the file in a patch, Skill, log, shell output, or chat message, and never read or print its contents.

## 9. Completion gates

Claim completion only when each applicable gate is separately proven:

- The unique alias connects; duplicate hostname blocks were not reused.
- The host-scoped `RemoteForward` succeeds and the remote proxy endpoint is reachable.
- Codex and VS Code proxy settings exist, use the remote port, and preserve unrelated settings.
- Node/npm/Codex versions are available on the login-shell `PATH`.
- `codex login status` succeeds, or the result is explicitly reported as not logged in/403.
- HTTP `421`, auth-endpoint `405`, or a successful proxy connection is not misreported as authorization.
- No SSH, Codex, grep, package, or forwarding process created by this run remains unexpectedly; unknown user processes are untouched.
- If the auth fallback was used, explicit user authorization was recorded as a decision only; no credential content was recorded.

If any gate is unverified, report it explicitly instead of claiming success.
