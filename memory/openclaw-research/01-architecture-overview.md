# OpenClaw 核心架构调研

## 一、整体架构

### 1.1 核心组件

```
┌─────────────────────────────────────────────┐
│              OpenClaw Gateway               │
│         (单一长连接守护进程)                  │
└──────────────┬──────────────────────────────┘
               │ WebSocket (127.0.0.1:18789)
        ┌──────┴──────┬──────────────┬─────────┐
        │             │              │         │
    ┌───▼───┐    ┌───▼───┐     ┌───▼───┐  ┌──▼──┐
    │ macOS │    │  CLI  │     │ Web UI│  │Nodes│
    │  App  │    │       │     │       │  │     │
    └───────┘    └───────┘     └───────┘  └─────┘
        │
        │
    ┌───▼────────────────────────────────────┐
    │   通道 (Channels)                       │
    │  WhatsApp / Telegram / Slack / Discord │
    │  Signal / iMessage / Feishu / WebChat  │
    └────────────────────────────────────────┘
```

### 1.2 关键特性

- **单Gateway模式**：每个主机只有一个Gateway控制所有消息通道
- **WebSocket协议**：所有客户端通过WebSocket连接
- **设备配对**：基于设备ID的配对和认证机制
- **Agent运行时**：嵌入式pi-mono运行时

---

## 二、Gateway 架构

### 2.1 核心职责

**Gateway守护进程负责：**
1. 维护与所有通道的连接（WhatsApp、Telegram等）
2. 暴露类型化的WebSocket API
3. 验证入站消息（JSON Schema）
4. 发送事件：`agent`、`chat`、`presence`、`health`、`heartbeat`、`cron`

### 2.2 连接生命周期

```
Client → Gateway: connect请求
Gateway → Client: 连接确认 + 状态快照
Gateway → Client: presence/tick事件
Client → Gateway: agent请求
Gateway → Client: 流式响应
```

### 2.3 协议规范

**传输层：**
- WebSocket文本帧，JSON负载
- 首帧必须是`connect`
- 请求：`{type:"req", id, method, params}`
- 响应：`{type:"res", id, ok, payload|error}`
- 事件：`{type:"event", event, payload, seq?, stateVersion?}`

**认证：**
- 如果设置了`OPENCLAW_GATEWAY_TOKEN`，必须在`connect.params.auth.token`中匹配
- 幂等性键用于副作用方法（`send`、`agent`）

### 2.4 配置要点

```bash
# 启动Gateway
openclaw gateway

# 健康检查
# 通过WebSocket发送`health`请求

# 远程访问
# 推荐：Tailscale或VPN
# 备选：SSH隧道
ssh -N -L 18789:127.0.0.1:18789 user@host
```

---

## 三、Agent 运行时

### 3.1 工作空间（Workspace）

**必需配置：**
- `agents.defaults.workspace`：Agent的唯一工作目录
- 推荐使用`openclaw setup`初始化

**工作空间布局：**
```
~/.openclaw/workspace/
├── AGENTS.md          # 操作指令 + 记忆
├── SOUL.md            # 人格、边界、语气
├── TOOLS.md           # 工具使用笔记
├── BOOTSTRAP.md       # 首次运行仪式（完成后删除）
├── IDENTITY.md        # Agent名称/风格/emoji
├── USER.md            # 用户资料
├── MEMORY.md          # 长期记忆（可选）
└── memory/            # 每日日志
    └── YYYY-MM-DD.md
```

### 3.2 Bootstrap文件注入

**首次会话时自动注入：**
- 空文件会被跳过
- 大文件会被截断并标记
- 缺失文件会注入"missing file"标记

**首次运行：**
- `BOOTSTRAP.md`仅在全新工作空间创建
- 完成仪式后删除
- 可通过`agent.skipBootstrap: true`禁用

### 3.3 内置工具

**核心工具（始终可用）：**
- read/exec/edit/write
- 受工具策略控制

**可选工具：**
- `apply_patch`：通过`tools.exec.applyPatch`启用

### 3.4 技能系统

**加载位置（优先级从高到低）：**
1. 工作空间：`<workspace>/skills`
2. 管理目录：`~/.openclaw/skills`
3. 内置：随安装提供

**配置控制：**
- 通过`skills`配置项控制

---

## 四、会话管理

### 4.1 会话存储

**位置：**
```
~/.openclaw/agents/<agentId>/sessions/<SessionId>.jsonl
```

**特点：**
- JSONL格式
- 稳定的会话ID
- 不读取旧的Pi/Tau会话

### 4.2 流式处理

**队列模式：**
- `steer`：在工具调用后检查队列，注入消息
- `followup`/`collect`：等待当前回合结束

**块流式传输：**
- 默认关闭
- 通过`agents.defaults.blockStreamingDefault`控制
- 可调整块大小和边界

---

## 五、模型系统

### 5.1 模型选择顺序

```
1. 主模型 (agents.defaults.model.primary)
2. 备用模型 (agents.defaults.model.fallbacks)
3. 提供商认证故障转移（在提供商内部）
```

### 5.2 配置示例

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-sonnet-4-5",
        fallbacks: ["openai/gpt-4o", "google/gemini-pro"]
      },
      models: {
        "anthropic/claude-sonnet-4-5": { alias: "Sonnet" },
        "openai/gpt-4o": { alias: "GPT-4o" }
      }
    }
  }
}
```

### 5.3 CLI命令

```bash
# 查看模型状态
openclaw models status

# 设置主模型
openclaw models set anthropic/claude-sonnet-4-5

# 管理备用模型
openclaw models fallbacks add openai/gpt-4o
openclaw models fallbacks list

# 扫描免费模型
openclaw models scan
```

---

## 六、记忆系统

### 6.1 记忆文件

**两层结构：**
1. **MEMORY.md**（可选）
   - 精选的长期记忆
   - 仅在主会话中加载
   - 不在群聊中加载

2. **memory/YYYY-MM-DD.md**
   - 每日日志（追加模式）
   - 会话启动时读取今天和昨天

### 6.2 记忆工具

**两个Agent工具：**
1. `memory_search` - 语义搜索
2. `memory_get` - 读取特定文件

**特性：**
- 基于Markdown
- 向量索引支持
- 混合搜索（BM25 + 向量）

### 6.3 自动记忆刷新

**触发条件：**
- 会话接近自动压缩时
- 提醒模型写入持久记忆

**配置：**
```json5
{
  agents: {
    defaults: {
      compaction: {
        memoryFlush: {
          enabled: true,
          softThresholdTokens: 4000,
          prompt: "Write lasting notes to memory/YYYY-MM-DD.md"
        }
      }
    }
  }
}
```

### 6.4 向量记忆搜索

**默认启用**

**提供商选择顺序：**
1. `local` - 如果配置了本地模型
2. `openai` - 如果有OpenAI密钥
3. `gemini` - 如果有Gemini密钥
4. `voyage` - 如果有Voyage密钥
5. `mistral` - 如果有Mistral密钥
6. 否则禁用

**配置示例：**
```json5
{
  agents: {
    defaults: {
      memorySearch: {
        provider: "openai",
        model: "text-embedding-3-small",
        fallback: "gemini"
      }
    }
  }
}
```

### 6.5 混合搜索

**结合两种检索信号：**
1. **向量相似度** - 语义匹配
2. **BM25关键词** - 精确匹配

**优势：**
- 语义查询："Mac Studio网关主机" vs "运行gateway的机器"
- 精确查询：ID、代码符号、错误字符串

**配置：**
```json5
{
  memorySearch: {
    query: {
      hybrid: {
        enabled: true,
        vectorWeight: 0.7,
        textWeight: 0.3,
        mmr: { enabled: true, lambda: 0.7 },
        temporalDecay: { enabled: true, halfLifeDays: 30 }
      }
    }
  }
}
```

---

## 七、安全与权限

### 7.1 配对机制

**设备身份：**
- 所有WebSocket客户端包含设备ID
- 新设备需要配对批准
- Gateway颁发设备令牌

**本地信任：**
- 本地连接（回环）可自动批准
- 非本地连接需要明确批准
- 必须签名`connect.challenge` nonce

### 7.2 沙箱策略

**三种权限级别：**
1. **sandbox** - 完全隔离
2. **tool-policy** - 工具策略控制
3. **elevated** - 提升权限

**配置：**
- 通过`tools.exec`控制
- `apply_patch`需要显式启用

---

## 八、最佳实践

### 8.1 配置建议

**最小配置：**
```json5
{
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace"
    }
  },
  channels: {
    whatsapp: {
      allowFrom: ["+1234567890"]  // 强烈推荐
    }
  }
}
```

**推荐配置：**
```json5
{
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      model: {
        primary: "anthropic/claude-sonnet-4-5",
        fallbacks: ["openai/gpt-4o"]
      },
      memorySearch: {
        provider: "openai",
        enabled: true
      },
      compaction: {
        reserveTokensFloor: 20000,
        memoryFlush: { enabled: true }
      }
    }
  },
  gateway: {
    auth: {
      token: "your-secure-token"
    }
  }
}
```

### 8.2 性能优化

**记忆系统：**
- 启用嵌入缓存
- 使用混合搜索
- 配置合理的刷新间隔

**会话管理：**
- 设置合适的压缩阈值
- 启用自动记忆刷新

**工具策略：**
- 限制危险工具
- 使用沙箱模式

### 8.3 安全建议

**认证：**
1. 设置Gateway令牌
2. 配置允许的发件人白名单
3. 使用设备配对

**沙箱：**
1. 非必要不启用`elevated`权限
2. 限制`exec`工具的使用
3. 审计工具调用日志

**网络：**
1. 使用Tailscale或VPN
2. 如需公网访问，启用TLS
3. 限制WebSocket端口访问

---

## 九、故障排查

### 9.1 常见问题

**模型不可用：**
```bash
# 检查模型状态
openclaw models status

# 检查认证
openclaw models status --check
```

**记忆搜索失败：**
```bash
# 检查记忆配置
# 查看Gateway日志
openclaw gateway logs
```

**连接问题：**
```bash
# 健康检查
openclaw gateway health

# 检查配对状态
openclaw devices list
```

### 9.2 日志查看

```bash
# Gateway日志
openclaw gateway logs

# 实时日志
tail -f ~/.openclaw/logs/gateway.log
```

---

## 十、扩展阅读

### 10.1 官方文档

- [Gateway协议](/gateway/protocol)
- [配对机制](/channels/pairing)
- [安全配置](/gateway/security)
- [会话管理](/reference/session-management-compaction)

### 10.2 相关主题

- [Agent工作空间](/concepts/agent-workspace)
- [模型故障转移](/concepts/model-failover)
- [多Agent协作](/concepts/multi-agent)
- [通道配置](/channels/)

---

*更新时间：2026-03-01*
*版本：1.0*
