# 研究分析技能清单

## 已安装技能

### 🎯 核心技能
1. **研究分析增强技能包** (`skills/research-enhanced/`)
   - 安装时间：2026-02-28
   - 版本：1.0.0
   - 状态：✅ 已安装

#### 包含模块：
- **学术搜索** (academic-search.py)
  - arXiv论文搜索
  - Semantic Scholar集成
  - 论文格式化输出

- **数据分析** (data-analysis.py)
  - 统计分析
  - 数据清洗
  - 自动报告生成

- **可视化** (visualization.py)
  - 多种图表类型
  - 对比分析
  - 趋势分析

#### 依赖库：
```
arxiv>=2.0.0
semanticscholar>=0.4.0
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
```

---

## 推荐的 MCP Servers

### 待安装
1. **@modelcontextprotocol/server-filesystem**
   - 文件系统增强
   - 用途：更好的文件操作

2. **@modelcontextprotocol/server-brave-search**
   - 网络搜索增强
   - 用途：学术资源搜索

3. **@modelcontextprotocol/server-postgres**
   - 数据库访问
   - 用途：数据存储和查询

4. **@modelcontextprotocol/server-puppeteer**
   - 浏览器自动化
   - 用途：网页数据抓取

---

## ClawHub 推荐技能

### 待安装
1. **数据分析技能包**
   - 增强数据处理
   - 更多统计方法

2. **学术写作技能包**
   - 论文格式化
   - 引用管理

3. **图表生成技能包**
   - 交互式可视化
   - 更多图表类型

---

## 使用指南

### 快速开始
```bash
# 安装依赖
cd /Users/ben/.openclaw/workspace-research/skills/research-enhanced
pip install -r requirements.txt

# 测试学术搜索
python academic-search.py

# 测试数据分析
python data-analysis.py

# 测试可视化
python visualization.py
```

### 在 OpenClaw 中使用
```python
# 学术搜索
search_arxiv("multi-agent systems", max_results=10)

# 数据分析
analyzer = DataAnalyzer("data.csv")
report = analyzer.generate_report()

# 可视化
viz = Visualizer()
viz.create_chart(data, chart_type='bar', save_path='chart.png')
```

---

## 更新记录

### 2026-02-28
- ✅ 创建研究分析增强技能包
- ✅ 实现学术搜索模块
- ✅ 实现数据分析模块
- ✅ 实现可视化模块
- ✅ 编写使用文档

---

_最后更新：2026-02-28_
