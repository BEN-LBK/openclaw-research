# OpenClaw 通道配置详解

## 一、通道概述

OpenClaw支持多种消息通道，通过统一的Gateway管理：

- WhatsApp (生产就绪)
- Telegram Bot (生产就绪)
- Discord
- Slack
- Signal
- iMessage
- Feishu (飞书)
- WebChat

---

## 二、WhatsApp 配置

### 2.1 快速设置

```bash
# 1. 配置访问策略
# 在 openclaw.json 中配置

# 2. 链接WhatsApp (扫码)
openclaw channels login --channel whatsapp

# 3. 启动Gateway
openclaw gateway

# 4. 批准首次配对请求
openclaw pairing list whatsapp
openclaw pairing approve whatsapp <CODE>
```

### 2.2 配置示例

```json5
{
  channels: {
    whatsapp: {
      enabled: true,
      dmPolicy: "pairing",  // 或 "allowlist"
      allowFrom: ["+15551234567"],
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"]
    }
  }
}
```

### 2.3 部署模式

**推荐：专用号码**
- 为OpenClaw使用独立的WhatsApp号码
- 清晰的DM白名单和路由边界
- 降低自我聊天混淆

**备选：个人号码**
- 支持但需要额外配置
- 需要处理自我聊天情况

### 2.4 DM策略

**配对模式（pairing）**
- 默认策略
- 未知发件人需要配对批准
- 配对码1小时后过期
- 每个通道最多3个待处理请求

**白名单模式（allowlist）**
- 仅允许列表中的号码
- 更安全但需要手动维护

### 2.5 群组配置

```json5
{
  channels: {
    whatsapp: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["+15551234567"],
      groups: {
        "*": {
          requireMention: true,  // 需要@提及
          replyInThread: false
        }
      }
    }
  }
}
```

---

## 三、Telegram 配置

### 3.1 快速设置

```bash
# 1. 创建Bot (在BotFather中)
# 打开Telegram，与 @BotFather 对话
# 运行 /newbot，保存token

# 2. 配置token
# 在 openclaw.json 中配置

# 3. 启动Gateway
openclaw gateway

# 4. 批准首次DM
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

### 3.2 配置示例

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",  // 或使用 TELEGRAM_BOT_TOKEN 环境变量
      dmPolicy: "pairing",
      groups: {
        "*": {
          requireMention: true
        }
      }
    }
  }
}
```

### 3.3 Telegram Bot设置

**隐私模式**
- 默认启用，限制群组消息接收
- 如需接收所有群组消息：
  - 通过`/setprivacy`禁用隐私模式
  - 或将Bot设为群组管理员

**群组权限**
- 在Telegram群组设置中控制
- 管理员Bot接收所有群组消息

**有用的BotFather命令**
- `/setjoingroups` - 允许/拒绝群组添加
- `/setprivacy` - 群组可见性行为

### 3.4 Webhook模式（可选）

默认使用长轮询，可选Webhook模式：

```json5
{
  channels: {
    telegram: {
      webhook: {
        enabled: true,
        url: "https://your-domain.com/webhook/telegram",
        port: 8443
      }
    }
  }
}
```

---

## 四、Discord 配置

### 4.1 基本配置

```json5
{
  channels: {
    discord: {
      enabled: true,
      botToken: "your-bot-token",
      dmPolicy: "pairing",
      guilds: {
        "*": {
          requireMention: true,
          replyInThread: true
        }
      }
    }
  }
}
```

### 4.2 权限设置

需要的Discord权限：
- 发送消息
- 读取消息历史
- 添加反应
- 使用斜杠命令

---

## 五、Slack 配置

### 5.1 基本配置

```json5
{
  channels: {
    slack: {
      enabled: true,
      botToken: "xoxb-your-token",
      appToken: "xapp-your-token",
      dmPolicy: "pairing"
    }
  }
}
```

### 5.2 权限范围

需要的Slack权限：
- `chat:write`
- `channels:history`
- `groups:history`
- `im:history`
- `mpim:history`

---

## 六、Signal 配置

### 6.1 基本配置

```json5
{
  channels: {
    signal: {
      enabled: true,
      phoneNumber: "+15551234567",
      dmPolicy: "allowlist",
      allowFrom: ["+15559876543"]
    }
  }
}
```

---

## 七、飞书配置

### 7.1 基本配置

```json5
{
  channels: {
    feishu: {
      enabled: true,
      appId: "cli_xxx",
      appSecret: "xxx",
      dmPolicy: "pairing"
    }
  }
}
```

### 7.2 权限配置

需要的飞书权限：
- 接收消息
- 发送消息
- 获取用户信息

---

## 八、WebChat 配置

### 8.1 基本配置

```json5
{
  channels: {
    webchat: {
      enabled: true,
      bind: "0.0.0.0:18790",
      auth: {
        required: true,
        token: "your-token"
      }
    }
  }
}
```

### 8.2 访问控制

**建议：**
- 启用认证
- 使用HTTPS
- 限制访问IP

---

## 九、通用配置选项

### 9.1 DM策略

**pairing（配对）**
- 需要批准新发件人
- 适合公共Bot

**allowlist（白名单）**
- 仅允许列表中的发件人
- 适合私人使用

**deny（拒绝）**
- 拒绝所有DM
- 仅处理群组消息

### 9.2 群组策略

```json5
{
  groups: {
    "*": {
      requireMention: true,     // 需要@提及
      replyInThread: false,     // 线程内回复
      allowBotMention: false    // 允许Bot提及
    },
    "specific-group-id": {
      requireMention: false     // 特定群组例外
    }
  }
}
```

### 9.3 消息格式化

```json5
{
  channels: {
    whatsapp: {
      formatting: {
        maxLength: 4096,        // 最大消息长度
        splitMessages: true,    // 分割长消息
        preserveFormatting: true
      }
    }
  }
}
```

---

## 十、故障排查

### 10.1 常见问题

**WhatsApp无法连接**
```bash
# 重新登录
openclaw channels logout --channel whatsapp
openclaw channels login --channel whatsapp
```

**Telegram Bot无响应**
```bash
# 检查token
openclaw channels test telegram

# 查看日志
openclaw gateway logs | grep telegram
```

**群组消息不触发**
- 检查`requireMention`设置
- 确认Bot权限
- 验证群组策略

### 10.2 日志查看

```bash
# 实时日志
openclaw gateway logs -f

# 特定通道日志
openclaw gateway logs | grep whatsapp
```

---

## 十一、最佳实践

### 11.1 安全建议

1. **使用白名单**
   - 限制允许的发件人
   - 定期审查白名单

2. **启用配对**
   - 对未知发件人要求批准
   - 监控配对请求

3. **权限最小化**
   - 仅授予必需的权限
   - 定期审查Bot权限

### 11.2 性能优化

1. **消息队列**
   - 使用适当的队列模式
   - 调整并发限制

2. **缓存策略**
   - 启用用户信息缓存
   - 配置合理的过期时间

3. **错误处理**
   - 设置重试策略
   - 监控失败率

### 11.3 运维建议

1. **监控**
   - 监控连接状态
   - 设置告警

2. **备份**
   - 定期备份配置
   - 保存会话数据

3. **更新**
   - 定期更新依赖
   - 关注安全公告

---

*更新时间：2026-03-01*
*版本：1.0*
