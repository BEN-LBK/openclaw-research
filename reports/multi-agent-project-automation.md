# 多智能体AI编程系统：项目自动化构建完整指南

## 一、核心概念

### 1.1 什么是多智能体编程系统

多智能体系统通过**协作式AI角色分工**实现复杂项目的自动化构建：

```
┌─────────────┐
│   用户需求   │
└──────┬──────┘
       │
┌──────▼────────────────────────────┐
│         Orchestrator (协调者)      │
│    任务分解、调度、进度监控         │
└──────┬────────────────────────────┘
       │
   ┌───┴────┬─────────┬──────────┐
   │        │         │          │
┌──▼──┐  ┌─▼───┐  ┌──▼───┐  ┌──▼────┐
│Architect│ │Coder│  │Tester│  │Reviewer│
│架构师  │ │程序员│ │测试员│  │审核员  │
└─────┘  └─────┘  └──────┘  └───────┘
```

### 1.2 关键特性对比

| 特性 | 单Agent | 多Agent |
|------|---------|---------|
| 任务复杂度 | 中等 | 极高 |
| 角色专业化 | 通用 | 专业化 |
| 并行执行 | 有限 | 完全支持 |
| 错误隔离 | 全局影响 | 局部影响 |
| 可扩展性 | 受限 | 灵活 |

---

## 二、主流框架对比

### 2.1 AutoGen (Microsoft)

**官方资源：**
- GitHub: `github.com/microsoft/autogen`
- 文档: `microsoft.github.io/autogen/`

**核心架构：**
```python
from autogen import AssistantAgent, UserProxyAgent, GroupChat

# 1. 定义角色
architect = AssistantAgent(
    name="Architect",
    system_message="你是软件架构师，负责设计系统架构和技术选型",
    llm_config={"model": "gpt-4"}
)

coder = AssistantAgent(
    name="Coder",
    system_message="你是高级程序员，负责实现具体功能",
    llm_config={"model": "gpt-4"}
)

tester = AssistantAgent(
    name="Tester",
    system_message="你是QA工程师，负责编写测试和验证功能",
    llm_config={"model": "gpt-4"}
)

reviewer = AssistantAgent(
    name="Reviewer",
    system_message="你是代码审查专家，负责代码质量检查",
    llm_config={"model": "gpt-4"}
)

# 2. 创建协作组
groupchat = GroupChat(
    agents=[architect, coder, tester, reviewer],
    messages=[],
    max_round=50
)

# 3. 启动协作
manager = GroupChatManager(groupchat=groupchat)
user_proxy.initiate_chat(
    manager,
    message="开发一个用户认证系统，包括注册、登录、密码重置功能"
)
```

**对话流程示例：**
```
User: 开发用户认证系统

Architect: 我建议采用以下架构：
- 后端: FastAPI + JWT
- 数据库: PostgreSQL
- 前端: React
需要实现：注册、登录、密码重置API

Coder: 好的，我先实现注册API：
[生成代码...]

Tester: 我来编写测试用例：
[生成测试代码...]

Reviewer: 代码审查发现：
1. 缺少输入验证
2. 密码需要加盐
请Coder修复

Coder: 已修复：
[更新代码...]

Tester: 测试通过✓

[循环直到所有功能完成]
```

### 2.2 CrewAI

**官方资源：**
- GitHub: `github.com/joaomdmoura/crewAI`
- 文档: `docs.crewai.com/`

**核心架构：**
```python
from crewai import Agent, Task, Crew, Process

# 1. 定义Agent
architect = Agent(
    role='软件架构师',
    goal='设计可扩展的系统架构',
    backstory='资深架构师，擅长微服务设计',
    allow_delegation=False
)

developer = Agent(
    role='全栈开发者',
    goal='高质量实现功能代码',
    backstory='10年开发经验，代码洁癖',
    allow_delegation=True
)

qa_engineer = Agent(
    role='QA工程师',
    goal='确保代码质量100%',
    backstory='测试驱动开发专家',
    allow_delegation=False
)

# 2. 定义任务
design_task = Task(
    description='设计电商购物车系统架构',
    agent=architect,
    expected_output='架构设计文档'
)

implement_task = Task(
    description='实现购物车核心功能',
    agent=developer,
    context=[design_task],
    expected_output='可运行的代码'
)

test_task = Task(
    description='编写单元测试和集成测试',
    agent=qa_engineer,
    context=[implement_task],
    expected_output='测试覆盖率>80%'
)

# 3. 组建团队
crew = Crew(
    agents=[architect, developer, qa_engineer],
    tasks=[design_task, implement_task, test_task],
    process=Process.sequential  # 或 hierarchical
)

# 4. 执行
result = crew.kickoff()
```

**Process模式：**
- **Sequential**: 按顺序执行任务
- **Hierarchical**: 管理者-工人模式

### 2.3 LangGraph

**官方资源：**
- GitHub: `github.com/langchain-ai/langgraph`
- 文档: `langchain-ai.github.io/langgraph/`

**状态图架构：**
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class ProjectState(TypedDict):
    requirements: str
    design: str
    code: str
    tests: str
    review_comments: list
    iteration: int

# 定义节点函数
def plan(state: ProjectState):
    requirements = state["requirements"]
    design = architect_agent.plan(requirements)
    return {"design": design}

def implement(state: ProjectState):
    code = coder_agent.implement(state["design"])
    return {"code": code}

def test(state: ProjectState):
    tests = tester_agent.test(state["code"])
    return {"tests": tests}

def review(state: ProjectState):
    comments = reviewer_agent.review(state["code"])
    return {"review_comments": comments}

def should_refactor(state: ProjectState):
    if state["review_comments"]:
        return "refactor"
    return "complete"

# 构建图
workflow = StateGraph(ProjectState)

workflow.add_node("plan", plan)
workflow.add_node("implement", implement)
workflow.add_node("test", test)
workflow.add_node("review", review)
workflow.add_node("refactor", implement)

workflow.set_entry_point("plan")
workflow.add_edge("plan", "implement")
workflow.add_edge("implement", "test")
workflow.add_edge("test", "review")
workflow.add_conditional_edges(
    "review",
    should_refactor,
    {
        "refactor": "refactor",
        "complete": END
    }
)

# 执行
app = workflow.compile()
result = app.invoke({
    "requirements": "开发REST API",
    "iteration": 0
})
```

### 2.4 MetaGPT

**官方资源：**
- GitHub: `github.com/geekan/MetaGPT`
- 文档: `docs.deepwisdom.ai/main/zh/`

**特色：软件公司模拟**
```python
from metagpt.roles import (
    ProductManager,
    Architect,
    ProjectManager,
    Engineer,
    QaEngineer
)
from metagpt.team import Team
from metagpt.software_company import SoftwareCompany

# 启动软件公司
company = SoftwareCompany()
company.hire([
    ProductManager(),
    Architect(),
    ProjectManager(),
    Engineer(),
    QaEngineer()
])

# 启动项目
company.run_project("开发一个类似Notion的协作工具")
```

**自动生成文档：**
```
output/
├── docs/
│   ├── PRD.md              # 产品需求文档
│   ├── system_design.md    # 系统设计
│   └── api_spec.md         # API规范
├── src/
│   ├── backend/
│   └── frontend/
└── tests/
```

---

## 三、完整项目自动化Demo

### 3.1 场景：自动开发Todo API

**项目结构：**
```
todo-api-project/
├── agents/
│   ├── orchestrator.py    # 总调度
│   ├── architect.py       # 架构师
│   ├── coder.py          # 程序员
│   ├── tester.py         # 测试员
│   └── reviewer.py       # 审核员
├── workflow.py           # 工作流定义
├── config.yaml          # 配置文件
└── main.py              # 入口
```

**config.yaml:**
```yaml
project:
  name: "Todo REST API"
  description: "CRUD API with authentication"
  
agents:
  orchestrator:
    model: "gpt-4"
    max_iterations: 100
    
  architect:
    model: "gpt-4"
    tools: ["web_search", "read_file"]
    
  coder:
    model: "gpt-4"
    tools: ["write_file", "execute_code"]
    
  tester:
    model: "gpt-3.5-turbo"
    tools: ["execute_code", "read_file"]
    
  reviewer:
    model: "gpt-4"
    focus: ["security", "performance", "readability"]

workflow:
  phases:
    - name: "planning"
      agent: "architect"
      outputs: ["design.md", "api_spec.yaml"]
      
    - name: "implementation"
      agent: "coder"
      depends_on: ["planning"]
      outputs: ["src/"]
      
    - name: "testing"
      agent: "tester"
      depends_on: ["implementation"]
      outputs: ["tests/", "coverage_report.html"]
      
    - name: "review"
      agent: "reviewer"
      depends_on: ["testing"]
      gate: true  # 必须通过才能继续
      
  iteration:
    max_count: 5
    trigger: "review_failed"
```

**workflow.py:**
```python
import yaml
from typing import Dict, List
from pathlib import Path

class ProjectWorkflow:
    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        
        self.agents = self._init_agents()
        self.state = {
            "current_phase": None,
            "iterations": 0,
            "artifacts": {},
            "errors": []
        }
    
    def run(self, requirement: str):
        """主循环：自动完成整个项目"""
        print(f"🚀 启动项目: {self.config['project']['name']}")
        
        # 阶段1：规划
        design = self._run_phase("planning", requirement)
        
        # 阶段2-N：实现-测试-审核循环
        while True:
            # 实现
            code = self._run_phase("implementation", design)
            
            # 测试
            test_result = self._run_phase("testing", code)
            
            # 审核
            review = self._run_phase("review", {
                "code": code,
                "tests": test_result
            })
            
            # 检查是否通过
            if review["passed"]:
                print("✅ 项目完成!")
                break
            
            # 检查迭代次数
            self.state["iterations"] += 1
            if self.state["iterations"] >= self.config["workflow"]["iteration"]["max_count"]:
                print("⚠️ 达到最大迭代次数，请求人工介入")
                self._request_human_help(review["issues"])
                break
            
            # 继续修复
            print(f"🔄 开始第 {self.state['iterations'] + 1} 轮修复")
    
    def _run_phase(self, phase_name: str, input_data):
        """执行单个阶段"""
        phase_config = self._get_phase_config(phase_name)
        agent = self.agents[phase_config["agent"]]
        
        print(f"\n📍 执行阶段: {phase_name}")
        
        # Agent执行
        result = agent.execute(
            task=input_data,
            tools=phase_config.get("tools", [])
        )
        
        # 保存产物
        for output in phase_config.get("outputs", []):
            self.state["artifacts"][output] = result.get(output)
        
        return result
    
    def _init_agents(self):
        """初始化所有Agent"""
        return {
            "architect": ArchitectAgent(self.config["agents"]["architect"]),
            "coder": CoderAgent(self.config["agents"]["coder"]),
            "tester": TesterAgent(self.config["agents"]["tester"]),
            "reviewer": ReviewerAgent(self.config["agents"]["reviewer"])
        }
```

**agents/coder.py:**
```python
class CoderAgent:
    def __init__(self, config):
        self.model = config["model"]
        self.tools = config.get("tools", [])
    
    def execute(self, task, tools):
        """实现代码"""
        # 1. 理解设计文档
        design = self._read_design(task)
        
        # 2. 生成代码结构
        structure = self._plan_structure(design)
        
        # 3. 逐文件实现
        for file_path, spec in structure.items():
            code = self._generate_code(spec)
            self._write_file(file_path, code)
        
        # 4. 运行检查
        self._run_linter()
        
        return {
            "src/": structure,
            "status": "implemented"
        }
    
    def _generate_code(self, spec):
        """使用LLM生成代码"""
        prompt = f"""
        根据以下规范生成Python代码：
        
        文件: {spec['file']}
        功能: {spec['description']}
        依赖: {spec['dependencies']}
        
        要求：
        1. 遵循PEP8规范
        2. 添加类型注解
        3. 包含docstring
        """
        return self._call_llm(prompt)
```

### 3.2 执行过程示例

```
$ python main.py "开发Todo REST API"

🚀 启动项目: Todo REST API

📍 执行阶段: planning
[Architect] 分析需求...
[Architect] 设计API规范...
[Architect] 选择技术栈: FastAPI + SQLAlchemy + PostgreSQL
✅ 输出: design.md, api_spec.yaml

📍 执行阶段: implementation
[Coder] 读取设计文档...
[Coder] 创建项目结构...
[Coder] 生成 models.py ✓
[Coder] 生成 main.py ✓
[Coder] 生成 routes.py ✓
[Coder] 运行linter... 通过 ✓

📍 执行阶段: testing
[Tester] 分析代码覆盖需求...
[Tester] 生成单元测试...
[Tester] 生成集成测试...
[Tester] 运行测试...
  - test_create_todo: ✓
  - test_get_todo: ✓
  - test_update_todo: ✓
  - test_delete_todo: ✗ (失败)
  
  覆盖率: 72%

📍 执行阶段: review
[Reviewer] 代码审查中...
❌ 发现问题:
  1. 缺少输入验证 (security)
  2. 未处理并发访问 (performance)
  3. test_delete_todo失败需要修复

🔄 开始第 2 轮修复

📍 执行阶段: implementation
[Coder] 修复输入验证...
[Coder] 添加并发锁...
[Coder] 修复删除逻辑...

📍 执行阶段: testing
[Tester] 运行测试...
  - 所有测试通过 ✓
  覆盖率: 89%

📍 执行阶段: review
[Reviewer] 代码审查中...
✅ 审核通过!

✅ 项目完成!

📁 生成的文件:
  - src/models.py
  - src/main.py
  - src/routes.py
  - src/schemas.py
  - tests/test_api.py
  - tests/test_models.py
  - docs/api_spec.yaml
  - README.md

⏱️ 总耗时: 12分钟
🔄 迭代次数: 2
📊 测试覆盖率: 89%
```

---

## 四、Google Cloud Code 集成

### 4.1 Cloud Code + Gemini

**配置示例：**
```json
// .cloudcode/config.json
{
  "ai": {
    "provider": "gemini",
    "model": "gemini-1.5-pro",
    "features": {
      "multiFileEdit": true,
      "codebaseIndexing": true,
      "testGeneration": true
    }
  },
  "automation": {
    "enabled": true,
    "workflow": "agile-sprint",
    "agents": ["architect", "developer", "tester"]
  }
}
```

### 4.2 VS Code扩展配置

```json
// settings.json
{
  "cloudcode.ai.enabled": true,
  "cloudcode.ai.multiAgent": true,
  "cloudcode.ai.maxIterations": 20,
  "cloudcode.ai.autoTest": true,
  "cloudcode.ai.autoReview": true,
  
  "cloudcode.agents": {
    "architect": {
      "role": "Design system architecture",
      "model": "gemini-1.5-pro"
    },
    "developer": {
      "role": "Implement features",
      "model": "gemini-1.5-flash"
    },
    "reviewer": {
      "role": "Code review and quality check",
      "model": "gemini-1.5-pro"
    }
  }
}
```

---

## 五、实际项目案例

### 案例1：MetaGPT自动开发游戏

**GitHub:** `github.com/geekan/MetaGPT/tree/main/examples`

```bash
# 一行命令生成完整游戏
metagpt "开发一个贪吃蛇游戏，包含分数系统、难度递增、音效"
```

**自动生成：**
```
snake_game/
├── docs/
│   └── game_design.md      # 游戏设计文档
├── src/
│   ├── main.py            # 游戏主逻辑
│   ├── snake.py           # 蛇类
│   ├── food.py            # 食物类
│   ├── audio.py           # 音效管理
│   └── ui.py              # 界面渲染
├── assets/
│   └── sounds/            # 音效文件
├── tests/
│   └── test_game.py       # 测试
└── README.md
```

### 案例2：AutoGen开发Web应用

**GitHub:** `github.com/microsoft/autogen/tree/main/samples`

```python
# 多Agent协作开发Flask应用
from autogen import GroupChat

task = """
开发一个博客系统，包含：
1. 用户注册/登录
2. 文章CRUD
3. 评论功能
4. Markdown支持
5. 搜索功能
"""

# 5个Agent自动协作完成
agents = [pm, architect, backend_dev, frontend_dev, tester]
groupchat = GroupChat(agents=agents)
manager.initiate_chat(task)
```

### 案例3：GPT-Engineer完整项目

**GitHub:** `github.com/gpt-engineer-org/gpt-engineer`

```bash
# 交互式需求描述
$ gpt-engineer

What do you want to build?
> 一个在线代码编辑器，支持多种语言，可以运行代码并显示输出

[AI分析需求...]
[生成文件结构...]
[实现核心功能...]
[添加测试...]
[完成!]

Generated files:
  - package.json
  - src/App.tsx
  - src/components/Editor.tsx
  - src/components/Output.tsx
  - src/utils/codeRunner.ts
  - tests/App.test.tsx
```

---

## 六、配置教程

### 6.1 AutoGen快速开始

```bash
# 1. 安装
pip install pyautogen

# 2. 配置API
export OPENAI_API_KEY="your-key"

# 3. 创建脚本
cat > team_coding.py << 'EOF'
from autogen import AssistantAgent, UserProxyAgent, GroupChat

# 创建Agent团队
agents = [
    AssistantAgent("Architect", system_message="架构师"),
    AssistantAgent("Developer", system_message="开发者"),
    AssistantAgent("Tester", system_message="测试员")
]

# 创建协作组
groupchat = GroupChat(agents=agents, messages=[])

# 执行任务
user = UserProxyAgent("User")
user.initiate_chat(
    GroupChatManager(groupchat),
    message="开发一个简单的计算器"
)
EOF

# 4. 运行
python team_coding.py
```

### 6.2 CrewAI项目模板

```bash
# 1. 安装
pip install crewai

# 2. 创建项目
crewai create my-project

# 3. 定义Agent (agents.yaml)
architect:
  role: 软件架构师
  goal: 设计系统架构
  backstory: 10年架构经验

developer:
  role: 全栈开发者
  goal: 实现功能
  backstory: 精通多种语言

# 4. 定义任务 (tasks.yaml)
design:
  description: 设计系统架构
  agent: architect
  
implement:
  description: 实现核心功能
  agent: developer
  depends_on: [design]

# 5. 运行
crewai run "开发用户管理系统"
```

### 6.3 LangGraph工作流

```bash
# 1. 安装
pip install langgraph langchain-openai

# 2. 定义工作流
cat > workflow.py << 'EOF'
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

def architect_node(state):
    return {"design": llm.invoke(state["req"])}

def coder_node(state):
    return {"code": llm.invoke(state["design"])}

def tester_node(state):
    return {"tests": llm.invoke(state["code"])}

# 构建图
graph = StateGraph(dict)
graph.add_node("architect", architect_node)
graph.add_node("coder", coder_node)
graph.add_node("tester", tester_node)

graph.add_edge("architect", "coder")
graph.add_edge("coder", "tester")

app = graph.compile()
EOF

# 3. 执行
python -c "from workflow import app; print(app.invoke({'req': '开发API'}))"
```

---

## 七、最佳实践

### 7.1 Agent设计原则

| 原则 | 说明 |
|------|------|
| **单一职责** | 每个Agent专注一个领域 |
| **明确边界** | 定义清晰的输入输出 |
| **可测试性** | Agent行为可独立验证 |
| **容错性** | 单个Agent失败不影响整体 |

### 7.2 任务分解策略

```python
def decompose_project(requirement):
    """将大项目分解为可执行的小任务"""
    
    # 1. 识别主要模块
    modules = identify_modules(requirement)
    
    # 2. 每个模块分解为任务
    tasks = []
    for module in modules:
        tasks.extend([
            Task(f"设计{module}", agent="architect"),
            Task(f"实现{module}", agent="developer"),
            Task(f"测试{module}", agent="tester"),
            Task(f"审核{module}", agent="reviewer")
        ])
    
    # 3. 建立依赖关系
    return build_dependency_graph(tasks)
```

### 7.3 质量保证机制

```python
class QualityGate:
    """质量门：确保每个阶段输出质量"""
    
    def check(self, phase, output):
        checks = {
            "planning": [
                self._check_design_completeness,
                self._check_feasibility
            ],
            "implementation": [
                self._check_code_syntax,
                self._check_code_style,
                self._check_security_issues
            ],
            "testing": [
                self._check_test_coverage,
                self._check_all_tests_pass
            ]
        }
        
        for check in checks[phase]:
            if not check(output):
                return False
        return True
```

### 7.4 监控与日志

```python
import logging

class AgentMonitor:
    """监控Agent执行过程"""
    
    def __init__(self):
        self.logger = logging.getLogger("AgentMonitor")
        self.metrics = {
            "iterations": 0,
            "tokens_used": 0,
            "files_created": 0,
            "tests_passed": 0
        }
    
    def log_agent_action(self, agent, action, result):
        self.logger.info(f"[{agent}] {action} -> {result}")
        self.metrics["iterations"] += 1
        
    def generate_report(self):
        return f"""
        项目执行报告
        =============
        总迭代次数: {self.metrics['iterations']}
        Token使用: {self.metrics['tokens_used']}
        创建文件: {self.metrics['files_created']}
        测试通过: {self.metrics['tests_passed']}
        """
```

---

## 八、资源汇总

### 8.1 GitHub仓库推荐

| 项目 | Stars | 描述 |
|------|-------|------|
| **microsoft/autogen** | 30k+ | 微软多Agent框架 |
| **joaomdmoura/crewAI** | 20k+ | 角色扮演式Agent团队 |
| **langchain-ai/langgraph** | 15k+ | 状态图工作流 |
| **geekan/MetaGPT** | 40k+ | 软件公司模拟 |
| **OpenDevin/OpenDevin** | 30k+ | 自主软件开发 |
| **princeton-nlp/SWE-agent** | 10k+ | GitHub Issue修复 |
| **e2b-dev/code-interpreter** | 5k+ | 代码执行沙箱 |

### 8.2 教程与文档

**官方文档：**
- AutoGen: `microsoft.github.io/autogen/`
- CrewAI: `docs.crewai.com/`
- LangGraph: `langchain-ai.github.io/langgraph/`
- MetaGPT: `docs.deepwisdom.ai/`

**教程系列：**
- `deeplearning.ai/short-courses/` - AI Agent课程
- `langchain.com/learn` - LangChain官方教程
- `youtube.com/@autogen` - AutoGen视频教程

### 8.3 示例项目

```bash
# AutoGen示例
git clone https://github.com/microsoft/autogen
cd autogen/samples

# CrewAI模板
git clone https://github.com/joaomdmoura/crewAI-examples

# MetaGPT示例
git clone https://github.com/geekan/MetaGPT
cd MetaGPT/examples
```

---

## 九、进阶主题

### 9.1 人机协作模式

```python
class HumanInTheLoop:
    """人工介入关键决策点"""
    
    DECISION_POINTS = [
        "architecture_choice",
        "security_design",
        "deployment_strategy"
    ]
    
    def should_ask_human(self, decision_type):
        return decision_type in self.DECISION_POINTS
    
    def ask_human(self, question, options):
        # 通过CLI或Web界面询问
        return human_input(question, options)
```

### 9.2 持续集成

```yaml
# .github/workflows/ai-development.yml
name: AI-Assisted Development

on:
  issue:
    types: [opened, labeled]

jobs:
  auto-implement:
    if: contains(github.event.issue.labels, 'ai-implement')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Multi-Agent System
        run: |
          python -m agents.orchestrator \
            --issue ${{ github.event.issue.number }} \
            --repo ${{ github.repository }}
      
      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          title: "AI: ${{ github.event.issue.title }}"
          body: "Automated implementation by AI agents"
```

### 9.3 性能优化

```python
# 并行执行多个Agent
import asyncio

async def parallel_development(modules):
    """并行开发多个模块"""
    tasks = [
        develop_module(module)
        for module in modules
    ]
    return await asyncio.gather(*tasks)

# 缓存共享知识
class SharedKnowledge:
    """Agent间共享的知识库"""
    def __init__(self):
        self.cache = {}
    
    def get(self, key):
        return self.cache.get(key)
    
    def set(self, key, value):
        self.cache[key] = value
```

---

## 十、总结

### 核心要点

1. **框架选择**
   - AutoGen：微软生态，文档完善
   - CrewAI：角色扮演，易于理解
   - LangGraph：灵活可控，适合复杂流程
   - MetaGPT：一键生成，快速原型

2. **实施建议**
   - 从小项目开始验证
   - 定义清晰的Agent角色
   - 设置合理的质量门
   - 保留人工监督机制

3. **成功关键**
   - 任务分解粒度适中
   - Agent间通信清晰
   - 错误处理完善
   - 持续监控优化

### 下一步行动

```bash
# 1. 选择框架
pip install pyautogen  # 或 crewai

# 2. 运行示例
git clone https://github.com/microsoft/autogen
python autogen/samples/agent_chat.py

# 3. 自定义开发
# 参考本报告的Demo代码
```

---

*报告版本: v1.0*
*更新时间: 2026-02-28*
*研究分析师: OpenClaw Research Agent*
