# 从GitHub拉取更新指南

## 使用场景
当GitHub仓库有更新时，将最新代码同步到服务器。

## 使用方法

### 方法一：使用拉取脚本（推荐）
```bash
# 给脚本执行权限
chmod +x github_pull.sh

# 运行拉取脚本
./github_pull.sh
```

### 方法二：手动Git命令
```bash
# 1. 拉取最新代码
git pull origin main

# 2. 如果有冲突，解决冲突
git status  # 查看冲突文件
# 手动编辑冲突文件
git add .   # 添加解决后的文件
git commit -m "解决冲突"

# 3. 如果拉取失败，强制覆盖（谨慎使用）
git fetch --all
git reset --hard origin/main
```

## 常见问题

### 1. 权限被拒绝
```bash
chmod +x github_pull.sh
```

### 2. 未设置Git用户信息
```bash
git config --global user.email "hzd@ibrushpal.com"
git config --global user.name "ibrushpal"
```

### 3. 未设置远程仓库
```bash
git remote add origin https://github.com/ibrushpal/ibrushpal.git
```

### 4. 冲突解决
如果拉取时出现冲突：
1. 查看冲突文件：`git status`
2. 编辑文件解决冲突
3. 标记冲突已解决：`git add 文件名`
4. 提交：`git commit -m "解决冲突"`

## 安全提示
- 拉取前建议备份重要文件
- 如果服务器有未提交的更改，先提交或备份
- 生产环境建议在测试环境先验证更新