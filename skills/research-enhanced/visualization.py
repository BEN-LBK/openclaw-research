#!/usr/bin/env python3
"""
数据可视化工具
生成各种类型的图表
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from pathlib import Path

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

class Visualizer:
    """数据可视化器"""
    
    def __init__(self, style: str = 'seaborn'):
        """初始化可视化器"""
        plt.style.use(style)
        self.fig = None
        self.ax = None
    
    def create_chart(
        self,
        data: pd.DataFrame,
        chart_type: str = 'bar',
        x: str = None,
        y: str = None,
        title: str = "",
        xlabel: str = "",
        ylabel: str = "",
        save_path: str = None,
        **kwargs
    ) -> str:
        """
        创建图表
        
        Args:
            data: 数据
            chart_type: 图表类型（bar, line, pie, scatter, histogram）
            x: X轴列名
            y: Y轴列名
            title: 标题
            xlabel: X轴标签
            ylabel: Y轴标签
            save_path: 保存路径
            **kwargs: 其他参数
        
        Returns:
            图表文件路径
        """
        fig, ax = plt.subplots(figsize=kwargs.get('figsize', (10, 6)))
        
        if chart_type == 'bar':
            if x and y:
                data.plot.bar(x=x, y=y, ax=ax, **kwargs)
            else:
                data.plot.bar(ax=ax, **kwargs)
        
        elif chart_type == 'line':
            if x and y:
                data.plot.line(x=x, y=y, ax=ax, **kwargs)
            else:
                data.plot.line(ax=ax, **kwargs)
        
        elif chart_type == 'pie':
            if y:
                data[y].plot.pie(ax=ax, **kwargs)
            else:
                data.plot.pie(ax=ax, **kwargs)
        
        elif chart_type == 'scatter':
            if x and y:
                data.plot.scatter(x=x, y=y, ax=ax, **kwargs)
        
        elif chart_type == 'histogram':
            if y:
                data[y].plot.hist(ax=ax, **kwargs)
            else:
                data.plot.hist(ax=ax, **kwargs)
        
        # 设置标题和标签
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图表
        if save_path:
            save_path = Path(save_path)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
            return str(save_path)
        else:
            # 临时保存
            temp_path = Path('/tmp/chart.png')
            fig.savefig(temp_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
            return str(temp_path)
    
    def create_comparison_chart(
        self,
        data: Dict[str, float],
        title: str = "对比分析",
        chart_type: str = 'bar',
        save_path: str = None
    ) -> str:
        """
        创建对比图表
        
        Args:
            data: 数据字典 {label: value}
            title: 标题
            chart_type: 图表类型
            save_path: 保存路径
        
        Returns:
            图表文件路径
        """
        df = pd.DataFrame(list(data.items()), columns=['Item', 'Value'])
        df = df.set_index('Item')
        
        return self.create_chart(
            df,
            chart_type=chart_type,
            title=title,
            ylabel='值',
            save_path=save_path
        )
    
    def create_trend_chart(
        self,
        data: pd.DataFrame,
        time_col: str,
        value_cols: List[str],
        title: str = "趋势分析",
        save_path: str = None
    ) -> str:
        """
        创建趋势图表
        
        Args:
            data: 数据
            time_col: 时间列名
            value_cols: 数值列名列表
            title: 标题
            save_path: 保存路径
        
        Returns:
            图表文件路径
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        for col in value_cols:
            ax.plot(data[time_col], data[col], marker='o', label=col)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('时间', fontsize=12)
        ax.set_ylabel('值', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            save_path = Path(save_path)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
            return str(save_path)
        else:
            temp_path = Path('/tmp/trend_chart.png')
            fig.savefig(temp_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
            return str(temp_path)

# 示例用法
if __name__ == "__main__":
    # 创建可视化器
    viz = Visualizer()
    
    # 示例1：柱状图
    data = pd.DataFrame({
        'Category': ['A', 'B', 'C', 'D'],
        'Value': [10, 20, 15, 25]
    })
    path = viz.create_chart(
        data,
        chart_type='bar',
        x='Category',
        y='Value',
        title='示例柱状图',
        save_path='charts/bar_chart.png'
    )
    print(f"图表已保存: {path}")
    
    # 示例2：对比图
    comparison_data = {
        '方法A': 85,
        '方法B': 92,
        '方法C': 78,
        '方法D': 95
    }
    path = viz.create_comparison_chart(
        comparison_data,
        title='方法对比',
        save_path='charts/comparison.png'
    )
    print(f"对比图已保存: {path}")
