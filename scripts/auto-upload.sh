#!/bin/bash
# OpenClaw 研究报告自动上传脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 工作目录
WORKSPACE="/Users/ben/.openclaw/workspace-research"
REPORTS_DIR="$WORKSPACE/reports"

echo -e "${GREEN}🦞 OpenClaw 研究报告自动上传${NC}"
echo "================================"

# 切换到工作目录
cd "$WORKSPACE"

# 检查是否有新的报告
echo -e "\n${YELLOW}检查报告目录...${NC}"
REPORT_COUNT=$(ls -1 reports/*.md 2>/dev/null | wc -l)
echo "发现 $REPORT_COUNT 份报告"

# 检查git状态
echo -e "\n${YELLOW}检查Git状态...${NC}"
git status --short

# 添加所有更改
echo -e "\n${YELLOW}添加更改到暂存区...${NC}"
git add .

# 检查是否有更改
if git diff --staged --quiet; then
    echo -e "${GREEN}✓ 没有新的更改需要提交${NC}"
    exit 0
fi

# 生成提交信息
CHANGED_FILES=$(git diff --staged --name-only)
COMMIT_MSG="docs: 更新研究报告

新增/更新的文件：
$CHANGED_FILES"

# 提交更改
echo -e "\n${YELLOW}提交更改...${NC}"
git commit -m "$COMMIT_MSG"

# 推送到GitHub
echo -e "\n${YELLOW}推送到GitHub...${NC}"
git push origin main

echo -e "\n${GREEN}✓ 报告已成功上传到GitHub！${NC}"
echo "仓库地址: https://github.com/BEN-LBK/openclaw-research"
