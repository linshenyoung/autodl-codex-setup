# AutoDL Codex Setup

<p align="center">
  <a href="README.zh-CN.md">简体中文</a> · <a href="README.md">English</a>
</p>

通过 Windows SSH 和 VS Code Remote-SSH，为 AutoDL 或类似的远程 Linux 服务器配置 [OpenAI Codex](https://developers.openai.com/codex/)。

本仓库提供一个可复用的 Codex Skill，面向公众开放。仓库不包含个人主机名、凭据、Token、设备码或私有基础设施信息。

## Skill 可以处理什么

- 本地 SSH 配置存在重复主机名时，自动采用唯一别名
- 通过 SSH `RemoteForward` 将远程服务器连接到本地 HTTP 代理
- 配置 `~/.codex/config.toml` 中的 Codex 代理
- 保留无关 JSON 设置的前提下配置 VS Code Remote-SSH 代理
- 缺少 Node.js 或 Codex CLI 时进行安装
- 分层检查 SSH、代理、端点、认证、超时残留和清理状态
- 通过用户可控终端完成交互式 `codex login --device-auth`
- 对已有本地 `auth.json` 提供明确授权后才执行的安全回退方案

## 安装

### 方式一：直接让 Codex 安装

将下面的 Prompt 复制给 Codex：

```text
请从 https://github.com/linshenyoung/autodl-codex-setup 安装公开的 autodl-codex-setup Skill。

请完成：
1. 先检查仓库结构，找到同时包含 SKILL.md 和 agents/openai.yaml 的目录。
2. 将这个目录安装到 ~/.codex/skills/autodl-codex-setup。
3. 如果目标目录已经存在，先比较内容；未经确认不要覆盖本地修改。
4. 验证安装后的 SKILL.md，并报告安装路径和验证结果。
5. 不要把 auth.json、Token、密码、私钥、设备码或无关文件复制到 Skill 目录。
```

### 方式二：手动安装

克隆本仓库后，复制内部的 Skill 目录：

```powershell
Copy-Item .\autodl-codex-setup "$HOME\.codex\skills\autodl-codex-setup" -Recurse
```

安装目录应包含 `SKILL.md`、`agents/openai.yaml` 和 `scripts/regression_check.py`。

## 让 Codex 配置服务器

先把所有占位符替换成你自己的信息，再将下面的 Prompt 复制给 Codex：

```text
请使用 autodl-codex-setup Skill 配置下面这台远程 AutoDL 服务器上的 Codex。

SSH 信息：
Host <唯一的SSH别名>
  HostName <你的AutoDL服务器地址>
  Port <SSH端口>
  User <SSH用户名>

本地 HTTP 代理端口：<本地代理端口>
建议使用的、与其他服务器不冲突的远程代理端口：<远程代理端口>

请分阶段完成，并让每个阶段都可观察、可验证：
1. 检查本地代理和 SSH 配置，包括重复的 HostName 配置块。优先使用唯一别名，并保留无关配置。
2. 只为这台服务器添加 Host 作用域内的 RemoteForward，将远程代理端口转发到本地代理端口；使用 ExitOnForwardFailure=yes 验证。
3. 检查远程系统、磁盘、进程、Node.js、npm、Codex CLI、Codex 配置、VS Code 设置和登录状态。
4. 只配置 Codex 和 VS Code 的代理键，保留其他设置。
5. 仅在必要时分阶段安装 Node.js 和 @openai/codex。
6. 使用安全的 GET/HEAD 检查代理链路；不要把 device-auth 端点的 POST 当作网络探针。
7. 只有在用户可控的交互式终端中启动 codex login --device-auth；不要在自动化日志中打印或保存设备码。
8. 验证 codex login status、版本、SSH 转发、代理配置，以及本次流程创建的进程是否已清理。

如果登录返回 HTTP 403，请报告为 Codex CLI 请求被拒绝，不要直接断定 SSH 或代理损坏。可以建议使用干净 shell、WSL、其他网络出口或更新后的 CLI 进行复试。

不要读取、打印、提交或上传 auth.json、Token、密码、私钥、设备码或私有基础设施信息。除非我明确授权“将现有 Codex 登录复制到这台已确认的目标服务器”，否则不要复制已有 auth.json。
```

## SSH 转发原理

远程 Codex 使用远程回环地址上的端口，SSH 再把流量转回本地代理：

```text
远程 Codex -> 127.0.0.1:<远程代理端口>
          SSH RemoteForward
本地代理   <- 127.0.0.1:<本地代理端口>
```

仅使用占位符的示例：

```ssh
Host <唯一的SSH别名>
  HostName <你的AutoDL服务器地址>
  Port <SSH端口>
  User <SSH用户名>
  RemoteForward <远程代理端口> 127.0.0.1:<本地代理端口>
```

如果 SSH 配置中已经存在多个相同 HostName 的配置块，不要继续复用该主机名。使用唯一别名可以避免 OpenSSH 首个匹配规则带来的端口错误。

## 验证与安全边界

Skill 内置静态回归检查，不会连接服务器，也不会读取凭据：

```powershell
python .\autodl-codex-setup\scripts\regression_check.py
```

关键边界：

- HTTP 421 或认证端点返回 405 只能证明链路可达，不代表已经授权。
- 对 device-auth 端点发送 POST 可能创建真实的一次性设备码，不能用作网络探针。
- SSH 命令超时后可能仍有进程运行；必须检查本次流程创建的准确 PID 和端口，再决定是否清理。
- 不要随意终止通用的 `sshd`、`node`、`codex`、`grep` 或训练进程。
- 只有得到明确授权、且远程不存在已有登录文件时，才可以复制 `auth.json`；复制后只验证 `codex login status`。

## 仓库结构

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

## 许可证

MIT，详见 [LICENSE](LICENSE)。

有关敏感信息处理和漏洞报告，请参阅 [SECURITY.md](SECURITY.md)。
