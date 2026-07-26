<p align="center">
  <strong>AutoDL Codex Setup</strong>
</p>

<p align="center">
  <a href="README.zh-CN.md">简体中文</a> · <a href="README.md">English</a>
</p>

使用 Windows SSH 和 VS Code Remote-SSH，为 AutoDL 或其他远程 Ubuntu 服务器配置 [OpenAI Codex](https://developers.openai.com/codex/)。

## 功能范围

- 为本机 HTTP 代理配置主机级 `RemoteForward`
- 配置远程 `~/.codex/config.toml`
- 配置 VS Code Remote-SSH 代理
- 在缺少依赖时安装 Node.js 和 Codex CLI
- 执行 `codex login --device-auth` 并安全验证登录状态
- 检查端口冲突并验证完整代理链路

## 快速示例

请将占位符替换为你自己的服务器信息。不要把真实域名、端口、用户名、凭据或设备验证码提交到公开仓库。

```ssh
Host autodl-example
  HostName <你的服务器地址>
  Port <SSH端口>
  User <SSH用户>
  RemoteForward <服务器代理端口> 127.0.0.1:<本机代理端口>
```

服务器端 Codex 使用 `http://127.0.0.1:<服务器代理端口>`；本机代理仍然监听在 `127.0.0.1:<本机代理端口>`。

## 安装 Skill

克隆本仓库后，将 `autodl-codex-setup` 目录复制到 Codex 的 Skills 目录：

```powershell
Copy-Item .\autodl-codex-setup "$HOME\.codex\skills\autodl-codex-setup" -Recurse
```

然后让 Codex 配置服务器，例如：

```text
Use autodl-codex-setup to configure this AutoDL host:
Host autodl-example
  HostName <你的服务器地址>
  Port <SSH端口>
  User <SSH用户>
```

## 可直接复制给 Codex 的 Prompt

安装 Skill 后，复制下面的 Prompt 到 Codex。请先把 `<...>` 中的占位符替换成你自己的信息。GitHub 代码块右上角通常会提供复制按钮。

```text
请使用 autodl-codex-setup Skill，为下面这台远程 AutoDL 服务器配置 Codex。

SSH 信息：
Host <SSH别名>
  HostName <你的服务器地址>
  Port <SSH端口>
  User <SSH用户>

本机 HTTP 代理端口：<本机代理端口>
建议使用的、与其他服务器不冲突的远端代理端口：<服务器代理端口>

请端到端完成以下流程：
1. 检查本机代理、现有 SSH 主机配置，以及远程服务器的系统、Node.js、npm、Codex CLI、Codex 配置、VS Code 设置和登录状态。
2. 只新增或修改这台服务器对应的 SSH RemoteForward，使远端代理端口转发到本机代理端口；保留其他配置并避免端口冲突。
3. 使用远端代理端口配置远程 Codex 和 VS Code。
4. 仅在 Node.js 或 Codex CLI 缺失或不可用时安装它们。
5. 执行 `codex login --device-auth`，把设备登录网址和一次性验证码展示给我，然后等待我完成浏览器确认再继续。
6. 验证 `codex login status`、Codex 版本、SSH 连通性和完整代理链路。

不要打印或提交 auth.json、Token、密码、私钥、使用后的一次性验证码或真实基础设施细节。所有验证步骤通过后才能报告完成；请报告修改的文件、远程路径、端口和仍需我手动完成的步骤，但不要暴露敏感信息。
```

### 占位符说明

请使用你自己的服务器信息；下面仅是非真实占位符：

```text
SSH别名：autodl-example
服务器地址：<你的服务器地址>
SSH端口：<SSH端口>
SSH用户：<SSH用户>
本机代理端口：<本机代理端口>
服务器代理端口：<服务器代理端口>
```

## 安全说明

- 每台服务器应使用独立的远端转发端口。
- 保留原有 SSH、TOML 和 JSON 中与代理无关的配置。
- 不要提交 `auth.json`、Token、密码、私钥或设备验证码。
- HTTP 代理测试成功不代表 Codex 已完成认证，仍需执行 `codex login status`。
- 仓库公开不等于自动授予代码使用权，复用前请查看许可证。

## 仓库结构

```text
autodl-codex-setup/
├── SKILL.md
└── agents/
    └── openai.yaml
```

## 许可证

本项目采用 [MIT License](LICENSE) 发布。

## 安全问题

请阅读 [SECURITY.md](SECURITY.md)，了解敏感信息处理和漏洞报告方式。
