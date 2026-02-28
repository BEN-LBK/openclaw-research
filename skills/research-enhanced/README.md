# 研究分析增强技能包

## 📦 安装指南

### 1. 安装依赖
```bash
cd /Users/ben/.openclaw/workspace-research/skills/research-enhanced
pip install -r requirements.txt
```

### 2. 验证安装
```bash
python academic-search.py
python data-analysis.py
python visualization.py
```

## 🔧 功能模块

### 📚 学术搜索 (academic-search.py)
- **arXiv搜索**: 搜索学术论文
- **Semantic Scholar**: 语义学术搜索
- **格式化输出**: Markdown/BibTeX/JSON

**使用示例：**
```python
from academic-search import search_arxiv, format_paper_list

# 搜索论文
papers = search_arxiv("multi-agent systems", max_results=10)

# 格式化为Markdown
report = format_paper_list(papers, format="markdown")
print(report)
```

### 📊 数据分析 (data-analysis.py)
- **统计分析**: 基础统计、相关性分析
- **数据清洗**: 缺失值处理、去重
- **报告生成**: 自动生成分析报告

**使用示例：**
```python
from data-analysis import DataAnalyzer

# 加载数据
analyzer = DataAnalyzer("data.csv")

# 生成分析报告
report = analyzer.generate_report("output/analysis_report.md")
print(report)
```

### 📈 可视化 (visualization.py)
- **多种图表**: 柱状图、折线图、饼图、散点图
- **对比分析**: 方法对比图表
- **趋势分析**: 时间序列可视化

**使用示例：**
```python
from visualization import Visualizer
import pandas as pd

# 创建可视化器
viz = Visualizer()

# 生成图表
data = pd.DataFrame({
    'Month': ['Jan', 'Feb', 'Mar', 'Apr'],
    'Sales': [100, 150, 120, 180]
})

path = viz.create_chart(
    data,
    chart_type='bar',
    x='Month',
    y='Sales',
    title='月度销售趋势',
    save_path='charts/sales.png'
)
```

## 🎯 应用场景

### 1. 文献调研
```bash
# 搜索相关论文
python academic-search.py "AI Agent" --max 20 --format markdown > literature_review.md
```

### 2. 数据分析报告
```bash
# 分析数据并生成报告
python data-analysis.py data.csv --output reports/analysis.md
```

### 3. 可视化生成
```bash
# 生成图表
python visualization.py --data data.csv --type bar --output charts/
```

## 📋 MCP 集成推荐

### 推荐的 MCP Servers

1. **@modelcontextprotocol/server-filesystem**
   - 文件系统访问
   - 增强文件操作能力

2. **@modelcontextprotocol/server-postgres**
   - 数据库访问
   - 数据存储和查询

3. **@modelcontextprotocol/server-brave-search**
   - 网络搜索增强
   - 学术资源搜索

4. **@modelcontextprotocol/server-puppeteer**
   - 浏览器自动化
   - 网页数据抓取

5. **@modelcontextprotocol/server-sqlite**
   - 本地数据库
   - 数据管理

### 安装 MCP Servers
```bash
# 安装 MCP CLI
npm install -g @modelcontextprotocol/cli

# 安装服务器
mcp install @modelcontextprotocol/server-filesystem
mcp install @modelcontextprotocol/server-postgres
mcp install @modelcontextprotocol/server-brave-search
```

## 🔍 ClawHub 推荐技能

基于研究分析需求，推荐从 ClawHub 安装：

1. **数据分析技能包**
   - 增强数据处理能力
   - 更多统计方法

2. **学术写作技能包**
   - 论文格式化
   - 引用管理

3. **图表生成技能包**
   - 更多图表类型
   - 交互式可视化

## 📝 使用记录

### 已完成的任务
- ✅ 创建学术搜索工具
- ✅ 创建数据分析工具
- ✅ 创建可视化工具
- ✅ 编写使用文档

### 待集成的功能
- [ ] MCP服务器集成
- [ ] ClawHub技能安装
- [ ] 自动化工作流

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 测试学术搜索
python academic-search.py

# 3. 测试数据分析
python data-analysis.py

# 4. 测试可视化
python visualization.py
```

## 📚 扩展阅读

- [arXiv API 文档](https://arxiv.org/help/api)
- [Semantic Scholar API](https://api.semanticscholar.org/)
- [Pandas 文档](https://pandas.pydata.org/)
- [Matplotlib 教程](https://matplotlib.org/stable/tutorials/)

---

_安装时间：2026-02-28_
_版本：1.0.0_
