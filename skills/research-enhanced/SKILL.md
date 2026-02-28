# 研究分析增强技能包

## 核心定位
为研究分析Agent提供专业的研究工具和能力增强。

## 包含技能

### 1. 学术搜索技能 (academic-search)
- arXiv论文搜索
- Google Scholar集成
- Semantic Scholar API
- DOI解析

### 2. 数据分析技能 (data-analysis)
- Python数据分析（Pandas, NumPy）
- 统计分析
- 数据清洗
- 报告生成

### 3. 可视化技能 (visualization)
- Matplotlib图表生成
- 数据可视化
- 交互式图表
- 报告图表

### 4. 文献管理技能 (literature-management)
- BibTeX管理
- 引用格式化
- 文献去重
- 引用网络分析

### 5. 报告增强技能 (report-enhancement)
- 自动目录生成
- 图表编号
- 参考文献管理
- 格式优化

## 安装状态
- [x] 学术搜索技能 - 基于现有web_search
- [x] 数据分析技能 - 基于exec + Python
- [x] 可视化技能 - 基于exec + matplotlib
- [ ] 文献管理技能 - 需要MCP集成
- [x] 报告增强技能 - 已实现

## 使用示例

### 学术搜索
```python
# 搜索arXiv论文
search_arxiv("multi-agent systems", max_results=10)

# 搜索Google Scholar
search_scholar("AI automation", year_range="2023-2024")
```

### 数据分析
```python
# 分析CSV数据
analyze_data("data.csv", 
    analysis_type="statistical",
    generate_report=True)
```

### 可视化
```python
# 生成图表
create_visualization(
    data,
    chart_type="bar",
    title="研究趋势分析",
    save_path="charts/trend.png"
)
```

---

_安装时间：2026-02-28_
