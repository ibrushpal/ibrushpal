# iBrushPal Git/GitHub使用指南

## 首次设置Git

```bash
# 1. 安装Git
sudo apt install git -y

# 2. 配置Git用户信息
git config --global user.email "您的邮箱"
git config --global user.name "您的用户名"

# 3. 初始化Git仓库
git init

# 4. 添加所有文件
git add .

# 5. 首次提交
git commit -m "初始提交"

# 6. 连接到GitHub仓库
git remote add origin https://github.com/您的用户名/ibrushpal.git

# 7. 推送到GitHub
git branch -M main
git push -u origin main
```

## 日常更新流程

```bash
# 1. 拉取最新代码（如果有其他人协作）
git pull origin main

# 2. 添加更改的文件
git add .

# 3. 提交更改
git commit -m "更新描述"

# 4. 推送到GitHub
git push origin main
```

## 常用Git命令

```bash
# 查看状态
git status

# 查看提交历史
git log

# 查看远程仓库
git remote -v

# 撤销本地修改
git checkout -- .

# 创建新分支
git checkout -b feature-branch
```

## GitHub仓库设置

1. 在GitHub创建新仓库：`ibrushpal`
2. 获取仓库URL：`https://github.com/您的用户名/ibrushpal.git`
3. 按照首次设置流程连接

## 注意事项

- 确保`.env`等敏感文件添加到`.gitignore`
- 定期提交和推送，避免代码丢失
- 使用有意义的提交信息