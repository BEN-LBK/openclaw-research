#!/usr/bin/env python3
"""
学术搜索工具
支持arXiv、Google Scholar等学术搜索引擎
"""

import json
import subprocess
from typing import List, Dict
from datetime import datetime

def search_arxiv(query: str, max_results: int = 10) -> List[Dict]:
    """
    搜索arXiv论文
    
    Args:
        query: 搜索关键词
        max_results: 最大结果数
    
    Returns:
        论文列表
    """
    # 使用arxiv API（需要安装：pip install arxiv）
    try:
        import arxiv
        
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        results = []
        for paper in search.results():
            results.append({
                "title": paper.title,
                "authors": [author.name for author in paper.authors],
                "summary": paper.summary,
                "published": paper.published.strftime("%Y-%m-%d"),
                "url": paper.entry_id,
                "pdf_url": paper.pdf_url,
                "categories": paper.categories
            })
        
        return results
    except ImportError:
        return {"error": "请先安装arxiv库：pip install arxiv"}

def search_semantic_scholar(query: str, limit: int = 10) -> List[Dict]:
    """
    搜索Semantic Scholar
    
    Args:
        query: 搜索关键词
        limit: 最大结果数
    
    Returns:
        论文列表
    """
    # 使用semanticscholar API（需要安装：pip install semanticscholar）
    try:
        from semanticscholar import SemanticScholar
        
        sch = SemanticScholar()
        results = sch.search_paper(query, limit=limit)
        
        papers = []
        for paper in results:
            papers.append({
                "title": paper.title,
                "authors": [author.name for author in paper.authors],
                "year": paper.year,
                "abstract": paper.abstract,
                "url": paper.url,
                "citation_count": paper.citationCount,
                "venue": paper.venue
            })
        
        return papers
    except ImportError:
        return {"error": "请先安装semanticscholar库：pip install semanticscholar"}

def format_paper_list(papers: List[Dict], format: str = "markdown") -> str:
    """
    格式化论文列表
    
    Args:
        papers: 论文列表
        format: 输出格式（markdown/bibtex/json）
    
    Returns:
        格式化后的文本
    """
    if format == "markdown":
        output = "# 搜索结果\n\n"
        for i, paper in enumerate(papers, 1):
            output += f"## {i}. {paper.get('title', 'N/A')}\n"
            output += f"- **作者**: {', '.join(paper.get('authors', []))}\n"
            output += f"- **年份**: {paper.get('year', paper.get('published', 'N/A'))}\n"
            if 'citation_count' in paper:
                output += f"- **引用数**: {paper['citation_count']}\n"
            output += f"- **链接**: {paper.get('url', 'N/A')}\n"
            if 'summary' in paper or 'abstract' in paper:
                abstract = paper.get('summary') or paper.get('abstract')
                output += f"- **摘要**: {abstract[:200]}...\n"
            output += "\n"
        return output
    
    elif format == "bibtex":
        # TODO: 实现BibTeX格式
        pass
    
    elif format == "json":
        return json.dumps(papers, indent=2, ensure_ascii=False)
    
    return ""

# 示例用法
if __name__ == "__main__":
    # 搜索arXiv
    print("搜索arXiv...")
    papers = search_arxiv("multi-agent reinforcement learning", max_results=5)
    print(format_paper_list(papers))
