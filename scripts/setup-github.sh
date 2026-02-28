#!/bin/bash
# GitHub仓库设置脚本

set -e

echo "🦞 设置GitHub仓库"
echo "=================="

# 检查gh是否已安装
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI未安装"
    echo "请先安装: brew install gh"
    exit 1
fi

# 检查认证状态
echo -e "\n检查GitHub认证状态..."
if ! gh auth status &> /dev/null; then
    echo "⚠️  GitHub CLI未认证"
    echo -e "\n请运行以下命令进行认证："
    echo "  gh auth login"
    echo -e "\n认证步骤："
    echo "1. 选择 GitHub.com"
    echo "2. 选择 HTTPS"
    echo "3. 选择 Yes (Login with GitHub CLI)"
    echo "4. 在浏览器中完成授权"
    exit 1
fi

# 获取用户名
USERNAME=$(gh api user --jq '.login')
REPO_NAME="openclaw-research"

echo -e "\n✓ 已认证用户: $USERNAME"

# 创建仓库
echo -e "\n创建GitHub仓库..."
if gh repo create "$REPO_NAME" \
    --public \
    --description "OpenClaw Research Agent 自动生成的研究报告" \
    --source=. \
    --remote=origin \
    --push; then
    echo -e "\n✅ 仓库创建成功！"
    echo "仓库地址: https://github.com/$USERNAME/$REPO_NAME"
else
    echo -e "\n⚠️  仓库可能已存在，尝试添加远程仓库..."
    git remote add origin "https://github.com/$USERNAME/$REPO_NAME.git" 2>/dev/null || true
    echo -e "\n请手动推送:"
    echo "  git push -u origin main"
fi

echo -e "\n📋 后续步骤："
echo "1. 每次生成报告后，运行: ./scripts/auto-upload.sh"
echo "2. 或者在OpenClaw中配置自动上传"
