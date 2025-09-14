# iBrushPal首次GitHub同步指南

## 仓库信息
- **仓库地址**: https://github.com/ibrushpal/ibrushpal.git
- **项目目录**: ~/ibrushpal

## 首次同步步骤

```bash
# 1. 进入项目目录
cd ~/ibrushpal

# 2. 初始化Git（如果未初始化）
git init

# 3. 配置Git用户信息
git config --global user.email "您的邮箱"
git config --global user.name "您的用户名"

# 4. 运行同步脚本
chmod +x github_sync.sh
./github_sync.sh
```

## 同步脚本功能
- 自动设置远程仓库到 `https://github.com/ibrushpal/ibrushpal.git`
- 添加所有文件到Git
- 提交更改并推送到GitHub

## 如果遇到问题

### 1. 如果仓库已存在内容
```bash
# 先拉取远程内容
git pull origin main

# 如果有冲突，手动解决后提交
git add .
git commit -m "合并冲突解决"
git push origin main
```

### 2. 如果权限被拒绝
```bash
# 检查SSH密钥或使用HTTPS+令牌
git remote set-url origin https://用户名:令牌@github.com/ibrushpal/ibrushpal.git
```

### 3. 强制推送（谨慎使用）
```bash
git push -f origin main
```

## 日常更新命令
```bash
# 简单更新
git add .
git commit -m "更新描述"
git push origin main

# 或直接运行脚本
./github_sync.sh
```

现在您可以开始将服务器代码同步到GitHub仓库了！