#!/usr/bin/env python3
"""
数据分析工具
提供统计分析、数据清洗、报告生成等功能
"""

import pandas as pd
import numpy as np
import json
from typing import Dict, List, Any
from pathlib import Path

class DataAnalyzer:
    """数据分析器"""
    
    def __init__(self, data_path: str = None, data: pd.DataFrame = None):
        """
        初始化数据分析器
        
        Args:
            data_path: 数据文件路径
            data: DataFrame对象
        """
        if data is not None:
            self.df = data
        elif data_path:
            self.df = self._load_data(data_path)
        else:
            self.df = None
    
    def _load_data(self, path: str) -> pd.DataFrame:
        """加载数据"""
        path = Path(path)
        if path.suffix == '.csv':
            return pd.read_csv(path)
        elif path.suffix in ['.xlsx', '.xls']:
            return pd.read_excel(path)
        elif path.suffix == '.json':
            return pd.read_json(path)
        else:
            raise ValueError(f"不支持的文件格式: {path.suffix}")
    
    def basic_statistics(self) -> Dict[str, Any]:
        """基础统计分析"""
        if self.df is None:
            return {"error": "未加载数据"}
        
        stats = {
            "shape": self.df.shape,
            "columns": list(self.df.columns),
            "dtypes": self.df.dtypes.to_dict(),
            "missing_values": self.df.isnull().sum().to_dict(),
            "numeric_stats": self.df.describe().to_dict()
        }
        
        return stats
    
    def correlation_analysis(self, method: str = 'pearson') -> Dict:
        """相关性分析"""
        if self.df is None:
            return {"error": "未加载数据"}
        
        numeric_df = self.df.select_dtypes(include=[np.number])
        corr_matrix = numeric_df.corr(method=method)
        
        return {
            "correlation_matrix": corr_matrix.to_dict(),
            "strong_correlations": self._find_strong_correlations(corr_matrix)
        }
    
    def _find_strong_correlations(self, corr_matrix: pd.DataFrame, threshold: float = 0.7) -> List[Dict]:
        """找出强相关变量对"""
        strong_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) >= threshold:
                    strong_corr.append({
                        "var1": corr_matrix.columns[i],
                        "var2": corr_matrix.columns[j],
                        "correlation": corr_value
                    })
        return strong_corr
    
    def clean_data(self, strategies: Dict = None) -> pd.DataFrame:
        """
        数据清洗
        
        Args:
            strategies: 清洗策略，如 {"missing": "drop", "duplicates": "drop"}
        
        Returns:
            清洗后的DataFrame
        """
        if self.df is None:
            return None
        
        df_clean = self.df.copy()
        
        # 默认策略
        if strategies is None:
            strategies = {
                "missing": "fill_mean",
                "duplicates": "drop",
                "outliers": "keep"
            }
        
        # 处理缺失值
        if strategies.get("missing") == "drop":
            df_clean = df_clean.dropna()
        elif strategies.get("missing") == "fill_mean":
            numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
            df_clean[numeric_cols] = df_clean[numeric_cols].fillna(
                df_clean[numeric_cols].mean()
            )
        
        # 处理重复值
        if strategies.get("duplicates") == "drop":
            df_clean = df_clean.drop_duplicates()
        
        return df_clean
    
    def generate_report(self, output_path: str = None) -> str:
        """生成分析报告"""
        if self.df is None:
            return "错误：未加载数据"
        
        report = "# 数据分析报告\n\n"
        report += f"**生成时间**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # 1. 数据概览
        report += "## 1. 数据概览\n\n"
        report += f"- **数据维度**: {self.df.shape[0]} 行 × {self.df.shape[1]} 列\n"
        report += f"- **列名**: {', '.join(self.df.columns)}\n\n"
        
        # 2. 统计摘要
        report += "## 2. 统计摘要\n\n"
        stats = self.basic_statistics()
        report += "### 数值型变量统计\n\n"
        report += pd.DataFrame(stats['numeric_stats']).to_markdown()
        report += "\n\n"
        
        # 3. 缺失值分析
        report += "## 3. 缺失值分析\n\n"
        missing = stats['missing_values']
        report += "| 列名 | 缺失数量 | 缺失比例 |\n"
        report += "|------|---------|----------|\n"
        for col, count in missing.items():
            ratio = count / len(self.df) * 100
            report += f"| {col} | {count} | {ratio:.2f}% |\n"
        report += "\n"
        
        # 4. 相关性分析
        report += "## 4. 相关性分析\n\n"
        corr_result = self.correlation_analysis()
        if corr_result['strong_correlations']:
            report += "### 强相关变量对\n\n"
            for pair in corr_result['strong_correlations']:
                report += f"- {pair['var1']} ↔ {pair['var2']}: {pair['correlation']:.3f}\n"
        else:
            report += "未发现强相关变量对（阈值=0.7）\n"
        report += "\n"
        
        # 保存报告
        if output_path:
            Path(output_path).write_text(report, encoding='utf-8')
            report += f"\n---\n报告已保存至: {output_path}\n"
        
        return report

# 示例用法
if __name__ == "__main__":
    # 创建示例数据
    data = pd.DataFrame({
        'A': np.random.randn(100),
        'B': np.random.randn(100),
        'C': np.random.choice(['X', 'Y', 'Z'], 100)
    })
    
    # 添加一些缺失值
    data.loc[0:10, 'A'] = np.nan
    
    # 分析
    analyzer = DataAnalyzer(data=data)
    print(analyzer.generate_report())
