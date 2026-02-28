# OpenClaw 工具系统与CLI参考

## 一、工具系统概述

### 1.1 内置工具

**核心工具（始终可用）：**
- `read` - 读取文件
- `write` - 写入文件
- `edit` - 编辑文件
- `exec` - 执行命令
- `process` - 管理进程

**记忆工具：**
- `memory_search` - 语义搜索记忆
- `memory_get` - 读取特定记忆文件

**可选工具：**
- `apply_patch` - 应用补丁（需显式启用）

### 1.2 工具权限

**三种权限级别：**

1. **sandbox（沙箱）**
   - 完全隔离
   - 最安全
   - 限制最多

2. **tool-policy（工具策略）**
   - 基于策略控制
   - 平衡安全和功能
   - 默认推荐

3. **elevated（提升权限）**
   - 提升权限
   - 最危险
   - 仅在必要时使用

### 1.3 配置示例

```json5
{
  tools: {
    exec: {
      enabled: true,
      sandbox: true,
      applyPatch: false,  // 需要显式启用
      approvals: {
        enabled: true,
        mode: "on-miss"  // 或 "always"
      }
    },
    browser: {
      enabled: true,
      sandbox: false
    }
  }
}
```

---

## 二、CLI命令参考

### 2.1 Gateway管理

```bash
# 启动Gateway（前台）
openclaw gateway

# 启动Gateway（守护进程）
openclaw gateway start

# 停止Gateway
openclaw gateway stop

# 重启Gateway
openclaw gateway restart

# 查看Gateway状态
openclaw gateway status

# 查看Gateway日志
openclaw gateway logs

# 健康检查
openclaw gateway health
```

### 2.2 模型管理

```bash
# 查看模型状态
openclaw models status
openclaw models list

# 设置主模型
openclaw models set anthropic/claude-sonnet-4-5

# 设置图像模型
openclaw models set-image openai/dall-e-3

# 管理备用模型
openclaw models fallbacks list
openclaw models fallbacks add openai/gpt-4o
openclaw models fallbacks remove openai/gpt-4o
openclaw models fallbacks clear

# 管理图像备用模型
openclaw models image-fallbacks list
openclaw models image-fallbacks add openai/dall-e-2

# 管理别名
openclaw models aliases list
openclaw models aliases add sonnet anthropic/claude-sonnet-4-5
openclaw models aliases remove sonnet

# 扫描免费模型
openclaw models scan
openclaw models scan --no-probe
openclaw models scan --min-params 7
openclaw models scan --set-default
```

### 2.3 通道管理

```bash
# 登录通道
openclaw channels login --channel whatsapp
openclaw channels login --channel telegram --account work

# 登出通道
openclaw channels logout --channel whatsapp

# 测试通道
openclaw channels test telegram

# 列出通道
openclaw channels list
```

### 2.4 配对管理

```bash
# 列出配对请求
openclaw pairing list whatsapp
openclaw pairing list telegram

# 批准配对
openclaw pairing approve whatsapp <CODE>
openclaw pairing approve telegram <CODE>

# 拒绝配对
openclaw pairing reject whatsapp <CODE>
```

### 2.5 设备管理

```bash
# 列出设备
openclaw devices list

# 删除设备
openclaw devices remove <device-id>
```

### 2.6 配置管理

```bash
# 编辑配置
openclaw config edit

# 查看配置
openclaw config get
openclaw config get agents.defaults.model

# 设置配置
openclaw config set agents.defaults.model.primary "anthropic/claude-sonnet-4-5"

# 查看配置模式
openclaw config schema
```

### 2.7 设置向导

```bash
# 运行设置向导
openclaw setup

# 运行入职向导
openclaw onboard
```

### 2.8 诊断

```bash
# 运行诊断
openclaw doctor

# 检查状态
openclaw status
```

### 2.9 Cron任务

```bash
# 列出cron任务
openclaw cron list

# 添加cron任务
openclaw cron add

# 运行cron任务
openclaw cron run <job-id>

# 查看任务运行历史
openclaw cron runs <job-id>
```

### 2.10 其他命令

```bash
# 查看帮助
openclaw help
openclaw gateway --help

# 查看版本
openclaw --version

# 查看文档
openclaw docs
```

---

## 三、工具使用最佳实践

### 3.1 文件操作

**读取文件：**
```python
# 读取完整文件
content = read("path/to/file")

# 读取部分内容
content = read("path/to/file", offset=10, limit=50)
```

**写入文件：**
```python
# 创建或覆盖文件
write("path/to/file", content="Hello World")

# 追加内容
write("path/to/file", content="\nNew line", mode="append")
```

**编辑文件：**
```python
# 精确替换
edit(
    path="config.json",
    oldText='"old": "value"',
    newText='"new": "value"'
)
```

### 3.2 命令执行

**基本执行：**
```python
# 执行命令
result = exec("ls -la")

# 指定工作目录
result = exec("npm install", workdir="/path/to/project")

# 设置环境变量
result = exec(
    "python script.py",
    env={"PYTHONPATH": "/custom/path"}
)
```

**后台执行：**
```python
# 后台运行
result = exec("long-running-task", background=True)

# 使用PTY（终端UI）
result = exec("vim file.txt", pty=true)
```

### 3.3 进程管理

```python
# 列出进程
processes = process(action="list")

# 查看进程日志
logs = process(action="log", sessionId="session-id")

# 向进程发送输入
process(action="write", sessionId="session-id", data="input")

# 终止进程
process(action="kill", sessionId="session-id")
```

### 3.4 记忆操作

**搜索记忆：**
```python
# 语义搜索
results = memory_search(
    query="how to configure gateway",
    maxResults=10
)

# 返回结果包含：
# - text: 片段文本
# - path: 文件路径
# - lines: 行号范围
# - score: 相关性分数
```

**读取记忆：**
```python
# 读取特定文件
content = memory_get(
    path="MEMORY.md",
    from=10,  # 可选：起始行
    lines=50   # 可选：行数
)
```

---

## 四、安全配置

### 4.1 工具策略

```json5
{
  tools: {
    exec: {
      enabled: true,
      sandbox: true,
      policy: {
        allowlist: [
          "git",
          "npm",
          "node"
        ],
        denylist: [
          "rm -rf /",
          "sudo"
        ]
      }
    },
    browser: {
      enabled: true,
      sandbox: true
    }
  }
}
```

### 4.2 审批流程

```json5
{
  tools: {
    exec: {
      approvals: {
        enabled: true,
        mode: "on-miss",  // 或 "always"
        timeout: 300000   // 5分钟
      }
    }
  }
}
```

**模式说明：**
- `on-miss`: 不在白名单中的命令需要批准
- `always`: 所有命令都需要批准

### 4.3 沙箱配置

```json5
{
  agents: {
    defaults: {
      sandbox: {
        enabled: true,
        workspaceRoot: "~/.openclaw/sandboxes",
        networkAccess: false,
        readOnlyPaths: [
          "/usr",
          "/System"
        ]
      }
    }
  }
}
```

---

## 五、性能优化

### 5.1 并发控制

```json5
{
  agents: {
    defaults: {
      concurrency: {
        maxTools: 5,          // 最大并发工具调用
        maxExec: 2,           // 最大并发exec
        timeout: 60000        // 超时时间
      }
    }
  }
}
```

### 5.2 缓存配置

```json5
{
  agents: {
    defaults: {
      cache: {
        enabled: true,
        maxSize: 1000000,     // 最大缓存大小
        ttl: 3600             // 缓存时间（秒）
      }
    }
  }
}
```

### 5.3 队列管理

```json5
{
  agents: {
    defaults: {
      queue: {
        mode: "steer",        // steer/followup/collect
        debounce: 1000,       // 防抖时间（毫秒）
        maxCapacity: 10       // 最大队列容量
      }
    }
  }
}
```

---

## 六、故障排查

### 6.1 工具调用失败

**常见原因：**
1. 权限不足
2. 沙箱限制
3. 命令不存在
4. 超时

**解决方法：**
```bash
# 检查工具配置
openclaw config get tools

# 查看日志
openclaw gateway logs | grep tool

# 运行诊断
openclaw doctor
```

### 6.2 CLI命令失败

**常见问题：**
1. Gateway未运行
2. 配置错误
3. 权限问题

**解决方法：**
```bash
# 检查Gateway状态
openclaw gateway status

# 验证配置
openclaw config get

# 运行诊断
openclaw doctor
```

---

## 七、最佳实践

### 7.1 工具使用

1. **优先使用安全工具**
   - 优先使用`read/write/edit`
   - 谨慎使用`exec`
   - 避免使用`elevated`权限

2. **错误处理**
   - 始终处理工具调用失败
   - 提供有意义的错误消息
   - 实现重试逻辑

3. **资源管理**
   - 及时关闭文件句柄
   - 限制并发操作
   - 监控资源使用

### 7.2 CLI使用

1. **配置管理**
   - 使用配置文件而非命令行参数
   - 版本控制配置
   - 定期备份

2. **日志管理**
   - 定期检查日志
   - 设置日志轮转
   - 监控关键错误

3. **安全实践**
   - 限制命令执行权限
   - 使用审批流程
   - 定期审查访问权限

---

*更新时间：2026-03-01*
*版本：1.0*
