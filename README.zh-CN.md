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
