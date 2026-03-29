# OpenClaw 可用 CLI 工具调研报告

> 调研时间：2026-03-29
> 调研目的：寻找适合在 OpenClaw 上部署的小红书/Twitter CLI 及其他好用工具

---

## 一、小红书 CLI 工具

### 1. **xiaohongshu-cli** ⭐⭐⭐⭐⭐
- **GitHub**: https://github.com/jackwener/xiaohongshu-cli
- **功能**：通过逆向工程 API 实现小红书搜索、阅读、互动
- **OpenClaw 集成**：✅ 已有 OpenClaw Skill 封装
- **安装方式**：
  ```bash
  clawhub install jackwener-xhs-cli
  ```
- **适用场景**：内容监控、数据分析、自动化运营

### 2. **xhs-mcp** ⭐⭐⭐⭐
- **官网**: https://algovate.github.io/xhs-mcp/
- **功能**：基于 MCP 协议的小红书自动化工具
  - 登录、发布、搜索、推荐
  - 支持 Puppeteer 无头浏览器
  - 图文/视频发布、用户笔记管理、评论互动
- **特点**：支持 AI 助手集成（Claude、Cursor 等）
- **适合场景**：AI 驱动的自动化运营

### 3. **xhs-toolkit** ⭐⭐⭐
- **功能**：基于 AI 和 MCP 的小红书自动化工具包
- **特点**：集成 DeepSeek 等 AI 模型
- **适合场景**：自动发布笔记、内容生成

### 4. **xhs-mp-cli** ⭐⭐
- **NPM**: https://www.npmjs.com/package/xhs-mp-cli
- **功能**：小红书官方小程序命令行工具
- **限制**：仅支持小程序相关操作（登录、预览、上传）
- **适合场景**：小程序开发者

---

## 二、Twitter/X CLI 工具

### 1. **twurl** (Twitter 官方)
- **GitHub**: https://github.com/twitter/twurl
- **功能**：Twitter 官方命令行工具
- **特点**：支持 OAuth 认证，直接调用 Twitter API
- **适合场景**：API 开发测试

### 2. **t** (CLI Twitter Client)
- **GitHub**: https://github.com/sferik/t
- **功能**：功能丰富的 Twitter 命令行客户端
- **特点**：Ruby 编写，支持几乎所有 Twitter API 功能
- **适合场景**：日常 Twitter 操作自动化

### 3. **twitter-api-v2**
- **GitHub**: https://github.com/PLhery/node-twitter-api-v2
- **功能**：Node.js Twitter API v2 客户端
- **特点**：支持 TypeScript，易于集成
- **适合场景**：在 OpenClaw 中用 Node.js 调用

### 4. **xurl** (OpenClaw 已有 Skill) ⭐⭐⭐⭐⭐
- **位置**: `~/.agents/skills/xurl/`
- **功能**：X (Twitter) API 的认证请求 CLI
- **支持操作**：
  - 发推、回复、引用
  - 搜索、读取帖子
  - 管理关注者
  - 发送 DM
  - 上传媒体
  - 交互 X API v2 端点
- **优势**：✅ 已集成到 OpenClaw，开箱即用！

---

## 三、其他推荐的 CLI 工具（适合 OpenClaw）

### 🔥 生产力工具

| 工具 | GitHub | 功能 | 推荐度 |
|------|--------|------|--------|
| **fzf** | junegunn/fzf | 模糊搜索神器 | ⭐⭐⭐⭐⭐ |
| **ripgrep (rg)** | BurntSushi/ripgrep | 超快文本搜索 | ⭐⭐⭐⭐⭐ |
| **bat** | sharkdp/bat | 带语法高亮的 cat | ⭐⭐⭐⭐⭐ |
| **exa** | ogham/exa | 现代化的 ls | ⭐⭐⭐⭐ |
| **fd** | sharkdp/fd | 现代化的 find | ⭐⭐⭐⭐ |
| **delta** | dandavison/delta | 美化 git diff | ⭐⭐⭐⭐ |

### 🌐 网络工具

| 工具 | GitHub | 功能 | 推荐度 |
|------|--------|------|--------|
| **httpie** | httpie/httpie | 人性化的 HTTP 客户端 | ⭐⭐⭐⭐⭐ |
| **curlie** | rs/curlie | curl + httpie 结合体 | ⭐⭐⭐⭐ |
| **dog** | ogham/dog | DNS 查询工具 | ⭐⭐⭐ |

### 📊 数据处理

| 工具 | GitHub | 功能 | 推荐度 |
|------|--------|------|--------|
| **jq** | stedolan/jq | JSON 处理神器 | ⭐⭐⭐⭐⭐ |
| **yq** | mikefarah/yq | YAML 处理工具 | ⭐⭐⭐⭐ |
| **csvkit** | wireservice/csvkit | CSV 处理工具集 | ⭐⭐⭐⭐ |

### 🔧 开发工具

| 工具 | GitHub | 功能 | 推荐度 |
|------|--------|------|--------|
| **gh** | cli/cli | GitHub 官方 CLI | ⭐⭐⭐⭐⭐ |
| **hub** | github/hub | GitHub 扩展工具 | ⭐⭐⭐⭐ |
| **tig** | jonas/tig | Git 文本界面 | ⭐⭐⭐⭐ |
| **lazygit** | jesseduffield/lazygit | Git 终端 UI | ⭐⭐⭐⭐⭐ |

### 📱 社交媒体工具

| 工具 | 平台 | 功能 | 推荐度 |
|------|------|------|--------|
| **himalaya** | Email | 邮件管理 CLI | ⭐⭐⭐⭐⭐ |
| **newsboat** | RSS | RSS 阅读器 | ⭐⭐⭐⭐ |
| **toot** | Mastodon | Mastodon CLI | ⭐⭐⭐ |

---

## 四、OpenClaw Skill 资源

### 官方资源
1. **ClawHub** - https://clawhub.ai
   - 1700+ 社区 Skill
   - 一键安装：`clawhub install <skill-name>`

2. **OpenClaw Skills Library** - https://openclawskills.io/skills
   - 按类别筛选
   - 搜索功能

3. **Awesome OpenClaw Skills** - https://github.com/VoltAgent/awesome-openclaw-skills
   - 精选 Skill 列表
   - 分类整理

### 已安装的 Skill（当前系统）
根据 `~/.agents/skills/` 目录，已安装：
- ✅ xurl (Twitter/X API)
- ✅ lark-* 系列（飞书全家桶）
- ✅ clawhub（Skill 管理器）
- ✅ coding-agent（代码任务）
- ✅ weather（天气）
- ✅ apple-notes（备忘录）
- ✅ apple-reminders（提醒事项）
- ✅ himalaya（邮件）
- ✅ github（GitHub 操作）
- ✅ 1password（密码管理）

---

## 五、推荐部署方案

### 方案 A：社交媒体自动化套件
```bash
# 安装小红书 CLI
clawhub install jackwener-xhs-cli

# Twitter 已有 xurl skill
# 安装 Mastodon CLI（可选）
npm install -g toot
```

### 方案 B：生产力工具套件
```bash
# 核心工具
brew install fzf ripgrep bat exa fd jq

# Git 工具
brew install tig lazygit gh

# 网络工具
brew install httpie
```

### 方案 C：数据处理套件
```bash
# JSON/YAML/CSV 处理
brew install jq yq csvkit

# 文本处理
brew install ripgrep fd
```

---

## 六、注意事项

### ⚠️ 风险提示
1. **小红书 CLI**：基于逆向工程 API，有封号风险，建议：
   - 使用小号测试
   - 控制请求频率
   - 遵守平台规则

2. **Twitter/X CLI**：
   - 需要 API Key（X API v2 需要付费）
   - 注意 API 速率限制
   - xurl skill 已配置好，直接使用

3. **恶意 Skill 风险**：
   - 2024 年发现 1184 个恶意 Skill
   - 只从 ClawHub 官方或可信源安装
   - 安装前检查代码

### ✅ 最佳实践
1. 优先使用 ClawHub 官方 Skill
2. 安装前查看 Skill 评分和下载量
3. 定期更新：`clawhub update <skill-name>`
4. 测试环境先行验证

---

## 七、总结

### 小红书方向
- **推荐**：`xiaohongshu-cli` (jackwener-xhs-cli)
- **理由**：已有 OpenClaw Skill 封装，开箱即用
- **安装**：`clawhub install jackwener-xhs-cli`

### Twitter/X 方向
- **推荐**：使用已有的 `xurl` Skill
- **理由**：已集成，无需额外安装
- **位置**：`~/.agents/skills/xurl/`

### 其他好用的 CLI
- **必备**：fzf, ripgrep, bat, jq, gh, lazygit
- **推荐**：httpie, exa, fd, delta
- **安装**：通过 Homebrew 一键安装

---

**参考资源**：
- ClawHub: https://clawhub.ai
- OpenClaw Skills Library: https://openclawskills.io/skills
- OpenClaw 文档: https://docs.openclaw.ai

---

_🦞 报告完成 - OpenClaw 可用 CLI 工具调研_
