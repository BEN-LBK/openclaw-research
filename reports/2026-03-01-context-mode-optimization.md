# 编码代理的 98% 上下文窗口优化：Context Mode 深度解析

> 原文：[Stop Burning Your Context Window — We Built Context Mode](https://mksg.lu/blog/context-mode) by Mert Köseoğlu
> 
> 调研日期：2026-03-01

---

## 核心问题：上下文窗口被"燃烧"

Claude Code 拥有 200K 的上下文窗口，但这个宝贵的资源正在被快速消耗。

### 问题数据

| 工具调用 | 上下文消耗 |
|---------|-----------|
| 单次 Playwright 快照 | 56 KB |
| 20 个 GitHub issues | 59 KB |
| 一份访问日志 | 45 KB |
| 分析 CSV（500行） | 85 KB |

**30 分钟后，40% 的上下文已经消失。**

更严重的是，当激活 81+ 个 MCP 工具时，**143K tokens（72%）在发送第一条消息前就已经被消耗**——全部用于工具定义。

## 解决方案：Context Mode

Context Mode 是一个 MCP 服务器，它坐在 Claude Code 和工具输出之间，将原始数据在进入上下文前进行压缩处理。

### 效果对比

| 场景 | 原始大小 | 压缩后 | 压缩比 |
|-----|---------|-------|-------|
| Playwright 快照 | 56 KB | 299 B | **99.5%** |
| GitHub issues (20个) | 59 KB | 1.1 KB | **98.1%** |
| 访问日志 (500请求) | 45 KB | 155 B | **99.7%** |
| 分析 CSV (500行) | 85 KB | 222 B | **99.7%** |
| Git log (153 commits) | 11.6 KB | 107 B | **99.1%** |
| 仓库研究 (子代理) | 986 KB | 62 KB | **93.7%** |

**整体效果：315 KB → 5.4 KB，压缩率 98%**

## 技术实现

### 1. 沙箱机制（Sandbox）

每个 `execute` 调用都会启动一个隔离的子进程：
- 独立的进程边界，脚本之间无法互相访问内存或状态
- 子进程运行代码，捕获 stdout
- **只有 stdout 进入对话上下文**
- 原始数据（日志、API 响应、快照）永远不离开沙箱

**支持的语言运行时：**
JavaScript、TypeScript、Python、Shell、Ruby、Go、Rust、PHP、Perl、R（共 10 种）

**认证 CLI 支持：**
`gh`、`aws`、`gcloud`、`kubectl`、`docker` 通过凭据传递工作——子进程继承环境变量和配置路径，但不暴露给对话。

### 2. 知识库（Knowledge Base）

`index` 工具的工作原理：
1. 按标题分块 markdown 内容，保持代码块完整
2. 存储到 **SQLite FTS5**（全文搜索 5）虚拟表
3. 使用 **BM25 排名**算法进行相关性评分
4. 应用 **Porter 词干提取**，使 "running"、"runs"、"ran" 匹配同一词干

`search` 返回**精确的代码块及其标题层级**——不是摘要，不是近似值，而是实际索引的内容。

`fetch_and_index` 扩展到 URL：获取、HTML转markdown、分块、索引。**原始页面永不进入上下文。**

## 实际改变

### 对开发者的影响

- **无需改变工作方式**
- Context Mode 包含 PreToolUse 钩子，自动将工具输出路由到沙箱
- 子代理学会使用 `batch_execute` 作为主要工具
- Bash 子代理升级为 `general-purpose` 以访问 MCP 工具

### 会话时间对比

| 指标 | 优化前 | 优化后 |
|-----|-------|-------|
| 会话变慢时间 | ~30 分钟 | ~3 小时 |
| 45分钟后上下文剩余 | 60% | 99% |
| 可用工作时间提升 | - | **6 倍** |

## 安装方式

### 方式一：Plugin Marketplace（推荐）
```bash
/plugin marketplace add mksglu/claude-context-mode
/plugin install context-mode@claude-context-mode
```

### 方式二：MCP-only
```bash
claude mcp add context-mode -- npx -y context-mode
```

重启 Claude Code 即可。

## 设计思路

作者运营 MCP Directory & Hub，日均 10 万+ 请求，看到了每个 MCP 服务器的模式：

> 每个人都在构建向上下文倾倒原始数据的工具。没有人解决输出端的问题。

Cloudflare 的 Code Mode 博文启发了他们——Cloudflare 压缩了工具定义，Context Mode 压缩了工具输出。**同样的原理，相反的方向。**

## 总结

Context Mode 解决了一个被忽视但关键的问题：AI 编码代理的上下文窗口是有限资源，而工具输出正在大量"燃烧"它。通过沙箱隔离和智能压缩，将 315 KB 的原始输出压缩到 5.4 KB，让开发者可以连续工作 3 小时而不是 30 分钟。

**开源地址：** https://github.com/mksglu/claude-context-mode

---

*关键词：MCP、Claude Code、上下文优化、编码代理、开发者工具*
